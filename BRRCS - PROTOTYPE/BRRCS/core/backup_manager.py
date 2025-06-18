import os
import shutil
import logging
from datetime import datetime
import glob

class BackupManager:
    """Manages backup operations for Excel files"""
    
    def __init__(self, source_file, backup_dir, max_backups=10):
        """
        Initialize backup manager.
        
        Args:
            source_file (str): Path to the Excel file to backup
            backup_dir (str): Directory to store backups
            max_backups (int): Maximum number of backups to keep
        """
        self.source_file = source_file
        self.backup_dir = backup_dir
        self.max_backups = max_backups
        self.logger = logging.getLogger(__name__)
        
        # Create backup directory if it doesn't exist
        os.makedirs(backup_dir, exist_ok=True)

    def create_backup(self):
        """
        Create a backup of the source file.
        
        Returns:
            tuple: (success, backup_path)
        """
        try:
            if not os.path.exists(self.source_file):
                self.logger.error(f"Source file not found: {self.source_file}")
                return False, None

            # Generate backup filename with timestamp
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            filename = os.path.basename(self.source_file)
            name, ext = os.path.splitext(filename)
            backup_filename = f"{name}_backup_{timestamp}{ext}"
            backup_path = os.path.join(self.backup_dir, backup_filename)

            # Create backup
            shutil.copy2(self.source_file, backup_path)
            self.logger.info(f"Created backup: {backup_path}")

            # Cleanup old backups
            self._cleanup_old_backups()

            return True, backup_path

        except Exception as e:
            self.logger.error(f"Backup failed: {str(e)}")
            return False, None

    def _cleanup_old_backups(self):
        """Remove old backups if exceeding max_backups limit"""
        try:
            # Get list of backup files
            pattern = os.path.join(self.backup_dir, f"{os.path.splitext(os.path.basename(self.source_file))[0]}_backup_*")
            backup_files = glob.glob(pattern)
            
            # Sort by modification time (oldest first)
            backup_files.sort(key=os.path.getmtime)
            
            # Remove oldest backups if exceeding limit
            while len(backup_files) > self.max_backups:
                oldest_backup = backup_files.pop(0)
                os.remove(oldest_backup)
                self.logger.info(f"Removed old backup: {oldest_backup}")

        except Exception as e:
            self.logger.error(f"Backup cleanup failed: {str(e)}")

    def restore_backup(self, backup_path):
        """
        Restore a backup file.
        
        Args:
            backup_path (str): Path to the backup file to restore
            
        Returns:
            bool: True if restore was successful
        """
        try:
            if not os.path.exists(backup_path):
                self.logger.error(f"Backup file not found: {backup_path}")
                return False

            # Create a backup of current file before restore
            self.create_backup()

            # Restore the backup
            shutil.copy2(backup_path, self.source_file)
            self.logger.info(f"Restored backup: {backup_path}")
            return True

        except Exception as e:
            self.logger.error(f"Restore failed: {str(e)}")
            return False

    def list_backups(self):
        """
        List all available backups.
        
        Returns:
            list: List of backup file paths sorted by date (newest first)
        """
        try:
            pattern = os.path.join(self.backup_dir, f"{os.path.splitext(os.path.basename(self.source_file))[0]}_backup_*")
            backup_files = glob.glob(pattern)
            
            # Sort by modification time (newest first)
            backup_files.sort(key=os.path.getmtime, reverse=True)
            
            return backup_files

        except Exception as e:
            self.logger.error(f"Failed to list backups: {str(e)}")
            return [] 