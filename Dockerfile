# --- Stage 1: Builder ---
# Use a specific slim variant as the builder base.
FROM python:3.11-slim-bookworm as builder

# Best Practice Environment Variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install build-time system dependencies (if needed for pip install)
# Example: RUN apt-get update && apt-get install -y --no-install-recommends gcc build-essential python3-dev libpq-dev && rm -rf /var/lib/apt/lists/*
# Add any packages required by your Python dependencies here

# Upgrade pip globally within the builder image
RUN pip install --no-cache-dir --upgrade pip

# Set working directory for context
WORKDIR /install

# Copy only the requirements file
COPY requirements.txt .

# Install Python dependencies globally into the builder's site-packages
# Use --no-cache-dir to keep layers smaller
# Use --require-hashes if your requirements.txt includes hashes
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt
    # If using hashes: pip install --no-cache-dir --prefix=/install --require-hashes -r requirements.txt

# --- Stage 2: Runtime ---
# Use the same slim variant for the final runtime image
FROM python:3.11-slim-bookworm

# Best Practice Environment Variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Build Arguments for user/group
ARG APP_USER=appuser
ARG APP_GROUP=appgroup
ARG UID=1001
ARG GID=1001

# Create non-root user and group
RUN groupadd -g ${GID} ${APP_GROUP} && \
    useradd -u ${UID} -g ${APP_GROUP} -m -s /bin/bash ${APP_USER}

# Install runtime system dependencies (if any are needed)
# Example: RUN apt-get update && apt-get install -y --no-install-recommends libpq5 && rm -rf /var/lib/apt/lists/*

# Set the final working directory
WORKDIR /app

# Copy installed packages from the builder stage's prefix install location
# This copies the contents of /install (like lib/python3.11/site-packages) into the root of the runtime image,
# merging them with the system Python installation.
COPY --from=builder /install /usr/local

# Copy the application code
COPY --chown=${APP_USER}:${APP_GROUP} . .

# Switch to the non-root user
USER ${APP_USER}