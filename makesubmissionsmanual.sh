#!/bin/bash

# Define the paths to your input and output folders
input_folder="submissions"
output_folder="submissions-manual"

# Create the output folder if it doesn't exist
mkdir -p "$output_folder"

# Loop through each zip file in the input folder
for zip_file in "$input_folder"/*.zip; do
    if [ -f "$zip_file" ]; then
        # Get the base name of the zip file (excluding the .zip extension)
        folder_name="$(basename -- "$zip_file" .zip)"

        # Create a folder for the extracted contents
        mkdir -p "$output_folder/$folder_name"

        # Extract the contents of the zip file into the corresponding folder
        unzip -q "$zip_file" -d "$output_folder/$folder_name"

        echo "Extracted: $zip_file"
    fi
done

echo "Extraction completed."
