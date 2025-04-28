FROM selenium/standalone-chrome:95.0-chromedriver-95.0-20250414

USER root

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    python3-dev \
    gcc \
    make \
    python3-venv

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml .
COPY udemypy/ ./udemypy/

# Install dependencies
RUN pip install --no-cache-dir .

# Define a volume for the SQLite database
VOLUME ["/app/data"]

# Set secrets 
RUN --mount=type=secret,id=TOKEN \
    --mount=type=secret,id=API_KEY \
    --mount=type=secret,id=API_KEY_SECRET \
    --mount=type=secret,id=ACCESS_TOKEN \
    --mount=type=secret,id=ACCESS_TOKEN_SECRET \
    TOKEN=$(cat /run/secrets/TOKEN) && \
    API_KEY=$(cat /run/secrets/API_KEY) && \
    API_KEY_SECRET=$(cat /run/secrets/API_KEY_SECRET) && \
    ACCESS_TOKEN=$(cat /run/secrets/ACCESS_TOKEN) && \
    ACCESS_TOKEN_SECRET=$(cat /run/secrets/ACCESS_TOKEN_SECRET)

# Set environment variables
ENV DATABASE=sqlite3 \
    CHANNEL_ID=@freecourses000 \
    CHANNEL_LINK=https://bit.ly/3k04NjZ \
    TWITTER_LINK=https://twitter.com/UdemyPy \
    TABLE_NAME=course \
    MAX_COURSES_TO_SEND=10 \
    PAGES_TO_SCRAPE=1 \
    COURSE_LIFETIME=15 \
    PAGE_LOAD_TIME=8

# Execution command
CMD ["bash"]
