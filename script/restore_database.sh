#!/bin/bash

# PostgreSQL Connection Parameters
DB_USER='postgres'
DB_HOST='localhost'
DB_NAME='kayadb'
DB_PORT='5432'
# Path to SQL dump / SQL file
BACKUP_FILE="$HOME/projects/database/kayadb_backup_2024-07-17-10-08-39.dump"

restore_database() {
    echo "Restoring database '$DB_NAME' from '$BACKUP_FILE'..."

    # Check if the backup file exists
    if [ ! -f "$BACKUP_FILE" ]; then
        echo "Backup file not found: $BACKUP_FILE"
        exit 1
    fi

    # Using pg_restore to restore the database
    psql -U $DB_USER -h $DB_HOST -d $DB_NAME -f "$BACKUP_FILE"
    if [ $? -eq 0 ]; then
        echo "Database restore completed successfully."
    else
        echo "Database restore failed. Please check the error messages."
    fi
}

# Call the restore function
restore_database
