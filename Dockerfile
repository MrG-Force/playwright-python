FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create a working directory
WORKDIR /app

COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy the rest of the application code (if needed, for context)
COPY . /app/

# Set the default command (can be overridden)
CMD ["pytest"]