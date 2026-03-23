# Use official Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy your bot files to the container
COPY . /app

# Install the requirements
RUN pip install --no-cache-dir -r requirements.txt

# Run the bot
CMD ["python", "bot.py"]