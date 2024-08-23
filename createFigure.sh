#!/bin/bash

# createFigure.sh
# Usage: ./createFigure.sh <figure_ID (3 digits)> <source_folder>

# Exit immediately if a command exits with a non-zero status
set -e

# Function to display usage information
usage() {
    echo "Usage: $0 <figure_ID (3 digits)> <source_folder>"
    exit 1
}

# Check if exactly two arguments are provided
if [ "$#" -ne 2 ]; then
    echo "Error: Invalid number of arguments."
    usage
fi

FIGURE_ID="$1"
SOURCE_FOLDER="$2"

# Validate that FIGURE_ID is exactly 3 digits
if ! [[ "$FIGURE_ID" =~ ^[0-9]{3}$ ]]; then
    echo "Error: Figure ID must be exactly 3 digits."
    usage
fi

# Check if SOURCE_FOLDER is a directory
if [ ! -d "$SOURCE_FOLDER" ]; then
    echo "Error: Source folder '$SOURCE_FOLDER' does not exist or is not a directory."
    exit 1
fi

# Create the output directory named K0<FIGURE_ID>
OUTPUT_DIR="K0${FIGURE_ID}"
mkdir -p "$OUTPUT_DIR"

# Initialize iterator
iterator=1

# Loop through each mp3 file
for file in "$SOURCE_FOLDER"/*.mp3; do
    # Format iterator as two digits with leading zero if necessary
    ITERATOR=$(printf "%02d" "$iterator")

    # Define the new title
    NEW_TITLE="K0${FIGURE_ID}CP${ITERATOR}"

    # Change the mp3 title using id3v2
    # Ensure id3v2 is installed
    if ! command -v id3v2 >/dev/null 2>&1; then
        echo "Error: id3v2 is not installed. Please install it to modify mp3 metadata."
        exit 1
    fi

    # Copy the modified mp3 to the output directory
    cp "$file" "$OUTPUT_DIR/CP${ITERATOR}"
    #Change title
    id3v2 -t "$NEW_TITLE" "$OUTPUT_DIR/CP${ITERATOR}"
    # Cipher the file
    java MKICipher "$OUTPUT_DIR/CP${ITERATOR}"
    #remove source file
    rm "$OUTPUT_DIR/CP${ITERATOR}"

    # Increment the iterator
    iterator=$((iterator + 1))
done

echo "Processing complete. Copy the files from '$OUTPUT_DIR' directory to your Faba box."
