# Official Python Image
FROM python:3.11

# Setting the work directory
WORKDIR /app

# Copying requirements
COPY . /app

# Installing requirements
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --upgrade setuptools && \
    pip install --no-cache-dir --upgrade -r requirements.txt && \
    pip install --no-cache-dir --upgrade watchdog

# Exposing port
EXPOSE 8501

# Starting Streamlit
CMD ["streamlit", "run", "app/main.py"]