# Use the official PostgreSQL image as base
FROM postgres:15

# Set environment variables for PostgreSQL
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=12345
ENV POSTGRES_DB=mydatabase

# To acess the database
# Host: localhost
# Port: 5432
# db: mydatabase
# user: postgres
# pw: 12345

# Optionally, copy your custom initialization scripts
COPY dummy_data.sql docker-entrypoint-initdb.d/

EXPOSE 5432
