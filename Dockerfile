# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Install PostgreSQL development packages
RUN apt-get update && apt-get install -y git gcc libpq-dev

# Copy the current directory contents into the container at /app
COPY ./app-cp /app

WORKDIR /app

# Install any needed packages specified in requirements.txt
RUN pip install .

# Make port 80 available to the world outside this container
EXPOSE 80

# Run app.py when the container launches
CMD ["uvicorn", "unity_sps_ogc_processes_api.main:app", "--host", "0.0.0.0", "--port", "80"]
