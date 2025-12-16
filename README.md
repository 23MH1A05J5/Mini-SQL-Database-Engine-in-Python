# Mini SQL Database Engine in Python

## Overview

This project is a simplified, **in-memory SQL query engine** implemented
in Python.

It loads data from a user-specified CSV file, parses a small subset of
SQL, and executes the query on rows stored entirely in memory.

The goal of this project is to: - Demystify how a database processes
basic `SELECT` queries - Practice data parsing, filtering, and
aggregation logic - Understand query execution without relying on an
actual database engine

------------------------------------------------------------------------

## Key Features

-   Load a CSV file into memory as a list of dictionaries (one
    dictionary per row)
-   Support for `SELECT`, `FROM`, optional single-condition `WHERE`, and
    `COUNT` aggregation
-   Interactive command-line REPL for executing SQL-like queries
-   Clear and user-friendly error messages for invalid syntax and
    unsupported queries

------------------------------------------------------------------------

## Project Structure

    mini_sql_engine/
    │
    ├── cli.py            # Command-line REPL, entry point
    ├── parser.py         # Small SQL parser for restricted grammar
    ├── engine.py         # In-memory query execution engine
    ├── Dockerfile        # Container image definition
    ├── employees.csv
    ├── sales.csv
    ├── sensors.csv
    ├── users.csv
    ├── mixed_types.csv
    └── README.md

Additional CSV files are included to test different scenarios.

------------------------------------------------------------------------

## Setup and Running the CLI

### Prerequisites

-   Python **3.11 or later**
-   Docker (optional, for containerized execution)

------------------------------------------------------------------------

### 1. Running Locally with Python

Clone the repository and navigate to the project directory:

``` bash
git clone https://github.com/23MH1A05L3/Build-a-Library-Management-System-API.git
cd mini_sql_engine
```

Ensure the CSV files you want to query (e.g., `employees.csv`,
`sales.csv`) are in the same directory as `cli.py`.

Start the CLI:

``` bash
python cli.py
```

When prompted, enter the CSV filename:

    employees.csv

You will see the prompt:

    mini-sql>

-   Enter SQL queries using the supported grammar
-   Type `exit` or `quit` to leave the REPL

------------------------------------------------------------------------

### 2. Running with Docker

#### Pull the Image

``` bash
docker pull ramapithani/mini-sql-engine
```

#### Run the Container

``` bash
docker run -it ramapithani/mini-sql-engine
```

The container automatically runs:

``` bash
python cli.py
```

Inside the CLI: - Enter the CSV filename (e.g., `employees.csv`) - Run
SQL queries at the `mini-sql>` prompt - Type `exit` or `quit` to stop
the container

------------------------------------------------------------------------

## Supported SQL Grammar

The engine supports only a **restricted subset of SQL**. Unsupported
syntax produces clear error messages.

### General Form

``` sql
SELECT <select_list>
FROM <table_name>
[WHERE <column> <operator> <value>];
```

-   `<table_name>` is the CSV filename **without `.csv`**
-   Only **one table** can be queried at a time
-   `WHERE` supports **only one condition**

------------------------------------------------------------------------

## SELECT (Projection)

### Supported Forms

**Select all columns**

``` sql
SELECT * FROM employees;
```

**Select specific columns**

``` sql
SELECT id, name, country FROM employees;
```

### Rules

-   Column names must exactly match CSV headers

-   Non-existent columns produce:

        Selected column not found: <name>

------------------------------------------------------------------------

## FROM (Table Name)

-   Table name comes from the CSV filename without extension

-   Unknown tables produce:

        Unknown table: <name>

Example:

``` sql
SELECT * FROM users;
```

------------------------------------------------------------------------

## WHERE (Filtering)

### Supported Pattern

``` sql
WHERE <column> <operator> <value>
```

### Supported Operators

-   `=`
-   `!=`
-   `>`
-   `<`
-   `>=`
-   `<=`

### Value Types

-   Numbers: `age > 30`
-   Strings: `country = 'India'`

### Examples

``` sql
SELECT * FROM employees WHERE country = 'India';
SELECT name, age FROM employees WHERE age > 30;
SELECT * FROM sales WHERE amount >= 150.0;
```

### Errors

-   Missing column:

        Column in WHERE not found: <name>

-   Unsupported operator:

        Unsupported operator in WHERE

------------------------------------------------------------------------

## Aggregation: COUNT

### Supported Forms

**Count all rows**

``` sql
SELECT COUNT(*) FROM employees;
SELECT COUNT(*) FROM employees WHERE country = 'India';
```

**Count non-empty column values**

``` sql
SELECT COUNT(age) FROM employees;
SELECT COUNT(credit_balance) FROM users WHERE is_premium = 'True';
```

### Rules

-   `COUNT(*)` → total filtered rows

-   `COUNT(column)` → non-empty values only

-   Missing column:

        Column not found for COUNT: <name>

------------------------------------------------------------------------

## Unsupported Queries

The following are intentionally **not supported**:

-   JOIN, GROUP BY, ORDER BY, LIMIT
-   INSERT, UPDATE, DELETE
-   Multiple tables in one query
-   Multiple WHERE conditions (AND / OR / NOT)
-   Functions other than COUNT
-   Aliases, subqueries, nested SELECTs

------------------------------------------------------------------------

## Example Queries

``` sql
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
```

------------------------------------------------------------------------

## Example Error Queries

``` sql
    -- Syntax error: missing FROM
    SELECT name, age WHERE age > 30;

    -- Non-existent column in SELECT
    SELECT foo FROM employees;

    -- Non-existent column in WHERE
    SELECT * FROM employees WHERE foo = 'X';

    -- Unsupported operator
    SELECT * FROM employees WHERE age >> 30;
```

------------------------------------------------------------------------

## Error Handling Behavior

The engine is designed to **fail fast and clearly**:

-   Invalid syntax (missing FROM, bad SELECT list, empty WHERE, unsupported operator)
    → “Invalid ...” / “Missing ...” style messages.
-   Non‑existent table or column
    → “Unknown table: <name>” or “Selected column not found: <name>”.
-   Unexpected internal issues
    → generic error message instead of a Python traceback.
    
This keeps the CLI stable and user-friendly while enforcing a strict SQL
subset.


