# Use the official Python image from the Docker Hub
FROM python:latest

# Set the working directory in the container
WORKDIR /app

# Copy the contents of the backend directory into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 8002

# Run main.py when the container launches
CMD ["uvicorn", "main:app","--host", "0.0.0.0", "--port", "8002"]