#!/bin/bash

# createFigureFabaPlus.sh
# Usage: ./createFigureFabaPlus.sh <figure_ID (4 digits)> <source_folder>

# Exit immediately if a command exits with a non-zero status
set -e

# Function to display usage information
usage() {
    echo "Usage: $0 <figure_ID (4 digits)> <source_folder>"
    exit 1
}

# Check if exactly two arguments are provided
if [ "$#" -ne 2 ]; then
    echo "Error: Invalid number of arguments."
    usage
fi

FIGURE_ID="$1"
SOURCE_FOLDER="$2"

# Validate that FIGURE_ID is exactly 4 digits
if ! [[ "$FIGURE_ID" =~ ^[0-9]{4}$ ]]; then
    echo "Error: Figure ID must be exactly 4 digits."
    usage
fi

# Check if SOURCE_FOLDER is a directory
if [ ! -d "$SOURCE_FOLDER" ]; then
    echo "Error: Source folder '$SOURCE_FOLDER' does not exist or is not a directory."
    exit 1
fi

# Define the output directory within the source folder
OUTPUT_DIR="${SOURCE_FOLDER}/K${FIGURE_ID}"
mkdir -p "$OUTPUT_DIR"

# Initialize iterator
iterator=0

# Loop through each mp3 file
for file in "$SOURCE_FOLDER"/*.mp3; do
    # Skip iteration if no mp3 files are found
    if [ ! -e "$file" ]; then
        echo "No MP3 files found in the source folder."
        exit 1
    fi

    # Format iterator as two digits with leading zero if necessary
    ITERATOR=$(printf "%02d" "$iterator")

    # Copy the modified mp3 to the output directory
    cp "$file" "$OUTPUT_DIR/CP${ITERATOR}.faba"

    # Increment the iterator
    iterator=$((iterator + 1))
done

# Create info file
TOTAL_TRACKS=$((iterator))
CHARACTER_DIR="02190530${FIGURE_ID}00"
INFO_JSON="{\"totalTracks\":$TOTAL_TRACKS,\"characterDir\":\"$CHARACTER_DIR\"}"
echo "$INFO_JSON" > "$OUTPUT_DIR/info"

echo "Processing complete. Copy the files from '$OUTPUT_DIR' directory to your Faba box."
