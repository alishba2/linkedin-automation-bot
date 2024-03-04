# Use the official Python 3.10 image as the base image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /ai-joblink-pro-python

# Copy the requirements.txt file and the Django application code
COPY ./requirements.txt /ai-joblink-pro-python


# Install Python dependencies
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Install additional system dependencies
RUN apt-get update && \
    apt-get install -y wget unzip && \
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the default command to run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
