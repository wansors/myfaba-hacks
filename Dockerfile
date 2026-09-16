# Use the lightweight debian:bookworm-slim image
# (bullseye is end-of-life, its apt repositories now return 404)
FROM debian:bookworm-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    bash \
    id3v2 \
    openjdk-17-jre \
    openjdk-17-jdk \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy necessary files into the container
COPY createFigure.sh /app/createFigure.sh
COPY MKICipher.java /app/MKICipher.java
COPY MKIDecipher.java /app/MKIDecipher.java

# Make the shell script executable
RUN chmod +x /app/createFigure.sh

# Compile Java files
RUN javac MKICipher.java MKIDecipher.java

# Set the entrypoint (optional)
ENTRYPOINT ["/bin/bash", "/app/createFigure.sh"]

