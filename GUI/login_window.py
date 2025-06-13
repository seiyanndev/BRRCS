import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Callable
from FUNCTIONS.user_manager import UserManager

class LoginWindow:
    """Login window for user authentication."""
    
    def __init__(self, on_login: Callable[[str, str], None]):
        """
        Initialize the login window.
        
        Args:
            on_login: Callback function when login is successful
        """
        self.on_login = on_login
        self.user_manager = UserManager()
        
        # Create window
        self.window = tk.Toplevel()
        self.window.title("BRRCS - Login")
        self.window.geometry("400x300")
        self.window.resizable(False, False)
        
        # Center window
        self._center_window()
        
        # Create widgets
        self._create_widgets()
        
        # Configure grid
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_rowconfigure(0, weight=1)
        
        # Make window modal
        self.window.transient()
        self.window.grab_set()
        
        # Bind events
        self._bind_events()
    
    def _center_window(self) -> None:
        """Center the window on the screen."""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")
    
    def _create_widgets(self) -> None:
        """Create the login window widgets."""
        # Main frame
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="BRRCS Login",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Username
        username_frame = ttk.Frame(main_frame)
        username_frame.pack(fill="x", pady=5)
        
        username_label = ttk.Label(username_frame, text="Username:")
        username_label.pack(side="left", padx=(0, 10))
        
        self.username_entry = ttk.Entry(username_frame)
        self.username_entry.pack(side="left", fill="x", expand=True)
        
        # Password
        password_frame = ttk.Frame(main_frame)
        password_frame.pack(fill="x", pady=5)
        
        password_label = ttk.Label(password_frame, text="Password:")
        password_label.pack(side="left", padx=(0, 10))
        
        self.password_entry = ttk.Entry(password_frame, show="•")
        self.password_entry.pack(side="left", fill="x", expand=True)
        
        # Login button
        self.login_button = ttk.Button(
            main_frame,
            text="Login",
            command=self._handle_login
        )
        self.login_button.pack(pady=20)
        
        # Status label
        self.status_label = ttk.Label(
            main_frame,
            text="",
            foreground="red"
        )
        self.status_label.pack(pady=5)
        
        # Set focus to username entry
        self.username_entry.focus()
    
    def _bind_events(self) -> None:
        """Bind window events."""
        # Handle Enter key
        self.window.bind("<Return>", lambda e: self._handle_login())
        
        # Handle Escape key
        self.window.bind("<Escape>", lambda e: self.window.destroy())
        
        # Handle window close
        self.window.protocol("WM_DELETE_WINDOW", self.window.destroy)
    
    def _handle_login(self) -> None:
        """Handle login button click."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        if not username or not password:
            self.status_label.configure(text="Please enter both username and password")
            return
        
        if self.user_manager.authenticate(username, password):
            self.window.destroy()
            self.on_login(username, self.user_manager.get_user_role())
        else:
            self.status_label.configure(text="Invalid username or password")
            self.password_entry.delete(0, tk.END)
            self.password_entry.focus()
    
    def show(self) -> None:
        """Show the login window."""
        self.window.deiconify()
        self.window.wait_window()

def main():
    """Test the login window."""
    def on_login(username: str, role: str):
        print(f"Logged in as {username} ({role})")
    
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    login = LoginWindow(on_login)
    login.show()
    
    root.destroy()

if __name__ == "__main__":
    main() 