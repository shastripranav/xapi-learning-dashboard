FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install --no-cache-dir fastapi uvicorn pydantic pydantic-settings pandas httpx python-dotenv aiosqlite python-multipart

COPY . .

RUN python -c "import sys; sys.path.insert(0, '.'); from data.generate_demo_data import main; main()"

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
