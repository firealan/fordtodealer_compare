# Use the official Python base image
FROM python:3.11.8-slim

# Set the working directory in the container
WORKDIR /app

# Set PYTHONUNBUFFERED to ensure immediate flushing of Python output
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Install Firefox browser and driver, create a non-root user
RUN apt-get update && apt-get install -y firefox-esr && \
    apt-get autoremove -y && \
    apt-get clean -y && \
    rm -rf /var/lib/apt/lists/* && \
    useradd -m pyuser

# Copy only the requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the local code into the container
COPY . .

# Set appropriate permissions
RUN chown -R pyuser:pyuser /app && \
    chmod -R u+w /app

# Switch to the non-root user
USER pyuser

# Entry point - run your script
CMD ["python", "main.py"]