# 1. Use a modern Python base
FROM python:3.10-slim-bookworm

# 2. Install system dependencies
RUN apt-get update && apt-get install -y gcc python3-dev

# 3. Set working directory to /app
WORKDIR /app

# 4. Copy requirements first for faster building
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# 5. Copy EVERY file from your folder into the container
# This fixes the "no root" or "file not found" error
COPY . .

# 6. Expose the port for Render Web Service
EXPOSE 10000

# 7. Start the bot (which now includes the web server)
CMD ["python3", "bot.py"]