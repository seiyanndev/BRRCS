import tkinter as tk
from tkinter import ttk
import os
from typing import Optional, Dict, Any
from dataclasses import dataclass

@dataclass
class WindowConfig:
    """Configuration for the main window."""
    title: str = "Barangay 6 Resident Records and Certification System"
    width: int = 1200
    height: int = 800
    min_width: int = 800
    min_height: int = 600
    theme: str = "default"
    icon_path: Optional[str] = None

class WindowManager:
    """Manages the main application window and its layout."""
    
    def __init__(self, config: Optional[WindowConfig] = None):
        """
        Initialize the window manager.
        
        Args:
            config (Optional[WindowConfig]): Window configuration
        """
        self.config = config or WindowConfig()
        self.root = tk.Tk()
        self._setup_window()
        self._create_frames()
        self._setup_styles()
        
        # Store references to content frames
        self.content_frames: Dict[str, tk.Frame] = {}
        
        # Bind window events
        self._bind_events()
    
    def _setup_window(self) -> None:
        """Set up the main window properties."""
        # Set window title
        self.root.title(self.config.title)
        
        # Set window size and position
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - self.config.width) // 2
        y = (screen_height - self.config.height) // 2
        self.root.geometry(f"{self.config.width}x{self.config.height}+{x}+{y}")
        
        # Set minimum window size
        self.root.minsize(self.config.min_width, self.config.min_height)
        
        # Set window icon if provided
        if self.config.icon_path and os.path.exists(self.config.icon_path):
            self.root.iconbitmap(self.config.icon_path)
        
        # Configure grid
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
    
    def _create_frames(self) -> None:
        """Create the main layout frames."""
        # Menu Panel (Left)
        self.menu_frame = ttk.Frame(self.root, padding="5")
        self.menu_frame.grid(row=0, column=0, sticky="nsew")
        self.menu_frame.grid_rowconfigure(0, weight=1)
        
        # Content Area (Right)
        self.content_frame = ttk.Frame(self.root, padding="10")
        self.content_frame.grid(row=0, column=1, sticky="nsew")
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)
        
        # Status Bar (Bottom)
        self.status_frame = ttk.Frame(self.root, padding="2")
        self.status_frame.grid(row=1, column=0, columnspan=2, sticky="ew")
        
        # Create status labels
        self.status_text = ttk.Label(self.status_frame, text="Ready")
        self.status_text.pack(side="left", padx=5)
        
        self.status_user = ttk.Label(self.status_frame, text="User: Guest")
        self.status_user.pack(side="right", padx=5)
    
    def _setup_styles(self) -> None:
        """Set up custom styles for widgets."""
        style = ttk.Style()
        
        # Configure menu panel style
        style.configure(
            "Menu.TFrame",
            background="#f0f0f0",
            relief="solid",
            borderwidth=1
        )
        self.menu_frame.configure(style="Menu.TFrame")
        
        # Configure content area style
        style.configure(
            "Content.TFrame",
            background="#ffffff",
            relief="solid",
            borderwidth=1
        )
        self.content_frame.configure(style="Content.TFrame")
        
        # Configure status bar style
        style.configure(
            "Status.TFrame",
            background="#e0e0e0",
            relief="solid",
            borderwidth=1
        )
        self.status_frame.configure(style="Status.TFrame")
        
        # Configure menu buttons
        style.configure(
            "Menu.TButton",
            padding=10,
            font=("Arial", 10)
        )
    
    def _bind_events(self) -> None:
        """Bind window events."""
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Handle window resize
        self.root.bind("<Configure>", self.on_resize)
    
    def create_menu_button(self, text: str, command: callable, **kwargs) -> ttk.Button:
        """
        Create a menu button in the menu panel.
        
        Args:
            text (str): Button text
            command (callable): Function to call when clicked
            **kwargs: Additional button configuration
            
        Returns:
            ttk.Button: The created button
        """
        button = ttk.Button(
            self.menu_frame,
            text=text,
            command=command,
            style="Menu.TButton",
            **kwargs
        )
        button.pack(fill="x", padx=5, pady=2)
        return button
    
    def create_content_frame(self, name: str) -> tk.Frame:
        """
        Create a new content frame.
        
        Args:
            name (str): Unique identifier for the frame
            
        Returns:
            tk.Frame: The created frame
        """
        frame = ttk.Frame(self.content_frame)
        self.content_frames[name] = frame
        return frame
    
    def show_content_frame(self, name: str) -> None:
        """
        Show a specific content frame.
        
        Args:
            name (str): Name of the frame to show
        """
        # Hide all frames
        for frame in self.content_frames.values():
            frame.grid_remove()
        
        # Show requested frame
        if name in self.content_frames:
            self.content_frames[name].grid(row=0, column=0, sticky="nsew")
    
    def set_status(self, text: str) -> None:
        """
        Update the status bar text.
        
        Args:
            text (str): New status text
        """
        self.status_text.configure(text=text)
    
    def set_user(self, username: str) -> None:
        """
        Update the user display in the status bar.
        
        Args:
            username (str): Username to display
        """
        self.status_user.configure(text=f"User: {username}")
    
    def on_closing(self) -> None:
        """Handle window closing."""
        # Add any cleanup code here
        self.root.destroy()
    
    def on_resize(self, event: Any) -> None:
        """
        Handle window resize events.
        
        Args:
            event: The resize event
        """
        # Add any resize handling code here
        pass
    
    def run(self) -> None:
        """Start the main event loop."""
        self.root.mainloop()

def main():
    """Test the window manager."""
    # Create window configuration
    config = WindowConfig(
        title="BRRCS - Test Window",
        width=1024,
        height=768
    )
    
    # Create window manager
    window = WindowManager(config)
    
    # Add some test buttons
    window.create_menu_button("Dashboard", lambda: window.set_status("Dashboard selected"))
    window.create_menu_button("Residents", lambda: window.set_status("Residents selected"))
    window.create_menu_button("Reports", lambda: window.set_status("Reports selected"))
    window.create_menu_button("Settings", lambda: window.set_status("Settings selected"))
    
    # Create a test content frame
    test_frame = window.create_content_frame("test")
    ttk.Label(test_frame, text="Test Content").pack(pady=20)
    
    # Show the test frame
    window.show_content_frame("test")
    
    # Set initial status
    window.set_status("Application started")
    window.set_user("Admin")
    
    # Run the application
    window.run()

if __name__ == "__main__":
    main() 