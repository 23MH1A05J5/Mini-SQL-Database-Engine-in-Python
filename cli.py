# cli.py

from parser import parse_query, SqlError
from engine import load_csv, execute_query


def print_rows(rows):
    if not rows:
        print("(no rows)")
        return

    # Determine columns from first row
    if isinstance(rows[0], dict):
        cols = list(rows[0].keys())
        # Header
        header = " | ".join(cols)
        print(header)
        print("-" * len(header))
        # Rows
        for row in rows:
            values = [str(row[c]) for c in cols]
            print(" | ".join(values))
    else:
        # For safety, if rows are not dict
        for row in rows:
            print(row)


def main():
    print("Mini SQL Engine (CSV + Python)")
    print("Enter CSV file path (e.g. sample.csv):")
    csv_path = input("> ").strip()

    try:
        tables, default_table = load_csv(csv_path)
    except SqlError as e:
        print(f"Error loading CSV: {e}")
        return

    print(f"Loaded table '{default_table}' from {csv_path}")
    print()
    print("Supported syntax (single table, single WHERE condition):")
    print("  SELECT * FROM table;")
    print("  SELECT col1, col2 FROM table;")
    print("  SELECT * FROM table WHERE age > 30;")
    print("  SELECT COUNT(*) FROM table;")
    print("  SELECT COUNT(col) FROM table WHERE country = 'India';")
    print("Type 'exit' or 'quit' to leave.")
    print()

    while True:
        sql = input("mini-sql> ").strip()
        if not sql:
            continue
        if sql.lower() in ("exit", "quit"):
            print("Bye.")
            break

        try:
            parsed = parse_query(sql)
            rows = execute_query(parsed, tables)
            print_rows(rows)
        except SqlError as e:
            print(f"SQL error: {e}")
        except Exception as e:
            # Catch-all to avoid crashing
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
