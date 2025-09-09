import os
import shutil
from datetime import datetime

def backup_database(db_path, backup_dir):
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    backup_file = os.path.join(backup_dir, f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db")
    shutil.copy2(db_path, backup_file)
    print(f"Backup created at: {backup_file}")

if __name__ == "__main__":
    DATABASE_PATH = 'path/to/your/database.db'  # Update with your actual database path
    BACKUP_DIR = 'path/to/your/backup/directory'  # Update with your desired backup directory

    backup_database(DATABASE_PATH, BACKUP_DIR)