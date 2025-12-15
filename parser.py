# parser.py

class SqlError(Exception):
    """Custom error type for SQL parsing/execution problems."""
    pass


def _try_convert_number(value: str):
    """Convert string to int or float if possible, else keep as string."""
    value = value.strip()
    # Remove surrounding quotes for strings
    if (value.startswith("'") and value.endswith("'")) or \
       (value.startswith('"') and value.endswith('"')):
        return value[1:-1]

    # Try number
    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        return value


def parse_query(sql: str) -> dict:
    """
    Parse a very small subset of SQL:
      SELECT * FROM table;
      SELECT col1, col2 FROM table;
      SELECT COUNT(*) FROM table;
      SELECT COUNT(col) FROM table WHERE col > 10;
      SELECT col1 FROM table WHERE col2 = 'X';
    """
    if not sql:
        raise SqlError("Empty query")

    # Remove trailing semicolon and extra spaces
    sql = sql.strip().rstrip(";").strip()

    upper_sql = sql.upper()

    if not upper_sql.startswith("SELECT "):
        raise SqlError("Query must start with SELECT")

    # Split SELECT ... FROM ...
    if " FROM " not in upper_sql:
        raise SqlError("Missing FROM clause")

    select_part = sql[6: upper_sql.index(" FROM ")].strip()
    rest = sql[upper_sql.index(" FROM ") + len(" FROM "):].strip()

    # Split rest into FROM table [WHERE condition]
    where_index = rest.upper().find(" WHERE ")
    if where_index == -1:
        table_part = rest.strip()
        where_part = None
    else:
        table_part = rest[:where_index].strip()
        where_part = rest[where_index + len(" WHERE "):].strip()
        if not where_part:
            raise SqlError("Empty WHERE condition")

    if not table_part:
        raise SqlError("Missing table name in FROM clause")

    from_table = table_part

    # Parse SELECT columns / COUNT
    select_cols = _parse_select_columns(select_part)

    # Parse WHERE condition (single condition)
    where_clause = _parse_where(where_part) if where_part else None

    return {
        "select_cols": select_cols,
        "from_table": from_table,
        "where_clause": where_clause,
    }


def _parse_select_columns(select_part: str):
    part_upper = select_part.upper().strip()

    # COUNT(*)
    if part_upper.startswith("COUNT("):
        if part_upper == "COUNT(*)":
            return [{"type": "count", "target": "*"}]
        if not part_upper.endswith(")"):
            raise SqlError("Invalid COUNT syntax")
        inner = select_part[6:-1].strip()  # text inside COUNT(...)
        if not inner:
            raise SqlError("Invalid COUNT syntax")
        return [{"type": "count", "target": inner}]

    # *
    if part_upper == "*":
        return ["*"]

    # col1, col2, ...
    cols = [c.strip() for c in select_part.split(",")]
    if not all(cols):
        raise SqlError("Invalid column list in SELECT")
    return cols


def _parse_where(where_part: str):
    # Support operators: >=, <=, !=, >, <, =
    operators = ["!=", ">=", "<=", ">", "<", "="]
    for op in operators:
        idx = where_part.find(op)
        if idx != -1:
            left = where_part[:idx].strip()
            right = where_part[idx + len(op):].strip()
            if not left or not right:
                raise SqlError("Invalid WHERE condition")
            return {
                "col": left,
                "op": op,
                "val": _try_convert_number(right),
            }

    raise SqlError("Unsupported operator in WHERE (allowed: =, !=, >, <, >=, <=)")
