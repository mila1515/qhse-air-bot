FROM python:3.9-slim

WORKDIR /app

# Install evidently
RUN pip install evidently

# Expose the default UI port
EXPOSE 8000

# Run the UI service
CMD ["evidently", "ui", "--port", "8000", "--host", "0.0.0.0"]
