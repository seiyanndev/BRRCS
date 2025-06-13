import tkinter as tk
from tkinter import ttk
import os
import sys
from typing import Dict, Optional, Callable
from dataclasses import dataclass
from datetime import datetime

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from FUNCTIONS.user_manager import UserManager
from FUNCTIONS.statistics_manager import StatisticsManager

@dataclass
class ViewConfig:
    """Configuration for a view."""
    title: str
    icon: Optional[str] = None
    requires_auth: bool = True
    required_role: Optional[str] = None

class View(ttk.Frame):
    """Base class for all views."""
    
    def __init__(self, parent: tk.Widget, config: ViewConfig):
        """
        Initialize the view.
        
        Args:
            parent: Parent widget
            config: View configuration
        """
        super().__init__(parent)
        self.config = config
        self._create_widgets()
    
    def _create_widgets(self) -> None:
        """Create the view's widgets."""
        # Override in subclasses
        pass
    
    def show(self) -> None:
        """Show the view."""
        self.pack(fill="both", expand=True)
    
    def hide(self) -> None:
        """Hide the view."""
        self.pack_forget()

class LoginView(View):
    """Login view."""
    
    def __init__(self, parent: tk.Widget, on_login: Callable[[str, str], None]):
        """
        Initialize the login view.
        
        Args:
            parent: Parent widget
            on_login: Callback when login is successful
        """
        super().__init__(
            parent,
            ViewConfig(
                title="Login",
                requires_auth=False
            )
        )
        self.on_login = on_login
        self.user_manager = UserManager()
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure("Login.TFrame", background="#f0f0f0")
        self.style.configure("Login.TLabel", background="#f0f0f0", font=("Segoe UI", 10))
        self.style.configure("LoginTitle.TLabel", background="#f0f0f0", font=("Segoe UI", 24, "bold"))
        self.style.configure("Login.TButton", font=("Segoe UI", 10))
        self.style.configure("Login.TEntry", font=("Segoe UI", 10))
        
        # Set background color
        self.configure(style="Login.TFrame")
    
    def _create_widgets(self) -> None:
        """Create login widgets."""
        # Main container with padding and background
        container = ttk.Frame(self, style="Login.TFrame", padding="40")
        container.place(relx=0.5, rely=0.5, anchor="center")
        
        # Card frame for login form
        card_frame = ttk.Frame(container, style="Login.TFrame")
        card_frame.pack(fill="both", expand=True)
        
        # Logo/Title
        title_label = ttk.Label(
            card_frame,
            text="BRRCS",
            style="LoginTitle.TLabel"
        )
        title_label.pack(pady=(0, 10))
        
        subtitle_label = ttk.Label(
            card_frame,
            text="Barangay 6 Resident Records and Certification System",
            style="Login.TLabel"
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Username
        username_frame = ttk.Frame(card_frame, style="Login.TFrame")
        username_frame.pack(fill="x", pady=5)
        
        username_label = ttk.Label(
            username_frame,
            text="Username",
            style="Login.TLabel"
        )
        username_label.pack(anchor="w", pady=(0, 5))
        
        self.username_entry = ttk.Entry(
            username_frame,
            width=30,
            style="Login.TEntry"
        )
        self.username_entry.pack(fill="x", ipady=5)
        
        # Password
        password_frame = ttk.Frame(card_frame, style="Login.TFrame")
        password_frame.pack(fill="x", pady=5)
        
        password_label = ttk.Label(
            password_frame,
            text="Password",
            style="Login.TLabel"
        )
        password_label.pack(anchor="w", pady=(0, 5))
        
        self.password_entry = ttk.Entry(
            password_frame,
            show="•",
            width=30,
            style="Login.TEntry"
        )
        self.password_entry.pack(fill="x", ipady=5)
        
        # Login button
        button_frame = ttk.Frame(card_frame, style="Login.TFrame")
        button_frame.pack(fill="x", pady=(30, 0))
        
        self.login_button = ttk.Button(
            button_frame,
            text="Sign In",
            style="Login.TButton",
            command=self._handle_login
        )
        self.login_button.pack(fill="x", ipady=5)
        
        # Status label
        self.status_label = ttk.Label(
            card_frame,
            text="",
            foreground="#dc3545",
            style="Login.TLabel"
        )
        self.status_label.pack(pady=(10, 0))
        
        # Bind Enter key to login
        self.username_entry.bind("<Return>", lambda e: self.password_entry.focus())
        self.password_entry.bind("<Return>", lambda e: self._handle_login())
        
        # Set focus to username entry
        self.username_entry.focus()
    
    def _handle_login(self) -> None:
        """Handle login button click."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        if not username or not password:
            self.status_label.configure(text="Please enter both username and password")
            return
        
        if self.user_manager.authenticate(username, password):
            self.on_login(username, self.user_manager.get_user_role())
        else:
            self.status_label.configure(text="Invalid username or password")
            self.password_entry.delete(0, tk.END)
            self.password_entry.focus()

class DashboardView(View):
    """Dashboard view."""
    
    def __init__(self, parent: tk.Widget, main_window=None):
        """Initialize the dashboard view."""
        self.main_window = main_window
        super().__init__(
            parent,
            ViewConfig(
                title="Dashboard",
                icon="📊"
            )
        )
        
        # Initialize statistics manager
        self.stats_manager = StatisticsManager()
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure("Dashboard.TFrame", background="#f0f0f0")
        self.style.configure("Dashboard.TLabel", background="#f0f0f0", font=("Segoe UI", 10))
        self.style.configure("DashboardTitle.TLabel", background="#f0f0f0", font=("Segoe UI", 24, "bold"))
        self.style.configure("DashboardSubtitle.TLabel", background="#f0f0f0", font=("Segoe UI", 12))
        self.style.configure("DashboardCard.TFrame", background="white", relief="solid", borderwidth=1)
        self.style.configure("DashboardCardTitle.TLabel", background="white", font=("Segoe UI", 12, "bold"))
        self.style.configure("DashboardCardValue.TLabel", background="white", font=("Segoe UI", 24, "bold"))
        self.style.configure("DashboardCardSubtitle.TLabel", background="white", font=("Segoe UI", 10))
        self.style.configure("DashboardCardIcon.TLabel", background="white", font=("Segoe UI", 24))
        self.style.configure("RefreshButton.TButton", font=("Segoe UI", 10))
        
        # Set background color
        self.configure(style="Dashboard.TFrame")
        
        # Initialize refresh flag
        self.is_refreshing = False
        
        # Schedule periodic refresh
        self._schedule_refresh()
    
    def _schedule_refresh(self) -> None:
        """Schedule periodic refresh of dashboard data."""
        if not self.is_refreshing:
            self._update_statistics()
            self.after(5000, self._schedule_refresh)  # Refresh every 5 seconds
    
    def _update_statistics(self) -> None:
        """Update statistics display."""
        try:
            self.is_refreshing = True
            # Use the main window's get_resident_count if available
            resident_count = 0
            if self.main_window and hasattr(self.main_window, 'get_resident_count'):
                resident_count = self.main_window.get_resident_count()
            else:
                stats = self.stats_manager.get_statistics()
                resident_count = stats["total_residents"]
            self._animate_value(self.total_residents_value, resident_count)
            self._animate_value(self.new_residencies_value, self.stats_manager.get_statistics()["new_residencies"])
            self._animate_value(self.issued_certificates_value, self.stats_manager.get_statistics()["certificates_today"])
            self._animate_value(self.completed_value, self.stats_manager.get_statistics()["completed_today"])
            current_date = self._get_current_date()
            if hasattr(self, 'date_label'):
                self.date_label.configure(text=current_date)
            if hasattr(self, 'certificates_subtitle'):
                self.certificates_subtitle.configure(text=f"Certificates issued on {current_date}")
        except Exception as e:
            print(f"Error updating statistics: {e}")
        finally:
            self.is_refreshing = False
    
    def _animate_value(self, label: ttk.Label, new_value: int) -> None:
        """
        Animate the transition of a value.
        
        Args:
            label: The label to animate
            new_value: The new value to display
        """
        try:
            current_value = int(label.cget("text"))
            if current_value != new_value:
                # Calculate step size for smooth animation
                step = 1 if new_value > current_value else -1
                
                def update_step():
                    nonlocal current_value
                    if (step > 0 and current_value < new_value) or (step < 0 and current_value > new_value):
                        current_value += step
                        label.configure(text=str(current_value))
                        self.after(50, update_step)
                    else:
                        label.configure(text=str(new_value))
                
                update_step()
        except ValueError:
            # If current value is not a number, just update directly
            label.configure(text=str(new_value))
    
    def _create_widgets(self) -> None:
        """Create dashboard widgets."""
        # Main container with padding
        main_container = ttk.Frame(self, style="Dashboard.TFrame", padding="20")
        main_container.pack(fill="both", expand=True)
        
        # Header section
        header_frame = ttk.Frame(main_container, style="Dashboard.TFrame")
        header_frame.pack(fill="x", pady=(0, 20))
        
        # Welcome message and refresh button container
        welcome_container = ttk.Frame(header_frame, style="Dashboard.TFrame")
        welcome_container.pack(fill="x")
        
        # Welcome message
        welcome_label = ttk.Label(
            welcome_container,
            text="Welcome to BRRCS",
            style="DashboardTitle.TLabel"
        )
        welcome_label.pack(side="left")
        
        # Refresh button
        refresh_button = ttk.Button(
            welcome_container,
            text="🔄 Refresh",
            style="RefreshButton.TButton",
            command=self._update_statistics
        )
        refresh_button.pack(side="right")
        
        # Date label
        self.date_label = ttk.Label(
            header_frame,
            text=self._get_current_date(),
            style="DashboardSubtitle.TLabel"
        )
        self.date_label.pack(anchor="w")
        
        # Statistics cards container
        stats_container = ttk.Frame(main_container, style="Dashboard.TFrame")
        stats_container.pack(fill="x", pady=(0, 20))
        
        # Top row of statistics cards
        top_row = ttk.Frame(stats_container, style="Dashboard.TFrame")
        top_row.pack(fill="x", pady=(0, 10))
        
        # Bottom row of statistics cards
        bottom_row = ttk.Frame(stats_container, style="Dashboard.TFrame")
        bottom_row.pack(fill="x")
        
        # Create statistics cards in 2x2 grid
        self._create_stat_card(top_row, "Total Residents", "👥", "Total registered residents", 0)
        self._create_stat_card(top_row, "New Residencies", "🏠", "New registrations this month", 1)
        self._create_stat_card(bottom_row, "Issued Certificates", "📄", f"Certificates issued on {self._get_current_date()}", 0)
        self._create_stat_card(bottom_row, "Completed Today", "✅", "Tasks completed today", 1)
        
        # Recent activity section
        activity_frame = ttk.Frame(main_container, style="Dashboard.TFrame")
        activity_frame.pack(fill="both", expand=True)
        
        # Activity title
        activity_title = ttk.Label(
            activity_frame,
            text="Recent Activity",
            style="DashboardTitle.TLabel"
        )
        activity_title.pack(anchor="w", pady=(0, 10))
        
        # Activity list
        activity_list = ttk.Frame(activity_frame, style="DashboardCard.TFrame")
        activity_list.pack(fill="both", expand=True)
        
        # Empty state message
        empty_label = ttk.Label(
            activity_list,
            text="No recent activity",
            style="DashboardSubtitle.TLabel"
        )
        empty_label.pack(pady=20)
    
    def _create_stat_card(self, parent: ttk.Frame, title: str, icon: str, subtitle: str, column: int) -> None:
        """
        Create a statistics card.
        
        Args:
            parent: Parent frame
            title: Card title
            icon: Card icon
            subtitle: Card subtitle
            column: Column position
        """
        card = ttk.Frame(parent, style="DashboardCard.TFrame", padding="15")
        card.grid(row=0, column=column, padx=5, sticky="nsew")
        parent.grid_columnconfigure(column, weight=1)
        
        # Icon and title container
        header_frame = ttk.Frame(card, style="DashboardCard.TFrame")
        header_frame.pack(fill="x")
        
        # Icon
        ttk.Label(
            header_frame,
            text=icon,
            style="DashboardCardIcon.TLabel"
        ).pack(side="left", padx=(0, 10))
        
        # Title
        ttk.Label(
            header_frame,
            text=title,
            style="DashboardCardTitle.TLabel"
        ).pack(side="left", fill="x", expand=True)
        
        # Value
        value_label = ttk.Label(
            card,
            text="0",
            style="DashboardCardValue.TLabel"
        )
        value_label.pack(anchor="w", pady=(5, 0))
        
        # Store reference to value label for updates
        if title == "Total Residents":
            self.total_residents_value = value_label
        elif title == "New Residencies":
            self.new_residencies_value = value_label
        elif title == "Issued Certificates":
            self.issued_certificates_value = value_label
            self.certificates_subtitle = ttk.Label(
                card,
                text=subtitle,
                style="DashboardCardSubtitle.TLabel"
            )
            self.certificates_subtitle.pack(anchor="w")
            return
        elif title == "Completed Today":
            self.completed_value = value_label
        
        # Subtitle
        ttk.Label(
            card,
            text=subtitle,
            style="DashboardCardSubtitle.TLabel"
        ).pack(anchor="w")
    
    def _get_current_date(self) -> str:
        """
        Get the current date in a formatted string.
        
        Returns:
            Formatted date string
        """
        return datetime.now().strftime("%A, %B %d, %Y")

class ResidentsView(View):
    """Residents management view."""
    
    def __init__(self, parent: tk.Widget, main_window=None):
        """Initialize the residents view."""
        self.main_window = main_window
        self.style = ttk.Style()  # Ensure style is initialized before any configuration
        super().__init__(
            parent,
            ViewConfig(
                title="Residents",
                icon="👥"
            )
        )
        # Only create widgets if not already created
        if not hasattr(self, 'initialized'):
            self.style.configure("Residents.TFrame", background="#f0f0f0")
            self.style.configure("Residents.TLabel", background="#f0f0f0", font=("Segoe UI", 10))
            self.style.configure("ResidentsTitle.TLabel", background="#f0f0f0", font=("Segoe UI", 24, "bold"))
            self.style.configure("Search.TEntry", font=("Segoe UI", 10))
            self.configure(style="Residents.TFrame")
            self.residents_data = []  # This will be populated from your data source
            self._create_widgets()
            self.initialized = True

    def _create_widgets(self) -> None:
        # Destroy all children before creating new widgets
        for child in self.winfo_children():
            child.destroy()
        # Main container with padding
        main_container = ttk.Frame(self, style="Residents.TFrame", padding="32 24 32 24")
        main_container.pack(fill="both", expand=True)

        # Search + Filter Row
        search_filter_frame = ttk.Frame(main_container, style="Residents.TFrame")
        search_filter_frame.pack(fill="x", pady=(0, 18))
        search_label = ttk.Label(
            search_filter_frame,
            text="🔍 Search:",
            style="Residents.TLabel"
        )
        search_label.pack(side="left", padx=(0, 8))
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self._on_search)
        search_entry = ttk.Entry(
            search_filter_frame,
            textvariable=self.search_var,
            style="Search.TEntry",
            width=32
        )
        search_entry.pack(side="left", padx=(0, 16))
        # Dropdown filter
        filter_label = ttk.Label(
            search_filter_frame,
            text="Filter by:",
            style="Residents.TLabel"
        )
        filter_label.pack(side="left", padx=(0, 6))
        self.filter_var = tk.StringVar(value="All")
        filter_options = ["All", "Age < 30", "Age 30-40", "Age > 40", "Address: Main St", "Address: Oak Ave"]
        filter_dropdown = ttk.Combobox(
            search_filter_frame,
            textvariable=self.filter_var,
            values=filter_options,
            state="readonly",
            width=16
        )
        filter_dropdown.pack(side="left")
        filter_dropdown.bind("<<ComboboxSelected>>", lambda e: self._on_search())

        # Card-like Table Area
        card_frame = ttk.Frame(main_container, style="ResidentsCard.TFrame", padding="16 12 16 12")
        card_frame.pack(fill="both", expand=True)
        columns = ("ID", "First Name", "Last Name", "Age", "Birthday", "Address")
        self.tree = ttk.Treeview(
            card_frame,
            columns=columns,
            show="headings",
            selectmode="browse",
            style="Residents.Treeview"
        )
        self.tree.heading("ID", text="ID")
        self.tree.heading("First Name", text="First Name")
        self.tree.heading("Last Name", text="Last Name")
        self.tree.heading("Age", text="Age")
        self.tree.heading("Birthday", text="Birthday")
        self.tree.heading("Address", text="Address")
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("First Name", width=150)
        self.tree.column("Last Name", width=150)
        self.tree.column("Age", width=50, anchor="center")
        self.tree.column("Birthday", width=100, anchor="center")
        self.tree.column("Address", width=300)
        scrollbar = ttk.Scrollbar(card_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self._load_residents()
        # Style for alternating row colors
        self.tree.tag_configure('oddrow', background='#f9f9f9')
        self.tree.tag_configure('evenrow', background='#e6eaf0')

        # Bind selection event
        self.tree.bind('<<TreeviewSelect>>', self._on_selection_change)

        # Divider above quick actions
        divider = ttk.Separator(main_container, orient="horizontal")
        divider.pack(fill="x", pady=(18, 8))
        # Quick Actions section (modern spacing)
        actions_frame = ttk.Frame(main_container, style="Residents.TFrame")
        actions_frame.pack(fill="x", pady=(0, 0))
        btn_style = {"style": "SidebarButton.TButton", "width": 20}
        add_btn = ttk.Button(actions_frame, text="➕ Add New Resident", command=self._quick_add_resident, **btn_style)
        add_btn.pack(side="left", padx=(0, 12))
        export_btn = ttk.Button(actions_frame, text="⬇️ Export Residents", command=self._quick_export_residents, **btn_style)
        export_btn.pack(side="left", padx=(0, 12))
        self.edit_btn = ttk.Button(actions_frame, text="✏️ Edit Data", command=self._quick_edit_data, state="disabled", **btn_style)
        self.edit_btn.pack(side="left", padx=(0, 12))
        delete_btn = ttk.Button(actions_frame, text="🗑️ Delete Selected", command=self._quick_delete_selected, **btn_style)
        delete_btn.pack(side="left", padx=(0, 0))

        # Modernize styles
        self.style.configure("ResidentsCard.TFrame", background="#ffffff", relief="groove", borderwidth=1)
        self.style.configure("Residents.Treeview", font=("Segoe UI", 10), rowheight=28, borderwidth=0)
        self.style.map("Residents.Treeview", background=[("selected", "#d0e6fa")])

    def _on_selection_change(self, event):
        """Handle selection change in the treeview."""
        selected_items = self.tree.selection()
        if selected_items:
            self.edit_btn.configure(state="normal")
        else:
            self.edit_btn.configure(state="disabled")

    def _quick_edit_data(self):
        """Handle edit data action."""
        selected_items = self.tree.selection()
        if selected_items:
            # Get the selected item's values
            item_values = self.tree.item(selected_items[0])['values']
            self._show_edit_popup(item_values, selected_items[0])

    def _show_edit_popup(self, resident_data, item_id):
        """Show popup window for editing resident data."""
        # Create popup window
        popup = tk.Toplevel(self)
        popup.title("Edit Resident Data")
        popup.geometry("400x500")
        popup.resizable(False, False)
        
        # Make popup modal
        popup.transient(self)
        popup.grab_set()
        
        # Center the popup
        popup.update_idletasks()
        width = popup.winfo_width()
        height = popup.winfo_height()
        x = (popup.winfo_screenwidth() // 2) - (width // 2)
        y = (popup.winfo_screenheight() // 2) - (height // 2)
        popup.geometry(f'{width}x{height}+{x}+{y}')
        
        # Create main frame with padding
        main_frame = ttk.Frame(popup, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="Edit Resident Information",
            font=("Segoe UI", 14, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Create form fields
        fields_frame = ttk.Frame(main_frame)
        fields_frame.pack(fill="both", expand=True)
        
        # Store entry variables
        entry_vars = {}
        
        # Create form fields
        fields = [
            ("First Name", resident_data[1]),
            ("Last Name", resident_data[2]),
            ("Age", resident_data[3]),
            ("Birthday", resident_data[4]),
            ("Address", resident_data[5])
        ]
        
        for i, (label_text, value) in enumerate(fields):
            # Label
            label = ttk.Label(
                fields_frame,
                text=label_text,
                font=("Segoe UI", 10)
            )
            label.grid(row=i, column=0, sticky="w", pady=(10, 5))
            
            # Entry
            var = tk.StringVar(value=value)
            entry_vars[label_text] = var
            entry = ttk.Entry(
                fields_frame,
                textvariable=var,
                width=30,
                font=("Segoe UI", 10)
            )
            entry.grid(row=i, column=1, sticky="ew", pady=(10, 5))
        
        # Configure grid
        fields_frame.grid_columnconfigure(1, weight=1)
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill="x", pady=(20, 0))
        
        def save_changes():
            # Get updated values
            new_values = [
                resident_data[0],  # Keep original ID
                entry_vars["First Name"].get(),
                entry_vars["Last Name"].get(),
                entry_vars["Age"].get(),
                entry_vars["Birthday"].get(),
                entry_vars["Address"].get()
            ]
            
            # Update the tree
            self.tree.item(item_id, values=new_values)
            
            # Update residents_data
            for i, resident in enumerate(self.residents_data):
                if resident[0] == resident_data[0]:
                    self.residents_data[i] = new_values
                    break
            
            # Close popup
            popup.destroy()
        
        # Save button
        save_btn = ttk.Button(
            buttons_frame,
            text="Save Changes",
            command=save_changes,
            style="SidebarButton.TButton"
        )
        save_btn.pack(side="right", padx=(5, 0))
        
        # Cancel button
        cancel_btn = ttk.Button(
            buttons_frame,
            text="Cancel",
            command=popup.destroy,
            style="SidebarButton.TButton"
        )
        cancel_btn.pack(side="right", padx=(5, 0))

    def _load_residents(self) -> None:
        import os
        try:
            import pandas as pd
        except ImportError:
            pd = None
        # Try to load from residents.xlsx
        excel_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'residents.xlsx')
        data_loaded = False
        if pd is not None and os.path.exists(excel_file):
            try:
                df = pd.read_excel(excel_file)
                # Ensure columns exist
                expected_cols = ["First Name", "Last Name", "Age", "Birthday", "Address"]
                if all(col in df.columns for col in expected_cols):
                    self.residents_data = [
                        (str(idx+1), row["First Name"], row["Last Name"], str(row["Age"]), str(row["Birthday"]), row["Address"])
                        for idx, row in df.iterrows()
                    ]
                    data_loaded = True
            except Exception as e:
                print(f"Error loading residents.xlsx: {e}")
        if not data_loaded:
            # Fallback to sample data
            self.residents_data = [
                ("1", "John", "Doe", "25", "1998-05-15", "123 Main St"),
                ("2", "Jane", "Smith", "30", "1993-08-20", "456 Oak Ave"),
                ("3", "Bob", "Johnson", "45", "1978-12-10", "789 Pine Rd"),
            ]
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Add data to table
        for idx, item in enumerate(self.residents_data):
            tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
            self.tree.insert("", "end", values=item, tags=(tag,))
        # After loading residents, trigger dashboard refresh if possible
        if self.main_window and hasattr(self.main_window, 'views') and 'dashboard' in self.main_window.views:
            dashboard = self.main_window.views['dashboard']
            if hasattr(dashboard, '_update_statistics'):
                dashboard._update_statistics()

    def _on_search(self, *args) -> None:
        search_term = self.search_var.get().lower()
        filter_val = self.filter_var.get()
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Filter and add matching items
        for idx, item in enumerate(self.residents_data):
            # Filtering logic
            match = any(search_term in str(value).lower() for value in item)
            if filter_val == "All":
                pass
            elif filter_val == "Age < 30":
                match = match and int(item[3]) < 30
            elif filter_val == "Age 30-40":
                match = match and 30 <= int(item[3]) <= 40
            elif filter_val == "Age > 40":
                match = match and int(item[3]) > 40
            elif filter_val.startswith("Address: "):
                addr = filter_val.split(": ", 1)[1]
                match = match and addr.lower() in item[5].lower()
            if match:
                tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
                self.tree.insert("", "end", values=item, tags=(tag,))

    def _quick_add_resident(self):
        """Handle add new resident action."""
        self._show_add_popup()

    def _show_add_popup(self):
        """Show popup window for adding new resident."""
        # Create popup window
        popup = tk.Toplevel(self)
        popup.title("Add New Resident")
        popup.geometry("400x500")
        popup.resizable(False, False)
        
        # Make popup modal
        popup.transient(self)
        popup.grab_set()
        
        # Center the popup
        popup.update_idletasks()
        width = popup.winfo_width()
        height = popup.winfo_height()
        x = (popup.winfo_screenwidth() // 2) - (width // 2)
        y = (popup.winfo_screenheight() // 2) - (height // 2)
        popup.geometry(f'{width}x{height}+{x}+{y}')
        
        # Create main frame with padding
        main_frame = ttk.Frame(popup, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="Add New Resident",
            font=("Segoe UI", 14, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Create form fields
        fields_frame = ttk.Frame(main_frame)
        fields_frame.pack(fill="both", expand=True)
        
        # Store entry variables
        entry_vars = {}
        
        # Create form fields
        fields = [
            ("First Name", ""),
            ("Last Name", ""),
            ("Age", ""),
            ("Birthday", ""),
            ("Address", "")
        ]
        
        for i, (label_text, value) in enumerate(fields):
            # Label
            label = ttk.Label(
                fields_frame,
                text=label_text,
                font=("Segoe UI", 10)
            )
            label.grid(row=i, column=0, sticky="w", pady=(10, 5))
            
            # Entry
            var = tk.StringVar(value=value)
            entry_vars[label_text] = var
            entry = ttk.Entry(
                fields_frame,
                textvariable=var,
                width=30,
                font=("Segoe UI", 10)
            )
            entry.grid(row=i, column=1, sticky="ew", pady=(10, 5))
        
        # Configure grid
        fields_frame.grid_columnconfigure(1, weight=1)
        
        # Error message label
        error_label = ttk.Label(
            main_frame,
            text="",
            foreground="red",
            font=("Segoe UI", 9)
        )
        error_label.pack(pady=(10, 0))
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill="x", pady=(20, 0))
        
        def validate_and_save():
            # Get values
            first_name = entry_vars["First Name"].get().strip()
            last_name = entry_vars["Last Name"].get().strip()
            age = entry_vars["Age"].get().strip()
            birthday = entry_vars["Birthday"].get().strip()
            address = entry_vars["Address"].get().strip()
            
            # Validate
            if not all([first_name, last_name, age, birthday, address]):
                error_label.configure(text="All fields are required")
                return
            
            try:
                age_num = int(age)
                if age_num <= 0 or age_num > 120:
                    error_label.configure(text="Age must be between 1 and 120")
                    return
            except ValueError:
                error_label.configure(text="Age must be a valid number")
                return
            
            # Generate new ID (max existing ID + 1)
            new_id = str(max([int(r[0]) for r in self.residents_data], default=0) + 1)
            
            # Create new resident data
            new_resident = [new_id, first_name, last_name, age, birthday, address]
            
            try:
                # Save to Excel file
                import os
                from FUNCTIONS.excel_writer import ExcelWriter
                
                excel_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'residents.xlsx')
                if os.path.exists(excel_file):
                    writer = ExcelWriter(excel_file)
                    writer.append_row({
                        'First Name': first_name,
                        'Last Name': last_name,
                        'Age': age_num,
                        'Birthday': birthday,
                        'Address': address
                    })
                    writer.close()
            except Exception as e:
                error_label.configure(text=f"Error saving to Excel: {str(e)}")
                return
            
            # Add to residents_data
            self.residents_data.append(new_resident)
            
            # Add to tree
            tag = 'evenrow' if len(self.residents_data) % 2 == 0 else 'oddrow'
            self.tree.insert("", "end", values=new_resident, tags=(tag,))
            
            # Update statistics if possible
            if self.main_window and hasattr(self.main_window, 'views') and 'dashboard' in self.main_window.views:
                try:
                    from FUNCTIONS.statistics_manager import StatisticsManager
                    import os
                    from datetime import datetime
                    
                    # Ensure DATA directory exists
                    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'DATA')
                    os.makedirs(data_dir, exist_ok=True)
                    
                    # Initialize statistics manager
                    stats_manager = StatisticsManager()
                    
                    # Update total residents
                    stats_manager.increment_total_residents()
                    
                    # Update new residencies for current month
                    current_month = datetime.now().strftime("%Y-%m")
                    if stats_manager.data["new_residencies"]["last_updated"] == current_month:
                        stats_manager.data["new_residencies"]["current_month"] += 1
                    else:
                        stats_manager.data["new_residencies"]["current_month"] = 1
                        stats_manager.data["new_residencies"]["last_updated"] = current_month
                    
                    # Save updated statistics
                    stats_manager._save_data(stats_manager.data)
                    
                    # Update dashboard
                    dashboard = self.main_window.views['dashboard']
                    if hasattr(dashboard, '_update_statistics'):
                        dashboard._update_statistics()
                        
                except Exception as e:
                    print(f"Error updating statistics: {str(e)}")
                    # Continue even if statistics update fails
            
            # Close popup
            popup.destroy()
        
        # Save button
        save_btn = ttk.Button(
            buttons_frame,
            text="Add Resident",
            command=validate_and_save,
            style="SidebarButton.TButton"
        )
        save_btn.pack(side="right", padx=(5, 0))
        
        # Cancel button
        cancel_btn = ttk.Button(
            buttons_frame,
            text="Cancel",
            command=popup.destroy,
            style="SidebarButton.TButton"
        )
        cancel_btn.pack(side="right", padx=(5, 0))

    def _quick_export_residents(self):
        """Handle export residents action."""
        try:
            import os
            from datetime import datetime
            import pandas as pd
            
            # Create export directory if it doesn't exist
            export_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'EXPORTS')
            os.makedirs(export_dir, exist_ok=True)
            
            # Generate filename with current date
            current_date = datetime.now().strftime("%Y-%m-%d")
            filename = f"Residents List {current_date}.xlsx"
            filepath = os.path.join(export_dir, filename)
            
            # Create DataFrame from current table data
            data = []
            for item in self.tree.get_children():
                values = self.tree.item(item)['values']
                data.append({
                    'ID': values[0],
                    'First Name': values[1],
                    'Last Name': values[2],
                    'Age': values[3],
                    'Birthday': values[4],
                    'Address': values[5]
                })
            
            # Create DataFrame and save to Excel
            df = pd.DataFrame(data)
            df.to_excel(filepath, index=False, sheet_name='Residents')
            
            # Show success message
            self._show_export_success(filepath)
            
        except Exception as e:
            self._show_export_error(str(e))

    def _show_export_success(self, filepath):
        """Show success message for export."""
        # Create popup window
        popup = tk.Toplevel(self)
        popup.title("Export Successful")
        popup.geometry("400x150")
        popup.resizable(False, False)
        
        # Make popup modal
        popup.transient(self)
        popup.grab_set()
        
        # Center the popup
        popup.update_idletasks()
        width = popup.winfo_width()
        height = popup.winfo_height()
        x = (popup.winfo_screenwidth() // 2) - (width // 2)
        y = (popup.winfo_screenheight() // 2) - (height // 2)
        popup.geometry(f'{width}x{height}+{x}+{y}')
        
        # Create main frame with padding
        main_frame = ttk.Frame(popup, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        # Success icon and message
        success_frame = ttk.Frame(main_frame)
        success_frame.pack(fill="x", pady=(0, 20))
        
        success_label = ttk.Label(
            success_frame,
            text="✓",
            font=("Segoe UI", 24),
            foreground="green"
        )
        success_label.pack(side="left", padx=(0, 10))
        
        message_frame = ttk.Frame(success_frame)
        message_frame.pack(side="left", fill="x", expand=True)
        
        title_label = ttk.Label(
            message_frame,
            text="Export Successful",
            font=("Segoe UI", 14, "bold")
        )
        title_label.pack(anchor="w")
        
        file_label = ttk.Label(
            message_frame,
            text=f"File saved to:\n{filepath}",
            font=("Segoe UI", 10),
            wraplength=300
        )
        file_label.pack(anchor="w", pady=(5, 0))
        
        # OK button
        ok_btn = ttk.Button(
            main_frame,
            text="OK",
            command=popup.destroy,
            style="SidebarButton.TButton"
        )
        ok_btn.pack(pady=(10, 0))

    def _show_export_error(self, error_message):
        """Show error message for export."""
        # Create popup window
        popup = tk.Toplevel(self)
        popup.title("Export Failed")
        popup.geometry("400x150")
        popup.resizable(False, False)
        
        # Make popup modal
        popup.transient(self)
        popup.grab_set()
        
        # Center the popup
        popup.update_idletasks()
        width = popup.winfo_width()
        height = popup.winfo_height()
        x = (popup.winfo_screenwidth() // 2) - (width // 2)
        y = (popup.winfo_screenheight() // 2) - (height // 2)
        popup.geometry(f'{width}x{height}+{x}+{y}')
        
        # Create main frame with padding
        main_frame = ttk.Frame(popup, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        # Error icon and message
        error_frame = ttk.Frame(main_frame)
        error_frame.pack(fill="x", pady=(0, 20))
        
        error_label = ttk.Label(
            error_frame,
            text="⚠️",
            font=("Segoe UI", 24),
            foreground="red"
        )
        error_label.pack(side="left", padx=(0, 10))
        
        message_frame = ttk.Frame(error_frame)
        message_frame.pack(side="left", fill="x", expand=True)
        
        title_label = ttk.Label(
            message_frame,
            text="Export Failed",
            font=("Segoe UI", 14, "bold")
        )
        title_label.pack(anchor="w")
        
        error_text = ttk.Label(
            message_frame,
            text=f"Error: {error_message}",
            font=("Segoe UI", 10),
            wraplength=300,
            foreground="red"
        )
        error_text.pack(anchor="w", pady=(5, 0))
        
        # OK button
        ok_btn = ttk.Button(
            main_frame,
            text="OK",
            command=popup.destroy,
            style="SidebarButton.TButton"
        )
        ok_btn.pack(pady=(10, 0))

    def _quick_delete_selected(self):
        """Handle delete selected resident action."""
        selected_items = self.tree.selection()
        if not selected_items:
            return
            
        # Get the selected resident's data
        resident_data = self.tree.item(selected_items[0])['values']
        
        # Show confirmation dialog
        if self._show_delete_confirmation(resident_data):
            try:
                # Delete from Excel file
                import os
                from FUNCTIONS.excel_writer import ExcelWriter
                
                excel_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'residents.xlsx')
                if os.path.exists(excel_file):
                    writer = ExcelWriter(excel_file)
                    if not writer.delete_row('First Name', resident_data[1]):
                        raise Exception("Failed to delete resident from Excel file")
                    writer.close()
                
                # Remove from tree
                self.tree.delete(selected_items[0])
                
                # Remove from residents_data
                for i, resident in enumerate(self.residents_data):
                    if resident[0] == resident_data[0]:
                        self.residents_data.pop(i)
                        break
                
                # Update statistics if possible
                if self.main_window and hasattr(self.main_window, 'views') and 'dashboard' in self.main_window.views:
                    dashboard = self.main_window.views['dashboard']
                    if hasattr(dashboard, '_update_statistics'):
                        dashboard._update_statistics()
                
                # Update alternating row colors
                self._update_row_colors()
                
            except Exception as e:
                # Show error message
                self._show_delete_error(str(e))
                return

    def _show_delete_confirmation(self, resident_data):
        """Show confirmation dialog for deleting resident."""
        # Create popup window
        popup = tk.Toplevel(self)
        popup.title("Confirm Deletion")
        popup.geometry("400x200")
        popup.resizable(False, False)
        
        # Make popup modal
        popup.transient(self)
        popup.grab_set()
        
        # Center the popup
        popup.update_idletasks()
        width = popup.winfo_width()
        height = popup.winfo_height()
        x = (popup.winfo_screenwidth() // 2) - (width // 2)
        y = (popup.winfo_screenheight() // 2) - (height // 2)
        popup.geometry(f'{width}x{height}+{x}+{y}')
        
        # Create main frame with padding
        main_frame = ttk.Frame(popup, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        # Warning icon and message
        warning_frame = ttk.Frame(main_frame)
        warning_frame.pack(fill="x", pady=(0, 20))
        
        warning_label = ttk.Label(
            warning_frame,
            text="⚠️",
            font=("Segoe UI", 24)
        )
        warning_label.pack(side="left", padx=(0, 10))
        
        message_frame = ttk.Frame(warning_frame)
        message_frame.pack(side="left", fill="x", expand=True)
        
        title_label = ttk.Label(
            message_frame,
            text="Delete Resident",
            font=("Segoe UI", 14, "bold")
        )
        title_label.pack(anchor="w")
        
        resident_name = f"{resident_data[1]} {resident_data[2]}"
        message_label = ttk.Label(
            message_frame,
            text=f"Are you sure you want to delete {resident_name}?\nThis action cannot be undone.",
            font=("Segoe UI", 10),
            wraplength=300
        )
        message_label.pack(anchor="w", pady=(5, 0))
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill="x", pady=(20, 0))
        
        # Store result
        result = {"confirmed": False}
        
        def confirm():
            result["confirmed"] = True
            popup.destroy()
        
        # Delete button
        delete_btn = ttk.Button(
            buttons_frame,
            text="Delete",
            command=confirm,
            style="Danger.TButton"
        )
        delete_btn.pack(side="right", padx=(5, 0))
        
        # Cancel button
        cancel_btn = ttk.Button(
            buttons_frame,
            text="Cancel",
            command=popup.destroy,
            style="SidebarButton.TButton"
        )
        cancel_btn.pack(side="right", padx=(5, 0))
        
        # Wait for popup to close
        self.wait_window(popup)
        return result["confirmed"]

    def _show_delete_error(self, error_message):
        """Show error message for delete operation."""
        # Create popup window
        popup = tk.Toplevel(self)
        popup.title("Delete Failed")
        popup.geometry("400x150")
        popup.resizable(False, False)
        
        # Make popup modal
        popup.transient(self)
        popup.grab_set()
        
        # Center the popup
        popup.update_idletasks()
        width = popup.winfo_width()
        height = popup.winfo_height()
        x = (popup.winfo_screenwidth() // 2) - (width // 2)
        y = (popup.winfo_screenheight() // 2) - (height // 2)
        popup.geometry(f'{width}x{height}+{x}+{y}')
        
        # Create main frame with padding
        main_frame = ttk.Frame(popup, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        # Error icon and message
        error_frame = ttk.Frame(main_frame)
        error_frame.pack(fill="x", pady=(0, 20))
        
        error_label = ttk.Label(
            error_frame,
            text="⚠️",
            font=("Segoe UI", 24),
            foreground="red"
        )
        error_label.pack(side="left", padx=(0, 10))
        
        message_frame = ttk.Frame(error_frame)
        message_frame.pack(side="left", fill="x", expand=True)
        
        title_label = ttk.Label(
            message_frame,
            text="Delete Failed",
            font=("Segoe UI", 14, "bold")
        )
        title_label.pack(anchor="w")
        
        error_text = ttk.Label(
            message_frame,
            text=f"Error: {error_message}",
            font=("Segoe UI", 10),
            wraplength=300,
            foreground="red"
        )
        error_text.pack(anchor="w", pady=(5, 0))
        
        # OK button
        ok_btn = ttk.Button(
            main_frame,
            text="OK",
            command=popup.destroy,
            style="SidebarButton.TButton"
        )
        ok_btn.pack(pady=(10, 0))

    def _update_row_colors(self):
        """Update alternating row colors after deletion."""
        for idx, item in enumerate(self.tree.get_children()):
            tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
            self.tree.item(item, tags=(tag,))

class UsersView(View):
    """Users management view (admin only)."""
    
    def __init__(self, parent: tk.Widget):
        """Initialize the users view."""
        super().__init__(
            parent,
            ViewConfig(
                title="Users",
                icon="👤",
                required_role="admin"
            )
        )
    
    def _create_widgets(self) -> None:
        """Create users widgets."""
        # Title
        title_label = ttk.Label(
            self,
            text="User Management",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=20)
        
        # Content
        content_frame = ttk.Frame(self, padding="20")
        content_frame.pack(fill="both", expand=True)
        
        # Add users content here
        ttk.Label(
            content_frame,
            text="User management interface will be implemented here",
            font=("Arial", 12)
        ).pack(pady=10)

class SettingsView(View):
    """Settings view (admin only)."""
    
    def __init__(self, parent: tk.Widget):
        """Initialize the settings view."""
        super().__init__(
            parent,
            ViewConfig(
                title="Settings",
                icon="⚙️",
                required_role="admin"
            )
        )
    
    def _create_widgets(self) -> None:
        """Create settings widgets."""
        # Title
        title_label = ttk.Label(
            self,
            text="System Settings",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=20)
        
        # Content
        content_frame = ttk.Frame(self, padding="20")
        content_frame.pack(fill="both", expand=True)
        
        # Add settings content here
        ttk.Label(
            content_frame,
            text="System settings interface will be implemented here",
            font=("Arial", 12)
        ).pack(pady=10)

class MainWindow:
    """Main application window."""
    
    def __init__(self):
        """Initialize the main window."""
        self.root = tk.Tk()
        self.root.title("Barangay 6 Resident Records and Certification System")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # Configure style
        self._setup_styles()
        
        # Center window
        self._center_window()
        
        # Create main layout
        self._create_layout()
        
        # Create views
        self.views: Dict[str, View] = {}
        self._create_views()
        
        # Create status bar
        self._create_status_bar()
        
        # Show login view initially
        self.show_view("login")
    
    def _setup_styles(self) -> None:
        """Set up custom styles for the application."""
        self.style = ttk.Style()
        
        # Configure sidebar styles
        self.style.configure(
            "Sidebar.TFrame",
            background="#2c3e50"
        )
        self.style.configure(
            "Sidebar.TLabel",
            background="#2c3e50",
            foreground="white",
            font=("Segoe UI", 10)
        )
        self.style.configure(
            "SidebarTitle.TLabel",
            background="#2c3e50",
            foreground="white",
            font=("Segoe UI", 16, "bold")
        )
        self.style.configure(
            "SidebarSubtitle.TLabel",
            background="#2c3e50",
            foreground="white",
            font=("Segoe UI", 10)
        )
        self.style.configure(
            "SidebarButton.TButton",
            background="#34495e",
            foreground="black",
            font=("Segoe UI", 10),
            padding=10
        )
        self.style.map(
            "SidebarButton.TButton",
            background=[("active", "#3498db")],
            foreground=[("active", "black")]
        )
        self.style.configure(
            "LogoutButton.TButton",
            background="#c0392b",
            foreground="black",
            font=("Segoe UI", 10),
            padding=10
        )
        self.style.map(
            "LogoutButton.TButton",
            background=[("active", "#e74c3c")],
            foreground=[("active", "black")]
        )
    
    def _center_window(self) -> None:
        """Center the window on the screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def _create_layout(self) -> None:
        """Create the main layout with sidebar and content area."""
        # Main container
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill="both", expand=True)
        
        # Sidebar
        self.sidebar = ttk.Frame(self.main_container, style="Sidebar.TFrame", width=250)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)  # Prevent sidebar from shrinking
        
        # Logo section
        logo_frame = ttk.Frame(self.sidebar, style="Sidebar.TFrame", padding="20")
        logo_frame.pack(fill="x", pady=(20, 0))
        
        # BRRCS Logo (text for now, can be replaced with an image)
        logo_label = ttk.Label(
            logo_frame,
            text="BRRCS",
            style="SidebarTitle.TLabel"
        )
        logo_label.pack()
        
        subtitle_label = ttk.Label(
            logo_frame,
            text="Barangay 6",
            style="Sidebar.TLabel"
        )
        subtitle_label.pack()
        
        # Navigation section
        nav_frame = ttk.Frame(self.sidebar, style="Sidebar.TFrame", padding="10")
        nav_frame.pack(fill="x", pady=20)
        
        # Navigation buttons will be added here when logged in
        self.nav_buttons: Dict[str, ttk.Button] = {}
        
        # Logout section at bottom
        logout_frame = ttk.Frame(self.sidebar, style="Sidebar.TFrame", padding="10")
        logout_frame.pack(side="bottom", fill="x", pady=10)
        
        self.logout_button = ttk.Button(
            logout_frame,
            text="Logout",
            style="LogoutButton.TButton",
            command=lambda: self.show_view("login")
        )
        self.logout_button.pack(fill="x")
        
        # Content area
        self.content_area = ttk.Frame(self.main_container)
        self.content_area.pack(side="right", fill="both", expand=True)
        
        # Hide sidebar initially
        self.sidebar.pack_forget()
    
    def _create_views(self) -> None:
        """Create all views."""
        # Login view
        self.views["login"] = LoginView(
            self.content_area,
            self._handle_login
        )
        
        # Dashboard view
        self.views["dashboard"] = DashboardView(self.content_area, main_window=self)
        
        # Residents view
        self.views["residents"] = ResidentsView(self.content_area, main_window=self)
        
        # Users view (admin only)
        self.views["users"] = UsersView(self.content_area)
        
        # Settings view (admin only)
        self.views["settings"] = SettingsView(self.content_area)
    
    def _create_status_bar(self) -> None:
        """Create the status bar."""
        self.status_frame = ttk.Frame(self.root)
        self.status_frame.pack(fill="x", side="bottom", padx=5, pady=2)
        
        # Status text
        self.status_text = ttk.Label(self.status_frame, text="Ready")
        self.status_text.pack(side="left", padx=5)
        
        # User info
        self.status_user = ttk.Label(self.status_frame, text="User: Guest")
        self.status_user.pack(side="right", padx=5)
    
    def _handle_login(self, username: str, role: str) -> None:
        """
        Handle successful login.
        
        Args:
            username: Username of logged-in user
            role: User role
        """
        # Update status
        self.set_status(f"Welcome, {username}!")
        self.set_user(username)
        
        # Show sidebar
        self.sidebar.pack(side="left", fill="y", before=self.content_area)
        
        # Show dashboard
        self.show_view("dashboard")
        
        # Update navigation
        self._update_navigation(role)
    
    def _update_navigation(self, role: str) -> None:
        # Clear all widgets from the sidebar except the logo/header (first 2 widgets)
        for widget in self.sidebar.pack_slaves()[2:]:
            widget.destroy()
        self.nav_buttons.clear()
        # Add navigation buttons in hierarchical order
        # 1. Dashboard (always first)
        self._add_nav_button("Dashboard", "dashboard", "📊")
        # 2. User Management (admin only)
        if role == "admin":
            self._add_nav_button("Residents", "residents", "👥")
        # 3. Actions (remove Add Resident)
        self._add_nav_button("Issue Certificate", "certificates", "📄")
        self._add_nav_button("View Reports", "reports", "📊")
        # 4. Settings (admin only)
        if role == "admin":
            self._add_nav_button("Settings", "settings", "⚙️")
        # Add separator before logout
        separator = ttk.Separator(self.sidebar, orient="horizontal")
        separator.pack(fill="x", padx=10, pady=10)
        # Logout button (always last)
        logout_button = ttk.Button(
            self.sidebar,
            text="🚪 Logout",
            style="LogoutButton.TButton",
            command=self._handle_logout
        )
        logout_button.pack(side="bottom", fill="x", padx=10, pady=10)
    
    def _add_nav_button(self, text: str, view_name: str, icon: str) -> None:
        """
        Add a navigation button.
        
        Args:
            text: Button text
            view_name: Name of view to show when clicked
            icon: Button icon
        """
        button = ttk.Button(
            self.sidebar,
            text=f"{icon} {text}",
            style="SidebarButton.TButton",
            command=lambda: self.show_view(view_name)
        )
        button.pack(fill="x", padx=10, pady=2)
        self.nav_buttons[view_name] = button
    
    def show_view(self, view_name: str) -> None:
        """
        Show a specific view.
        
        Args:
            view_name: Name of view to show
        """
        # Hide all views
        for view in self.views.values():
            view.hide()
        
        # Show requested view
        if view_name in self.views:
            self.views[view_name].show()
            
            # Hide sidebar for login view
            if view_name == "login":
                self.sidebar.pack_forget()
            elif not self.sidebar.winfo_ismapped():
                self.sidebar.pack(side="left", fill="y", before=self.content_area)
    
    def set_status(self, text: str) -> None:
        """
        Update the status bar text.
        
        Args:
            text: New status text
        """
        self.status_text.configure(text=text)
    
    def set_user(self, username: str) -> None:
        """
        Update the user display in the status bar.
        
        Args:
            username: Username to display
        """
        self.status_user.configure(text=f"User: {username}")
    
    def _handle_logout(self):
        """Handle logout action."""
        self.set_user("Guest")
        self.set_status("Logged out.")
        self.show_view("login")
    
    def run(self) -> None:
        """Start the application."""
        self.root.mainloop()

    def get_resident_count(self):
        residents_view = self.views.get("residents")
        if residents_view and hasattr(residents_view, "residents_data"):
            return len(residents_view.residents_data)
        return 0

def main():
    """Run the application."""
    app = MainWindow()
    app.run()

if __name__ == "__main__":
    main() 