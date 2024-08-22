#!/bin/bash

# Directory path to delete contents from
DIRECTORY_TO_DELETE="$HOME/projects/database"

# Function to delete contents inside the directory
delete_directory_contents() {
    echo "Deleting contents inside: $DIRECTORY_TO_DELETE"

    # Check if the directory exists
    if [ -d "$DIRECTORY_TO_DELETE" ]; then
        # Loop through each file and subdirectory
        for file in "$DIRECTORY_TO_DELETE"/*; do
            if [ -e "$file" ]; then  # Check if the file exists
                rm -rf "$file"        # Delete the file or directory
                if [ $? -eq 0 ]; then
                    echo "Deleted: $file"
                else
                    echo "Failed to delete: $file. Check permissions or errors."
                    exit 1
                fi
            fi
        done
        echo "Directory contents deleted successfully."
    else
        echo "Directory does not exist: $DIRECTORY_TO_DELETE"
    fi
}

# Call the function to delete directory contents
delete_directory_contents
