FROM mcr.microsoft.com/playwright/python:v1.43.0-jammy
WORKDIR /app
COPY requirements.txt ./
# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt \
	&& playwright install
# Copy backend code and alembic migrations
COPY . .
COPY ./alembic ./alembic
ENV PYTHONPATH=/app
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
