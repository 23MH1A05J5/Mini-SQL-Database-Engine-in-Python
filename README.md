Mini SQL Database Engine in Python

Overview

    This project is a simplified, in‑memory SQL query engine implemented in Python.
    It loads data from a user‑specified CSV file, parses a small subset of SQL, and executes the query on the rows stored in memory.
    The goal is to demystify what happens inside a database when you run a basic SELECT query and to practice data parsing, filtering, and aggregation logic.

Key features:

    Load a CSV file into memory as a list of dictionaries (one dict per row).

    Support for SELECT, FROM, an optional single‑condition WHERE clause, and COUNT aggregation.

    A simple command‑line REPL where the user can type SQL‑like queries.

    Clear error messages for invalid syntax, missing columns, or unsupported queries.

Project Structure

mini_sql_engine/
    cli.py # Command-line REPL, entry point
    parser.py # Very small SQL parser for a restricted grammar
    engine.py # In-memory execution engine on top of CSV data
    Dockerfile # Container image definition
    employees.csv
    sales.csv
    sensors.csv
    users.csv
    mixed_types.csv
    README.md

More CSV files are included for testing different scenarios.

Setup and Running the CLI

Prerequisites:

  Python 3.11 or later installed on your machine.

  Docker installed if you want to run the project in a container.

  1.Running locally with Python

    Clone the GitHub repository and go into the project folder:

    git clone https://github.com/23MH1A05L3/Build-a-Library-Management-System-API.git
    cd mini_sql_engine

    Ensure the CSV files you want to query (for example employees.csv or sales.csv) are in the same folder as cli.py.

    Start the CLI:

    python cli.py

    When prompted for the CSV path, type the filename, for example:

    employees.csv

    You will then see a prompt like:

    mini-sql>

    Enter SQL queries in the supported grammar (see next section).
    Type exit or quit to close the REPL.

2.Running in Docker

    Build the image

    From the mini_sql_engine folder (where the Dockerfile is):

    docker build -t mini-sql-engine .

    This creates a Docker image named mini-sql-engine containing the Python code.

    Run the container

      To allow the container to see and use the CSV files from the local project folder, mount the folder into /app.

      On Windows (cmd.exe or PowerShell) – replace the path with the actual project path:

          docker run -it -v "<project_folder-path>":/app mini-sql-engine

      On macOS / Linux (if needed):

          docker run -it -v "$PWD":/app mini-sql-engine

    The container will automatically run:

      python cli.py

    Inside the CLI:
      Enter the CSV file name, for example:
        employees.csv

    Type your SQL queries at the mini-sql> prompt.

    Type exit or quit to stop the container.

Supported SQL Grammar :

    The engine intentionally supports only a small, well‑defined subset of SQL.
    Anything outside this subset should produce a clear error message rather than silently doing the wrong thing.

General form:

    SELECT <select_list>
    FROM <table_name>
    [WHERE <column> <operator> <value>];

    <table_name> is the CSV filename without .csv (for employees.csv, the table name is employees).
    Only one table can be queried at a time.
    The WHERE clause is optional and supports only a single condition (no AND / OR / NOT).

SELECT (projection)

Supported forms:

    Select all columns:

    SELECT * FROM employees;

    Select specific columns (comma‑separated list):

    SELECT id, name, country FROM employees;

Rules:

    Column names must exactly match CSV headers.

    If any selected column does not exist, the engine returns an error such as
    “Selected column not found: <name>”.

    FROM (table name)

    The table name is derived from the CSV filename without extension.

    If the user loads users.csv, the valid table name in queries is users.

    If a query references an unknown table, the engine returns an error
    such as “Unknown table: <name>”.

Example: (assuming users.csv was the chosen file).

SELECT * FROM users;

WHERE (filtering with a single condition) :

    Supported pattern:

    WHERE <column> <operator> <value>

        Only one condition is allowed (no AND/OR).

    Supported comparison operators:
                                      =
                                      !=
                                      <
                                      =
                                      <=

    Values can be:

      Numbers: age > 30, salary >= 70000.5
      Quoted strings: country = 'India', status = "PAID"

    Examples:

      SELECT * FROM employees WHERE country = 'India';
      SELECT name, age FROM employees WHERE age > 30;
      SELECT * FROM sales WHERE amount >= 150.0;

    If the column in the WHERE clause does not exist, the engine returns an error like
        “Column in WHERE not found: <name>”.

    If the operator is not supported, the engine returns an error like
        “Unsupported operator in WHERE (allowed: =, !=, >, <, >=, <=)”.

Aggregation: COUNT

  The engine supports COUNT as a simple aggregation over the filtered rows.

  Supported forms:

    Count all rows:

        SELECT COUNT() FROM employees;
        SELECT COUNT() FROM employees WHERE country = 'India';

    Count non‑null, non‑empty values in a column:

        SELECT COUNT(age) FROM employees;
        SELECT COUNT(credit_balance) FROM users WHERE is_premium = 'True';

  Rules:

    COUNT(*) returns the total number of rows that pass the WHERE filter.

    COUNT(column) returns how many rows have a non‑empty value for that column after filtering.

    If the column in COUNT(column) does not exist, the engine returns an error such as
    “Column not found for COUNT: <name>”.

  Unsupported Queries:

    To keep the project simple, the following are not supported and should result in clear error messages or rejection:

      JOINs, GROUP BY, ORDER BY, LIMIT, INSERT, UPDATE, DELETE.

      Multiple tables in a single query.

      Multiple conditions in WHERE (no AND, OR, NOT).

      Functions other than COUNT.

      Aliases, subqueries, or nested SELECTs.

Example Queries :

Assuming employees.csv is loaded (table name employees):

    -- Select all columns
    SELECT * FROM employees;

    -- Select specific columns
    SELECT name, age, country FROM employees;

    -- Filter by numeric condition
    SELECT * FROM employees WHERE age > 30;

    -- Filter by string condition
    SELECT name, department FROM employees WHERE country = 'India';

    -- Count all rows
    SELECT COUNT(*) FROM employees;

    -- Count non-null salaries for a subset
    SELECT COUNT(salary) FROM employees WHERE is_full_time = 'True';

Example error‑testing queries:

    -- Syntax error: missing FROM
    SELECT name, age WHERE age > 30;

    -- Non-existent column in SELECT
    SELECT foo FROM employees;

    -- Non-existent column in WHERE
    SELECT * FROM employees WHERE foo = 'X';

    -- Unsupported operator
    SELECT * FROM employees WHERE age >> 30;

Error Handling Behaviour : 

    The engine aims to fail fast and clearly when the user enters unsupported or incorrect SQL:

    Invalid syntax (missing FROM, bad SELECT list, empty WHERE, unsupported operator)
    → “Invalid ...” / “Missing ...” style messages.

    Non‑existent table or column
    → “Unknown table: <name>” or “Selected column not found: <name>”.

    Unexpected internal issues
    → generic error message instead of a Python traceback.

  This ensures the CLI does not crash and gives helpful feedback to the user while staying within the restricted SQL grammar defined above.