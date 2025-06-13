import os
import time
import psutil
import threading
from typing import Optional, List, Dict, Callable
from dataclasses import dataclass
from datetime import datetime
import logging
from enum import Enum

class LockState(Enum):
    """Enum for lock states."""
    UNLOCKED = "unlocked"
    LOCKED = "locked"
    PENDING = "pending"
    ERROR = "error"

@dataclass
class FileLockInfo:
    """Information about a file's lock state."""
    is_locked: bool
    state: LockState
    locked_by: Optional[str] = None
    lock_time: Optional[datetime] = None
    process_id: Optional[int] = None
    lock_duration: Optional[float] = None
    retry_count: int = 0

class FileLocker:
    """Manages file access and locking to prevent simultaneous edits."""
    
    def __init__(self, file_path: str, 
                 lock_timeout: int = 300,
                 retry_interval: float = 1.0,
                 max_retries: int = 30,
                 auto_release: bool = True):
        """
        Initialize the file locker.
        
        Args:
            file_path (str): Path to the file to manage
            lock_timeout (int): Timeout in seconds for stale locks
            retry_interval (float): Time between retry attempts
            max_retries (int): Maximum number of retry attempts
            auto_release (bool): Whether to automatically release lock on process exit
        """
        self.file_path = file_path
        self._lock_file = f"{file_path}.lock"
        self._lock_timeout = lock_timeout
        self._lock_retry_interval = retry_interval
        self._max_retries = max_retries
        self._auto_release = auto_release
        self._logger = self._setup_logger()
        self._lock_state = LockState.UNLOCKED
        self._lock_acquired_time = None
        self._lock_callbacks: List[Callable[[FileLockInfo], None]] = []
        
        if auto_release:
            self._register_auto_release()
    
    def _setup_logger(self) -> logging.Logger:
        """Set up logging for the file locker."""
        logger = logging.getLogger('FileLocker')
        logger.setLevel(logging.INFO)
        
        # Create handlers
        c_handler = logging.StreamHandler()
        f_handler = logging.FileHandler('file_locker.log')
        
        # Create formatters
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        c_handler.setFormatter(formatter)
        f_handler.setFormatter(formatter)
        
        # Add handlers
        logger.addHandler(c_handler)
        logger.addHandler(f_handler)
        
        return logger
    
    def _register_auto_release(self) -> None:
        """Register automatic lock release on process exit."""
        def cleanup():
            if self._lock_state == LockState.LOCKED:
                self.release_lock()
        
        import atexit
        atexit.register(cleanup)
    
    def _get_process_info(self, pid: int) -> Dict:
        """Get information about a process."""
        try:
            process = psutil.Process(pid)
            return {
                'pid': pid,
                'name': process.name(),
                'username': process.username(),
                'create_time': datetime.fromtimestamp(process.create_time())
            }
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return {'pid': pid, 'error': 'Process not accessible'}
    
    def _write_lock_file(self, process_info: Dict) -> None:
        """Write lock information to the lock file."""
        with open(self._lock_file, 'w') as f:
            f.write(f"pid={process_info['pid']}\n")
            f.write(f"name={process_info['name']}\n")
            f.write(f"username={process_info['username']}\n")
            f.write(f"time={datetime.now().isoformat()}\n")
            f.write(f"state={self._lock_state.value}\n")
    
    def _read_lock_file(self) -> Optional[Dict]:
        """Read lock information from the lock file."""
        try:
            if not os.path.exists(self._lock_file):
                return None
                
            with open(self._lock_file, 'r') as f:
                lines = f.readlines()
                
            lock_info = {}
            for line in lines:
                key, value = line.strip().split('=', 1)
                lock_info[key] = value
                
            return lock_info
        except Exception as e:
            self._logger.error(f"Error reading lock file: {str(e)}")
            return None
    
    def _is_process_running(self, pid: int) -> bool:
        """Check if a process is still running."""
        try:
            return psutil.pid_exists(pid) and psutil.Process(pid).is_running()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return False
    
    def _is_lock_stale(self, lock_time: str) -> bool:
        """Check if a lock is stale (older than timeout)."""
        try:
            lock_datetime = datetime.fromisoformat(lock_time)
            age = (datetime.now() - lock_datetime).total_seconds()
            return age > self._lock_timeout
        except Exception:
            return True
    
    def _notify_callbacks(self, lock_info: FileLockInfo) -> None:
        """Notify all registered callbacks of lock state changes."""
        for callback in self._lock_callbacks:
            try:
                callback(lock_info)
            except Exception as e:
                self._logger.error(f"Error in lock callback: {str(e)}")
    
    def register_callback(self, callback: Callable[[FileLockInfo], None]) -> None:
        """
        Register a callback function to be called on lock state changes.
        
        Args:
            callback: Function that takes a FileLockInfo parameter
        """
        self._lock_callbacks.append(callback)
    
    def unregister_callback(self, callback: Callable[[FileLockInfo], None]) -> None:
        """
        Unregister a previously registered callback function.
        
        Args:
            callback: Function to unregister
        """
        if callback in self._lock_callbacks:
            self._lock_callbacks.remove(callback)
    
    def check_lock(self) -> FileLockInfo:
        """
        Check if the file is locked.
        
        Returns:
            FileLockInfo: Information about the file's lock state
        """
        lock_info = self._read_lock_file()
        
        if not lock_info:
            return FileLockInfo(is_locked=False, state=LockState.UNLOCKED)
        
        pid = int(lock_info['pid'])
        
        # Check if process is still running
        if not self._is_process_running(pid):
            self._logger.info(f"Lock is stale - process {pid} is not running")
            self.release_lock()
            return FileLockInfo(is_locked=False, state=LockState.UNLOCKED)
        
        # Check if lock is stale
        if self._is_lock_stale(lock_info['time']):
            self._logger.info(f"Lock is stale - older than {self._lock_timeout} seconds")
            self.release_lock()
            return FileLockInfo(is_locked=False, state=LockState.UNLOCKED)
        
        lock_duration = None
        if self._lock_acquired_time:
            lock_duration = (datetime.now() - self._lock_acquired_time).total_seconds()
        
        return FileLockInfo(
            is_locked=True,
            state=LockState(lock_info.get('state', LockState.LOCKED.value)),
            locked_by=lock_info['username'],
            lock_time=datetime.fromisoformat(lock_info['time']),
            process_id=pid,
            lock_duration=lock_duration
        )
    
    def toggle_lock(self, wait: bool = True) -> bool:
        """
        Toggle the lock state of the file.
        
        Args:
            wait (bool): Whether to wait and retry if file is locked
            
        Returns:
            bool: True if lock state was successfully toggled, False otherwise
        """
        current_state = self.check_lock()
        
        if current_state.is_locked:
            return self.release_lock()
        else:
            return self.acquire_lock(wait)
    
    def acquire_lock(self, wait: bool = True) -> bool:
        """
        Try to acquire a lock on the file.
        
        Args:
            wait (bool): Whether to wait and retry if file is locked
            
        Returns:
            bool: True if lock was acquired, False otherwise
        """
        retries = 0
        while True:
            lock_info = self.check_lock()
            
            if not lock_info.is_locked:
                # Create lock file
                process_info = self._get_process_info(os.getpid())
                self._lock_state = LockState.LOCKED
                self._lock_acquired_time = datetime.now()
                self._write_lock_file(process_info)
                self._logger.info(f"Lock acquired by process {os.getpid()}")
                
                # Notify callbacks
                self._notify_callbacks(FileLockInfo(
                    is_locked=True,
                    state=LockState.LOCKED,
                    locked_by=process_info['username'],
                    lock_time=self._lock_acquired_time,
                    process_id=os.getpid()
                ))
                return True
            
            if not wait or retries >= self._max_retries:
                self._logger.warning(f"Could not acquire lock - file is locked by {lock_info.locked_by}")
                return False
            
            self._lock_state = LockState.PENDING
            retries += 1
            time.sleep(self._lock_retry_interval)
    
    def release_lock(self) -> bool:
        """
        Release the lock on the file.
        
        Returns:
            bool: True if lock was released, False otherwise
        """
        try:
            if os.path.exists(self._lock_file):
                os.remove(self._lock_file)
                self._logger.info(f"Lock released by process {os.getpid()}")
                
                # Notify callbacks
                self._notify_callbacks(FileLockInfo(
                    is_locked=False,
                    state=LockState.UNLOCKED,
                    lock_time=self._lock_acquired_time,
                    process_id=os.getpid()
                ))
                
                self._lock_state = LockState.UNLOCKED
                self._lock_acquired_time = None
                return True
            return False
        except Exception as e:
            self._logger.error(f"Error releasing lock: {str(e)}")
            self._lock_state = LockState.ERROR
            return False
    
    def get_locking_processes(self) -> List[Dict]:
        """
        Get information about all processes that might be locking the file.
        
        Returns:
            List[Dict]: List of process information dictionaries
        """
        locking_processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'username', 'open_files']):
            try:
                for file in proc.open_files():
                    if file.path == self.file_path:
                        locking_processes.append({
                            'pid': proc.pid,
                            'name': proc.name(),
                            'username': proc.username(),
                            'create_time': datetime.fromtimestamp(proc.create_time())
                        })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        return locking_processes
    
    def get_lock_duration(self) -> Optional[float]:
        """
        Get the duration of the current lock in seconds.
        
        Returns:
            Optional[float]: Lock duration in seconds, or None if not locked
        """
        if self._lock_acquired_time:
            return (datetime.now() - self._lock_acquired_time).total_seconds()
        return None
    
    def __enter__(self):
        """Context manager entry."""
        if not self.acquire_lock(wait=True):
            raise RuntimeError(f"Could not acquire lock for {self.file_path}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.release_lock() 