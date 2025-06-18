import json
import os
import logging
import bcrypt
from typing import Optional, Dict, List
from dataclasses import dataclass

@dataclass
class User:
    """User data structure"""
    username: str
    role: str
    full_name: str
    is_active: bool = True

class UserAuth:
    """Handles user authentication and access control"""
    
    def __init__(self, users_file: str):
        """
        Initialize user authentication.
        
        Args:
            users_file (str): Path to the JSON file containing user data
        """
        self.users_file = users_file
        self.logger = logging.getLogger(__name__)
        self.current_user: Optional[User] = None
        
        # Create users file if it doesn't exist
        if not os.path.exists(users_file):
            self._create_default_users_file()
    
    def _create_default_users_file(self):
        """Create default users file with admin account"""
        default_users = {
            "admin": {
                "password": self._hash_password("admin123"),
                "role": "admin",
                "full_name": "System Administrator",
                "is_active": True
            }
        }
        
        try:
            with open(self.users_file, 'w') as f:
                json.dump(default_users, f, indent=4)
            self.logger.info("Created default users file with admin account")
        except Exception as e:
            self.logger.error(f"Failed to create users file: {e}")
            raise
    
    def _hash_password(self, password: str) -> str:
        """Hash a password using bcrypt"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def _verify_password(self, password: str, hashed: str) -> bool:
        """Verify a password against its hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    def _load_users(self) -> Dict:
        """Load users from JSON file"""
        try:
            with open(self.users_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Failed to load users file: {e}")
            return {}
    
    def _save_users(self, users: Dict):
        """Save users to JSON file"""
        try:
            with open(self.users_file, 'w') as f:
                json.dump(users, f, indent=4)
        except Exception as e:
            self.logger.error(f"Failed to save users file: {e}")
            raise
    
    def login(self, username: str, password: str) -> bool:
        """
        Authenticate a user.
        
        Args:
            username (str): Username
            password (str): Password
            
        Returns:
            bool: True if authentication successful
        """
        users = self._load_users()
        
        if username not in users:
            self.logger.warning(f"Login failed: User {username} not found")
            return False
            
        user_data = users[username]
        
        if not user_data['is_active']:
            self.logger.warning(f"Login failed: User {username} is inactive")
            return False
            
        if not self._verify_password(password, user_data['password']):
            self.logger.warning(f"Login failed: Invalid password for user {username}")
            return False
            
        self.current_user = User(
            username=username,
            role=user_data['role'],
            full_name=user_data['full_name'],
            is_active=user_data['is_active']
        )
        
        self.logger.info(f"User {username} logged in successfully")
        return True
    
    def logout(self):
        """Log out the current user"""
        if self.current_user:
            self.logger.info(f"User {self.current_user.username} logged out")
            self.current_user = None
    
    def get_current_user(self) -> Optional[User]:
        """Get the currently logged in user"""
        return self.current_user
    
    def add_user(self, username: str, password: str, role: str, full_name: str) -> bool:
        """
        Add a new user.
        
        Args:
            username (str): Username
            password (str): Password
            role (str): User role
            full_name (str): User's full name
            
        Returns:
            bool: True if user was added successfully
        """
        users = self._load_users()
        
        if username in users:
            self.logger.error(f"Failed to add user: Username {username} already exists")
            return False
            
        users[username] = {
            "password": self._hash_password(password),
            "role": role,
            "full_name": full_name,
            "is_active": True
        }
        
        try:
            self._save_users(users)
            self.logger.info(f"Added new user: {username}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to add user: {e}")
            return False
    
    def update_user(self, username: str, **kwargs) -> bool:
        """
        Update user information.
        
        Args:
            username (str): Username to update
            **kwargs: Fields to update (password, role, full_name, is_active)
            
        Returns:
            bool: True if update was successful
        """
        users = self._load_users()
        
        if username not in users:
            self.logger.error(f"Failed to update user: Username {username} not found")
            return False
            
        if 'password' in kwargs:
            kwargs['password'] = self._hash_password(kwargs['password'])
            
        users[username].update(kwargs)
        
        try:
            self._save_users(users)
            self.logger.info(f"Updated user: {username}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to update user: {e}")
            return False
    
    def delete_user(self, username: str) -> bool:
        """
        Delete a user.
        
        Args:
            username (str): Username to delete
            
        Returns:
            bool: True if deletion was successful
        """
        users = self._load_users()
        
        if username not in users:
            self.logger.error(f"Failed to delete user: Username {username} not found")
            return False
            
        del users[username]
        
        try:
            self._save_users(users)
            self.logger.info(f"Deleted user: {username}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to delete user: {e}")
            return False
    
    def list_users(self) -> List[User]:
        """
        List all users.
        
        Returns:
            List[User]: List of User objects
        """
        users = self._load_users()
        return [
            User(
                username=username,
                role=data['role'],
                full_name=data['full_name'],
                is_active=data['is_active']
            )
            for username, data in users.items()
        ] 