# 1. Use Python 3.12 (matches your requirements)
FROM python:3.12-slim

# 2. Install 'uv' for fast package management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 3. Install System Dependencies (Needed for Supabase/Postgres)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 4. Set Working Directory
WORKDIR /app

# 5. Copy Dependency Files
COPY pyproject.toml uv.lock ./

# 6. Install Python Dependencies
RUN uv pip install --system --no-cache -r pyproject.toml

# 7. Copy Your Code
# This copies main.py, backend folder, etc.
# (But it skips .env because of .dockerignore)
COPY . .

# Expose the port FastAPI listens on
EXPOSE 8000

# 8. Command to run the app
# Since main.py is in the root, we call "main:app"
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]