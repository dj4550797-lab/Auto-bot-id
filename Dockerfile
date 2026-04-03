# Use official Python image
FROM python:3.10-slim-buster

# Update system and install required dependencies for psutil
RUN apt-get update && apt-get install -y gcc python3-dev

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN pip3 install -U -r requirements.txt

# Copy all the bot files to the container
COPY . .

# Run the bot
CMD ["python3", "bot.py"]