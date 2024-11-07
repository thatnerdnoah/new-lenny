# Use an Ubuntu base image
FROM --platform=linux/amd64 ubuntu:latest

# Install Python and other dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory inside the container
WORKDIR /app

# Clone the GitHub repository
# Replace "<github-repo-url>" with your GitHub repository URL
RUN git clone <github-repo-url> .

# Copy the necessary file into the specified directory
# Replace "source/file/path" with your local file path, and "/app/target/directory" with the target path in the container
COPY source/file/path /app/target/directory

# Install project dependencies
RUN pip3 install -r requirements.txt

# Run the project
CMD ["python3", "main.py"]
