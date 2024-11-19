FROM python:3.9-alpine3.13
LABEL maintainer="adoniashaile1@gmail.com"

# Print Python logs to the screen
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install system dependencies (if needed)
RUN apk add --no-cache --virtual .build-deps gcc musl-dev

# Copy the requirements files
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt

# Create a user to avoid running as root
RUN adduser --disabled-password --no-create-home django-user

# Set default value for the DEV argument
ARG DEV=false

# Create a virtual environment and install dependencies
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ "$DEV" = "true" ]; then \
        /py/bin/pip install -r /tmp/requirements.dev.txt; \
    fi && \
    # Clean up
    rm -rf /tmp/requirements.txt /tmp/requirements.dev.txt && \
    apk del .build-deps

# Set the environment path
ENV PATH="/py/bin:$PATH"

# Copy the application code
COPY ./app /app

# Expose the application port
EXPOSE 8000

# Switch to the non-root user
USER django-user