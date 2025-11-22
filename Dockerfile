FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Set timezone to Asia/Taipei
ENV TZ=Asia/Taipei
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install system dependencies (if any needed for lxml or others)
# lxml binary wheels are usually available, but gcc might be needed for some libs
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ src/
COPY .streamlit/ .streamlit/ 2>/dev/null || true

# Create data directory
RUN mkdir -p data

# Expose Streamlit port
EXPOSE 8501

# Command to run the app
# We will run streamlit by default, but we need to run the scheduler too.
# For simplicity in this monolithic container, we can run a script that starts both,
# OR just run streamlit and have streamlit start the scheduler (not recommended for production but easy),
# OR use supervisord.
#
# BETTER APPROACH: 
# run `src/main.py` which will be the entry point.
# If main.py is streamlit, it blocks.
#
# For now, let's assume the user runs `docker-compose up` which uses the command defined there.
# Default command:
CMD ["streamlit", "run", "src/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
