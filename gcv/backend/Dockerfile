# Stage 1: Build the virtual environment
FROM python:3.12-slim as builder

# Install poetry
RUN pip install poetry

# Set poetry config
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Set working directory
WORKDIR /app

# Copy the dependency files
COPY ../pyproject.toml ../poetry.lock ./

# Install dependencies
RUN poetry install --no-root --no-dev

# Stage 2: Create the final image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy the virtual environment from the builder
COPY --from=builder /app/.venv ./.venv

# Activate the virtual environment
ENV PATH="/app/.venv/bin:$PATH"

# Copy the application code
COPY app /app

# Expose the port
EXPOSE 8000

# Run the application
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-w", "3", "-b", "0.0.0.0:8000", "main:app"]
