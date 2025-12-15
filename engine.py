# engine.py

import csv
import os
from parser import SqlError


def load_csv(path: str):
    """
    Load one CSV file into memory.
    Returns: (tables_dict, table_name)
    tables_dict maps table_name -> list[dict] rows.
    """
    if not os.path.exists(path):
        raise SqlError(f"CSV file not found: {path}")

    table_name = os.path.splitext(os.path.basename(path))[0]

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        raise SqlError("CSV file is empty")

    return {table_name: rows}, table_name


def execute_query(parsed: dict, tables: dict):
    table_name = parsed["from_table"]
    if table_name not in tables:
        raise SqlError(f"Unknown table: {table_name}")

    rows = tables[table_name]

    # WHERE filter
    where_clause = parsed["where_clause"]
    if where_clause:
        rows = _apply_where(rows, where_clause)

    select_cols = parsed["select_cols"]

    # COUNT aggregation
    if isinstance(select_cols, list) and select_cols and isinstance(select_cols[0], dict) \
       and select_cols[0].get("type") == "count":
        return _apply_count(rows, select_cols[0])

    # Regular projection
    return _apply_projection(rows, select_cols)


def _apply_where(rows, where_clause):
    col = where_clause["col"]
    op = where_clause["op"]
    val = where_clause["val"]

    filtered = []

    for row in rows:
        if col not in row:
            raise SqlError(f"Column in WHERE not found: {col}")

        cell = row[col]

        # Try to align types
        cell_val = _convert_cell(cell, val)

        if _compare(cell_val, op, val):
            filtered.append(row)

    return filtered


def _convert_cell(cell_str, target_val):
    # If target is number, convert cell to number
    if isinstance(target_val, (int, float)):
        try:
            if "." in cell_str:
                return float(cell_str)
            return int(cell_str)
        except ValueError:
            # If cannot convert, treat as non-matching
            return None
    # else keep as string
    return cell_str


def _compare(left, op, right):
    # Handle failed numeric conversion
    if left is None:
        return False

    if op == "=":
        return left == right
    if op == "!=":
        return left != right
    if op == ">":
        return left > right
    if op == "<":
        return left < right
    if op == ">=":
        return left >= right
    if op == "<=":
        return left <= right
    raise SqlError(f"Unsupported operator: {op}")


def _apply_count(rows, count_expr):
    target = count_expr["target"]
    if target == "*":
        count = len(rows)
    else:
        count = 0
        for row in rows:
            if target not in row:
                raise SqlError(f"Column not found for COUNT: {target}")
            value = row[target]
            if value is not None and value != "":
                count += 1

    return [{"count": count}]


def _apply_projection(rows, select_cols):
    if select_cols == ["*"]:
        return rows

    projected = []
    for row in rows:
        new_row = {}
        for col in select_cols:
            if col not in row:
                raise SqlError(f"Selected column not found: {col}")
            new_row[col] = row[col]
        projected.append(new_row)
    return projected
