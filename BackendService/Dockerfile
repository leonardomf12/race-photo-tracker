# Use the official PostgreSQL image as base
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .


EXPOSE 8000

# Use exec form for better signal handling
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]



