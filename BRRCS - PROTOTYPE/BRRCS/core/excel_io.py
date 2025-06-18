import pandas as pd
import logging
import os
from openpyxl import load_workbook
from datetime import datetime
from .data_model import SchemaValidator
from .backup_manager import BackupManager
from .file_locker import FileLocker

class ExcelIO:
    def __init__(self, filepath):
        self.filepath = filepath
        self.logger = logging.getLogger(__name__)
        self.backup_dir = os.path.join(os.path.dirname(filepath), 'backup')
        self.validator = SchemaValidator()
        self.backup_manager = BackupManager(filepath, self.backup_dir)
        self.file_locker = FileLocker(filepath)

    def load_residents(self):
        """
        Load resident records from the Excel file.
        Returns a pandas DataFrame or None if error occurs.
        """
        if not os.path.exists(self.filepath):
            self.logger.error(f"Excel file not found: {self.filepath}")
            return None

        try:
            # Check if file is locked
            if self.file_locker.is_file_locked():
                self.logger.error(f"Excel file is locked by another process: {self.filepath}")
                return None

            df = pd.read_excel(self.filepath, engine='openpyxl')
            
            # Validate headers
            is_valid, missing_columns = self.validator.validate_headers(df.columns.tolist())
            if not is_valid:
                self.logger.error(f"Invalid Excel structure. Missing columns: {missing_columns}")
                return None
                
            # Validate data types
            is_valid, type_mismatches = self.validator.validate_data_types(df)
            if not is_valid:
                self.logger.error(f"Data type mismatches in columns: {type_mismatches}")
                return None
            
            self.logger.info(f"Loaded {len(df)} resident records from {self.filepath}")
            return df
        except Exception as e:
            self.logger.error(f"Failed to load Excel file: {e}")
            return None

    def save_residents(self, df):
        """
        Save the entire DataFrame to the Excel file.
        Args:
            df (pandas.DataFrame): DataFrame containing resident records
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Validate headers and data types before saving
            is_valid, missing_columns = self.validator.validate_headers(df.columns.tolist())
            if not is_valid:
                self.logger.error(f"Cannot save: Invalid structure. Missing columns: {missing_columns}")
                return False
                
            is_valid, type_mismatches = self.validator.validate_data_types(df)
            if not is_valid:
                self.logger.error(f"Cannot save: Data type mismatches in columns: {type_mismatches}")
                return False

            # Try to acquire lock
            if not self.file_locker.acquire_lock():
                self.logger.error("Could not acquire file lock for saving")
                return False

            try:
                # Create backup before saving
                success, backup_path = self.backup_manager.create_backup()
                if not success:
                    self.logger.error("Failed to create backup before saving")
                    return False
                
                # Save the DataFrame to Excel
                df.to_excel(self.filepath, index=False, engine='openpyxl')
                self.logger.info(f"Saved {len(df)} resident records to {self.filepath}")
                return True
            finally:
                # Always release the lock
                self.file_locker.release_lock()

        except Exception as e:
            self.logger.error(f"Failed to save Excel file: {e}")
            return False

    def update_resident(self, resident_id, updated_data):
        """
        Update a single resident's record.
        Args:
            resident_id: Unique identifier for the resident
            updated_data (dict): Dictionary containing updated fields
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Validate the updated data
            is_valid, errors = self.validator.validate_record(updated_data)
            if not is_valid:
                self.logger.error(f"Invalid update data: {errors}")
                return False

            # Try to acquire lock
            if not self.file_locker.acquire_lock():
                self.logger.error("Could not acquire file lock for update")
                return False

            try:
                # Load current data
                df = self.load_residents()
                if df is None:
                    return False

                # Find and update the resident's record
                mask = df['resident_id'] == resident_id
                if not any(mask):
                    self.logger.error(f"Resident ID {resident_id} not found")
                    return False

                # Update the record
                for key, value in updated_data.items():
                    if key in df.columns:
                        df.loc[mask, key] = value

                # Save changes
                return self.save_residents(df)
            finally:
                # Always release the lock
                self.file_locker.release_lock()

        except Exception as e:
            self.logger.error(f"Failed to update resident record: {e}")
            return False

    def delete_resident(self, resident_id):
        """
        Delete a resident's record.
        Args:
            resident_id: Unique identifier for the resident
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Try to acquire lock
            if not self.file_locker.acquire_lock():
                self.logger.error("Could not acquire file lock for deletion")
                return False

            try:
                # Load current data
                df = self.load_residents()
                if df is None:
                    return False

                # Find and remove the resident's record
                mask = df['resident_id'] == resident_id
                if not any(mask):
                    self.logger.error(f"Resident ID {resident_id} not found")
                    return False

                # Remove the record
                df = df[~mask]

                # Save changes
                return self.save_residents(df)
            finally:
                # Always release the lock
                self.file_locker.release_lock()

        except Exception as e:
            self.logger.error(f"Failed to delete resident record: {e}")
            return False

    def add_resident(self, new_resident_data):
        """
        Add a new resident record.
        Args:
            new_resident_data (dict): Dictionary containing new resident's data
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Validate the new resident data
            is_valid, errors = self.validator.validate_record(new_resident_data)
            if not is_valid:
                self.logger.error(f"Invalid resident data: {errors}")
                return False

            # Try to acquire lock
            if not self.file_locker.acquire_lock():
                self.logger.error("Could not acquire file lock for adding resident")
                return False

            try:
                # Load current data
                df = self.load_residents()
                if df is None:
                    return False

                # Check for duplicate resident_id
                if new_resident_data['resident_id'] in df['resident_id'].values:
                    self.logger.error(f"Resident ID {new_resident_data['resident_id']} already exists")
                    return False

                # Append new record
                df = pd.concat([df, pd.DataFrame([new_resident_data])], ignore_index=True)

                # Save changes
                return self.save_residents(df)
            finally:
                # Always release the lock
                self.file_locker.release_lock()

        except Exception as e:
            self.logger.error(f"Failed to add resident record: {e}")
            return False

    def restore_from_backup(self, backup_path):
        """
        Restore the Excel file from a backup.
        Args:
            backup_path (str): Path to the backup file
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Try to acquire lock
            if not self.file_locker.acquire_lock():
                self.logger.error("Could not acquire file lock for restore")
                return False

            try:
                return self.backup_manager.restore_backup(backup_path)
            finally:
                # Always release the lock
                self.file_locker.release_lock()

        except Exception as e:
            self.logger.error(f"Failed to restore from backup: {e}")
            return False

    def list_backups(self):
        """
        List all available backups.
        Returns:
            list: List of backup file paths sorted by date (newest first)
        """
        return self.backup_manager.list_backups() 