# Use a small Python base image
FROM python:3.11-slim

# Set work directory inside the container
WORKDIR /app

# Copy project files into the image
COPY . /app

# Default command: run the CLI
# (User will still be able to type the CSV path and SQL queries)
CMD ["python", "cli.py"]
