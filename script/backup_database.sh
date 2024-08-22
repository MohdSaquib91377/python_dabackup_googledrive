#!/bin/bash

# POSTGRESQL Database backup
DB_USER='postgres'
DB_HOST='localhost'
DB_NAME='kayadb'
DB_PASSWORD='hjdjguye34799biwef923jdbw8r#78('  # Provide your PostgreSQL password here

# Backup directory
BACKUP_DIRECTORY="$HOME/projects/database"

backup_database() {
    timestamp=$(date +"%Y-%m-%d-%H-%M-%S")
    backup_file="$BACKUP_DIRECTORY/${DB_NAME}_backup_$timestamp.dump"

    # Create the backup directory if it doesn't exist
    mkdir -p "$BACKUP_DIRECTORY"

    # Check if the directory was created successfully
    if [ $? -ne 0 ]; then
        echo "Failed to create backup directory: $BACKUP_DIRECTORY"
        exit 1
    fi

    echo "Taking database backup of '$DB_NAME'..."
    PGPASSWORD="$DB_PASSWORD"  pg_dump -U $DB_USER -h $DB_HOST -d $DB_NAME > "$backup_file"

    if [ $? -eq 0 ]; then
        echo "Backup completed successfully: $backup_file"
    else
        echo "Backup failed. Please check the error messages."
    fi
}

# Call the backup function
backup_database
