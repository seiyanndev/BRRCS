import os
import time
import threading
import pandas as pd
from datetime import datetime
from FUNCTIONS.file_locker import FileLocker, FileLockInfo, LockState

def create_test_file(file_path: str) -> None:
    """Create a test Excel file."""
    df = pd.DataFrame({
        'First Name': ['John', 'Jane'],
        'Last Name': ['Doe', 'Smith'],
        'Age': [30, 25],
        'Birthday': ['1993-01-01', '1998-01-01']
    })
    df.to_excel(file_path, index=False)

def test_basic_locking():
    """Test basic file locking functionality."""
    test_file = 'test_locking.xlsx'
    create_test_file(test_file)
    
    try:
        # Test single process locking
        locker = FileLocker(test_file)
        
        # Should not be locked initially
        assert not locker.check_lock().is_locked
        
        # Should be able to acquire lock
        assert locker.acquire_lock()
        
        # Should be locked now
        lock_info = locker.check_lock()
        assert lock_info.is_locked
        assert lock_info.locked_by is not None
        assert lock_info.process_id is not None
        assert lock_info.state == LockState.LOCKED
        
        # Should be able to release lock
        assert locker.release_lock()
        
        # Should not be locked after release
        assert not locker.check_lock().is_locked
        
        print("Basic locking test passed!")
        
    finally:
        # Cleanup
        if os.path.exists(test_file):
            os.remove(test_file)
        if os.path.exists(f"{test_file}.lock"):
            os.remove(f"{test_file}.lock")

def test_concurrent_locking():
    """Test concurrent access to the same file."""
    test_file = 'test_concurrent.xlsx'
    create_test_file(test_file)
    
    def worker(worker_id: int, results: list):
        try:
            locker = FileLocker(test_file)
            success = locker.acquire_lock(wait=False)
            results.append((worker_id, success))
            if success:
                time.sleep(1)  # Simulate work
                locker.release_lock()
        except Exception as e:
            results.append((worker_id, str(e)))
    
    try:
        # Create multiple threads trying to access the file
        results = []
        threads = []
        for i in range(3):
            t = threading.Thread(target=worker, args=(i, results))
            threads.append(t)
            t.start()
        
        # Wait for all threads to complete
        for t in threads:
            t.join()
        
        # Check results
        success_count = sum(1 for _, success in results if success is True)
        assert success_count == 1, "Only one thread should acquire the lock"
        
        print("Concurrent locking test passed!")
        
    finally:
        # Cleanup
        if os.path.exists(test_file):
            os.remove(test_file)
        if os.path.exists(f"{test_file}.lock"):
            os.remove(f"{test_file}.lock")

def test_context_manager():
    """Test the context manager functionality."""
    test_file = 'test_context.xlsx'
    create_test_file(test_file)
    
    try:
        # Test context manager
        with FileLocker(test_file) as locker:
            # Should be locked inside context
            assert locker.check_lock().is_locked
            
            # Try to acquire lock in another locker
            other_locker = FileLocker(test_file)
            assert not other_locker.acquire_lock(wait=False)
        
        # Should be unlocked after context
        assert not FileLocker(test_file).check_lock().is_locked
        
        print("Context manager test passed!")
        
    finally:
        # Cleanup
        if os.path.exists(test_file):
            os.remove(test_file)
        if os.path.exists(f"{test_file}.lock"):
            os.remove(f"{test_file}.lock")

def test_stale_lock():
    """Test handling of stale locks."""
    test_file = 'test_stale.xlsx'
    create_test_file(test_file)
    
    try:
        # Create a stale lock
        locker = FileLocker(test_file)
        locker.acquire_lock()
        
        # Modify the lock file to make it stale
        with open(f"{test_file}.lock", 'w') as f:
            f.write(f"pid=999999\n")  # Non-existent PID
            f.write(f"name=test\n")
            f.write(f"username=test\n")
            f.write(f"time={(datetime.now().timestamp() - 3600)}\n")  # 1 hour old
            f.write(f"state=locked\n")
        
        # Should be able to acquire lock despite stale lock
        new_locker = FileLocker(test_file)
        assert new_locker.acquire_lock()
        
        print("Stale lock test passed!")
        
    finally:
        # Cleanup
        if os.path.exists(test_file):
            os.remove(test_file)
        if os.path.exists(f"{test_file}.lock"):
            os.remove(f"{test_file}.lock")

def test_toggle_lock():
    """Test the toggle lock functionality."""
    test_file = 'test_toggle.xlsx'
    create_test_file(test_file)
    
    try:
        locker = FileLocker(test_file)
        
        # Initial state should be unlocked
        assert not locker.check_lock().is_locked
        
        # Toggle to locked
        assert locker.toggle_lock()
        assert locker.check_lock().is_locked
        assert locker.check_lock().state == LockState.LOCKED
        
        # Toggle to unlocked
        assert locker.toggle_lock()
        assert not locker.check_lock().is_locked
        assert locker.check_lock().state == LockState.UNLOCKED
        
        print("Toggle lock test passed!")
        
    finally:
        # Cleanup
        if os.path.exists(test_file):
            os.remove(test_file)
        if os.path.exists(f"{test_file}.lock"):
            os.remove(f"{test_file}.lock")

def test_lock_callbacks():
    """Test the lock state change callbacks."""
    test_file = 'test_callbacks.xlsx'
    create_test_file(test_file)
    
    callback_results = []
    
    def on_lock_change(lock_info: FileLockInfo):
        callback_results.append(lock_info)
    
    try:
        locker = FileLocker(test_file)
        locker.register_callback(on_lock_change)
        
        # Acquire lock
        assert locker.acquire_lock()
        assert len(callback_results) == 1
        assert callback_results[0].is_locked
        assert callback_results[0].state == LockState.LOCKED
        
        # Release lock
        assert locker.release_lock()
        assert len(callback_results) == 2
        assert not callback_results[1].is_locked
        assert callback_results[1].state == LockState.UNLOCKED
        
        # Unregister callback
        locker.unregister_callback(on_lock_change)
        
        # Acquire lock again
        assert locker.acquire_lock()
        assert len(callback_results) == 2  # No new callbacks
        
        print("Lock callbacks test passed!")
        
    finally:
        # Cleanup
        if os.path.exists(test_file):
            os.remove(test_file)
        if os.path.exists(f"{test_file}.lock"):
            os.remove(f"{test_file}.lock")

def test_lock_duration():
    """Test lock duration tracking."""
    test_file = 'test_duration.xlsx'
    create_test_file(test_file)
    
    try:
        locker = FileLocker(test_file)
        
        # Acquire lock
        assert locker.acquire_lock()
        
        # Wait a bit
        time.sleep(1)
        
        # Check duration
        duration = locker.get_lock_duration()
        assert duration is not None
        assert 0.9 <= duration <= 1.1  # Allow small timing variations
        
        # Release lock
        assert locker.release_lock()
        
        # Duration should be None after release
        assert locker.get_lock_duration() is None
        
        print("Lock duration test passed!")
        
    finally:
        # Cleanup
        if os.path.exists(test_file):
            os.remove(test_file)
        if os.path.exists(f"{test_file}.lock"):
            os.remove(f"{test_file}.lock")

def test_auto_release():
    """Test automatic lock release on process exit."""
    test_file = 'test_auto_release.xlsx'
    create_test_file(test_file)
    
    try:
        # Create locker with auto_release=True (default)
        locker = FileLocker(test_file)
        assert locker.acquire_lock()
        
        # Create a new locker to check the lock
        checker = FileLocker(test_file)
        assert checker.check_lock().is_locked
        
        # Simulate process exit
        locker.__exit__(None, None, None)
        
        # Lock should be released
        assert not checker.check_lock().is_locked
        
        print("Auto release test passed!")
        
    finally:
        # Cleanup
        if os.path.exists(test_file):
            os.remove(test_file)
        if os.path.exists(f"{test_file}.lock"):
            os.remove(f"{test_file}.lock")

def main():
    """Run all tests."""
    print("Running file locker tests...")
    
    test_basic_locking()
    test_concurrent_locking()
    test_context_manager()
    test_stale_lock()
    test_toggle_lock()
    test_lock_callbacks()
    test_lock_duration()
    test_auto_release()
    
    print("\nAll tests completed successfully!")

if __name__ == "__main__":
    main() 