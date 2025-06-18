import tkinter as tk
import logging
import os
from core.config_loader import ConfigLoader
from core.user_auth import UserAuth
from gui.main_window import MainWindow

def setup_logging():
    """Configure logging"""
    log_dir = os.path.join(os.path.dirname(__file__), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(os.path.join(log_dir, 'app.log')),
            logging.StreamHandler()
        ]
    )

def ensure_directories():
    """Ensure required directories exist"""
    base_dir = os.path.dirname(__file__)
    directories = [
        os.path.join(base_dir, 'logs'),
        os.path.join(base_dir, 'data'),
        os.path.join(base_dir, 'backups'),
        os.path.join(base_dir, 'templates')
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def main():
    """Main application entry point"""
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # Ensure required directories exist
        ensure_directories()
        
        # Load configuration
        config_loader = ConfigLoader()
        config = config_loader.load_config()
        
        # Initialize user authentication with users file from config
        users_file = os.path.join(os.path.dirname(__file__), 'data', 'users.json')
        auth = UserAuth(users_file)
        
        # Create root window
        root = tk.Tk()
        
        # Create and run main window
        app = MainWindow(root)
        app.run()
        
    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    main() 