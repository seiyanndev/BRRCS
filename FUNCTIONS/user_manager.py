import json
import os
import bcrypt
from typing import Optional, Dict, Any

class UserManager:
    """Manages user authentication and authorization."""
    
    def __init__(self):
        """Initialize the user manager."""
        self.users_file = "DATA/users.json"
        self.current_user: Optional[str] = None
        self._ensure_users_file()
    
    def _ensure_users_file(self) -> None:
        """Ensure the users file exists with default admin user."""
        os.makedirs(os.path.dirname(self.users_file), exist_ok=True)
        
        if not os.path.exists(self.users_file):
            # Create default admin user
            default_admin = {
                "admin": {
                    "password_hash": self._hash_password("admin123"),
                    "role": "admin"
                }
            }
            with open(self.users_file, "w") as f:
                json.dump(default_admin, f, indent=4)
    
    def _hash_password(self, password: str) -> str:
        """
        Hash a password using bcrypt.
        
        Args:
            password: Plain text password
            
        Returns:
            Hashed password
        """
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt).decode()
    
    def _verify_password(self, password: str, hashed: str) -> bool:
        """
        Verify a password against its hash.
        
        Args:
            password: Plain text password
            hashed: Hashed password
            
        Returns:
            True if password matches hash
        """
        return bcrypt.checkpw(password.encode(), hashed.encode())
    
    def authenticate(self, username: str, password: str) -> bool:
        """
        Authenticate a user.
        
        Args:
            username: Username
            password: Password
            
        Returns:
            True if authentication successful
        """
        users = self._load_users()
        if username not in users:
            return False
        
        if self._verify_password(password, users[username]["password_hash"]):
            self.current_user = username
            return True
        
        return False
    
    def get_user_role(self) -> Optional[str]:
        """
        Get the role of the current user.
        
        Returns:
            User role or None if not logged in
        """
        if not self.current_user:
            return None
        
        users = self._load_users()
        return users[self.current_user]["role"]
    
    def _load_users(self) -> Dict[str, Dict[str, Any]]:
        """
        Load users from file.
        
        Returns:
            Dictionary of users
        """
        if not os.path.exists(self.users_file):
            return {}
        
        with open(self.users_file, "r") as f:
            return json.load(f)
    
    def logout(self) -> None:
        """Log out the current user."""
        self.current_user = None 