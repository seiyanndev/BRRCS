import os
import logging
import msvcrt
import time
from typing import Optional

class FileLocker:
    """Handles file locking and concurrent access checks for Excel files"""
    
    def __init__(self, filepath: str):
        """
        Initialize file locker.
        
        Args:
            filepath (str): Path to the Excel file to monitor
        """
        self.filepath = filepath
        self.lock_file = f"{filepath}.lock"
        self.logger = logging.getLogger(__name__)
        self._lock_handle: Optional[int] = None

    def is_file_locked(self) -> bool:
        """
        Check if the Excel file is currently locked by another process.
        
        Returns:
            bool: True if file is locked, False otherwise
        """
        try:
            # Check if the Excel file exists
            if not os.path.exists(self.filepath):
                return False

            # Try to open the file in exclusive mode
            handle = msvcrt.get_osfhandle(os.open(self.filepath, os.O_RDWR))
            
            # Try to lock the file
            try:
                msvcrt.locking(handle, msvcrt.LK_NBLCK, 1)
                # If we get here, the file is not locked
                msvcrt.locking(handle, msvcrt.LK_UNLCK, 1)
                os.close(handle)
                return False
            except IOError:
                # File is locked
                os.close(handle)
                return True

        except Exception as e:
            self.logger.error(f"Error checking file lock: {e}")
            return True  # Assume locked on error to be safe

    def acquire_lock(self, timeout: int = 5) -> bool:
        """
        Try to acquire a lock on the file.
        
        Args:
            timeout (int): Maximum time to wait for lock in seconds
            
        Returns:
            bool: True if lock was acquired, False otherwise
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            if not self.is_file_locked():
                try:
                    # Create lock file
                    with open(self.lock_file, 'w') as f:
                        f.write(str(os.getpid()))
                    self.logger.info(f"Acquired lock on {self.filepath}")
                    return True
                except Exception as e:
                    self.logger.error(f"Failed to create lock file: {e}")
                    return False
            time.sleep(0.5)  # Wait before retrying
            
        self.logger.warning(f"Could not acquire lock on {self.filepath} after {timeout} seconds")
        return False

    def release_lock(self) -> bool:
        """
        Release the lock on the file.
        
        Returns:
            bool: True if lock was released, False otherwise
        """
        try:
            if os.path.exists(self.lock_file):
                os.remove(self.lock_file)
                self.logger.info(f"Released lock on {self.filepath}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to release lock: {e}")
            return False

    def __enter__(self):
        """Context manager entry"""
        if not self.acquire_lock():
            raise IOError(f"Could not acquire lock on {self.filepath}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.release_lock() 