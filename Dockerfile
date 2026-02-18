# 1. Use Python 3.12
FROM python:3.12-slim

# 2. Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 3. Install system dependencies (Required for some Python packages)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 4. Set working directory
WORKDIR /app

# 5. Copy config files
COPY pyproject.toml uv.lock* ./

# 6. Install dependencies
# We use --system to install into the global python environment
RUN uv pip install --system --no-cache -r pyproject.toml

# 7. Copy the rest of the code
COPY . .

# 8. Run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]