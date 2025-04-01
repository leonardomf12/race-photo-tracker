# Use the official PostgreSQL image as base
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

EXPOSE 8050

# Define the command to run the app
CMD ["bash", "-c", "python3 app.py"]

