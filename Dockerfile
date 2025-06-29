FROM python:3.10-slim

# Install OpenCV dependencies
RUN apt-get update && apt-get install -y libgl1 libglib2.0-0

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make uploads folder
RUN mkdir -p uploads

# Start the app
CMD ["python", "app.py"]
