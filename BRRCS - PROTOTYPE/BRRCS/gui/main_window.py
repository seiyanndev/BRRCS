import tkinter as tk
from tkinter import ttk, messagebox
import logging
from .styles import StyleManager
from datetime import datetime
import os
import pandas as pd
import re

class MainWindow:
    """Main application window"""
    
    def __init__(self, root: tk.Tk):
        """
        Initialize the main window.
        
        Args:
            root (tk.Tk): The root window
        """
        self.root = root
        self.logger = logging.getLogger(__name__)
        
        # Configure window
        self.root.title("Barangay 6 Resident Records and Certification System")
        self.root.geometry("1200x800")
        self.root.minsize(900, 600)
        
        # Make window full screen
        self.root.state('zoomed')  # For Windows
        # For Linux/Mac, use: self.root.attributes('-zoomed', True)
        
        # Configure styles
        StyleManager.configure_styles(self.root)
        
        # Create main container
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create layout
        self._create_layout()
        
        # Create status bar
        self._create_status_bar()
        
        self.logger.info("Main window initialized")
    
    def _create_layout(self):
        """Create the main window layout"""
        # Sidebar
        self.sidebar = ttk.Frame(self.main_container, style='Sidebar.TFrame', width=260)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        
        # Logo
        try:
            logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'images', 'logo.png')
            logo_img = tk.PhotoImage(file=logo_path)
            # Make logo smaller
            logo_img = logo_img.subsample(4, 4)  # Increased subsample for smaller size
            logo_label = ttk.Label(self.sidebar, image=logo_img, style='Sidebar.TLabel')
            logo_label.image = logo_img  # Keep a reference to prevent garbage collection
            logo_label.pack(pady=(15, 5), padx=20, anchor='center')
        except Exception as e:
            self.logger.error(f"Error loading logo: {e}")
        
        # App title
        self.header = ttk.Label(self.sidebar, text="BRRCS", style='Sidebar.TLabel', font=StyleManager.FONTS['title'])
        self.header.pack(pady=(5, 0), padx=20, anchor='center')  # Changed to center alignment
        self.subtitle = ttk.Label(self.sidebar, text="Barangay 6", style='Sidebar.TLabel', font=StyleManager.FONTS['heading'])
        self.subtitle.pack(pady=(0, 30), padx=20, anchor='center')  # Changed to center alignment
        # Sidebar buttons
        nav_items = [
            ("\U0001F4CA  Dashboard", self._show_dashboard),
            ("\U0001F465  Residents", self._show_residents),
            ("\U0001F4C4  Issue Certificate", self._generate_certificate),
            ("\U0001F5C3  View Reports", self._show_reports),
            ("\u2699  Settings", self._show_settings)
        ]
        self.sidebar_buttons = []
        for text, command in nav_items:
            btn = ttk.Button(self.sidebar, text=text, style='Sidebar.TButton', command=command)
            btn.pack(fill=tk.X, padx=16, pady=4)
            self.sidebar_buttons.append(btn)
        # Spacer
        ttk.Label(self.sidebar, text="", style='Sidebar.TLabel').pack(expand=True, fill=tk.BOTH)
        # Logout button
        self.logout_btn = ttk.Button(self.sidebar, text="\u23FB  Logout", style='Logout.TButton', command=self._logout)
        self.logout_btn.pack(fill=tk.X, padx=16, pady=16, side=tk.BOTTOM)

        # Main content area
        self.content = ttk.Frame(self.main_container, style='Content.TFrame')
        self.content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self._show_dashboard()
    
    def _create_status_bar(self):
        """Create the status bar"""
        self.status_bar = ttk.Frame(self.root)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_label = ttk.Label(
            self.status_bar,
            text="Welcome, admin!",
            style='Status.TLabel'
        )
        self.status_label.pack(side=tk.LEFT, padx=5)
        
        self.user_label = ttk.Label(
            self.status_bar,
            text="User: admin",
            style='Status.TLabel'
        )
        self.user_label.pack(side=tk.RIGHT, padx=5)
    
    # Navigation methods
    def _show_dashboard(self):
        """Show the dashboard view"""
        self._clear_content()
        
        # Header frame to contain title and refresh button
        header_frame = ttk.Frame(self.content, style='Content.TFrame')
        header_frame.pack(fill=tk.X, padx=30, pady=(30, 0))
        
        # Left side of header (title and date)
        title_frame = ttk.Frame(header_frame, style='Content.TFrame')
        title_frame.pack(side=tk.LEFT)
        
        header = ttk.Label(title_frame, text="Welcome to BRRCS", font=StyleManager.FONTS['title'], foreground=StyleManager.COLORS['navy'], background=StyleManager.COLORS['content_bg'])
        header.pack(anchor='nw')
        
        today = datetime.now().strftime('%A, %B %d, %Y')
        subheader = ttk.Label(title_frame, text=today, font=StyleManager.FONTS['subtitle'], foreground=StyleManager.COLORS['muted'], background=StyleManager.COLORS['content_bg'])
        subheader.pack(anchor='nw', pady=(0, 20))
        
        # Right side of header (refresh button)
        refresh_btn = ttk.Button(header_frame, text="\u21BB  Refresh", style='TButton', command=self._show_dashboard)
        refresh_btn.pack(side=tk.RIGHT, pady=(0, 20))
        
        # Stat cards
        cards_frame = ttk.Frame(self.content, style='Content.TFrame')
        cards_frame.pack(anchor='nw', padx=30, pady=(0, 20), fill=tk.X)
        
        # Get total residents count from self.residents_df if available
        total_residents = len(self.residents_df) if hasattr(self, 'residents_df') and self.residents_df is not None else 0
        card_data = [
            ("\U0001F465", "Total Residents", str(total_residents), "Total registered residents"),
            ("\U0001F3E0", "New Residencies", "0", "New registrations this month"),
            ("\U0001F4C4", "Issued Certificates", "0", "Certificates issued on " + today),
            ("\u2714", "Completed Today", "0", "Tasks completed today")
        ]
        
        for i, (icon, label, number, desc) in enumerate(card_data):
            card = ttk.Frame(cards_frame, style='Card.TFrame')
            card.grid(row=0, column=i, padx=10, ipadx=20, ipady=15, sticky='nsew')
            
            # Icon and label in one row
            icon_frame = ttk.Frame(card, style='Card.TFrame')
            icon_frame.pack(fill=tk.X, padx=15, pady=(15, 5))
            
            icon_label = ttk.Label(icon_frame, text=icon, font=('Segoe UI', 24), background=StyleManager.COLORS['card_bg'])
            icon_label.pack(side=tk.LEFT)
            
            label_label = ttk.Label(icon_frame, text=label, style='CardLabel.TLabel')
            label_label.pack(side=tk.LEFT, padx=(10, 0))
            
            # Number and description
            number_label = ttk.Label(card, text=number, style='CardNumber.TLabel')
            number_label.pack(anchor='nw', padx=15, pady=(5, 0))
            
            desc_label = ttk.Label(card, text=desc, style='CardDesc.TLabel')
            desc_label.pack(anchor='nw', padx=15, pady=(0, 15))
            
            cards_frame.columnconfigure(i, weight=1)
        
        # Recent Activity
        section = ttk.Label(self.content, text="Recent Activity", style='Section.TLabel', font=StyleManager.FONTS['heading'], foreground=StyleManager.COLORS['navy'])
        section.pack(anchor='nw', padx=30, pady=(20, 10))
        
        activity_frame = ttk.Frame(self.content, style='Card.TFrame')
        activity_frame.pack(anchor='nw', padx=30, pady=(0, 20), fill=tk.X, ipadx=20, ipady=15)
        
        activity_label = ttk.Label(activity_frame, text="No recent activity", style='CardDesc.TLabel')
        activity_label.pack(anchor='w', padx=15, pady=15)
    
    def _show_residents(self):
        """Show the residents view"""
        self._clear_content()
        
        # Header Section
        header_frame = ttk.Frame(self.content, style='Content.TFrame')
        header_frame.pack(fill=tk.X, padx=30, pady=(30, 20))
        
        # Title and subtitle
        title_frame = ttk.Frame(header_frame, style='Content.TFrame')
        title_frame.pack(side=tk.LEFT)
        
        header = ttk.Label(title_frame, text="Residents", font=StyleManager.FONTS['title'], foreground=StyleManager.COLORS['navy'], background=StyleManager.COLORS['content_bg'])
        header.pack(anchor='nw')
        
        subtitle = ttk.Label(title_frame, text="Manage resident records", font=StyleManager.FONTS['subtitle'], foreground=StyleManager.COLORS['muted'], background=StyleManager.COLORS['content_bg'])
        subtitle.pack(anchor='nw')
        
        # Action buttons
        button_frame = ttk.Frame(header_frame, style='Content.TFrame')
        button_frame.pack(side=tk.RIGHT)
        
        add_btn = ttk.Button(button_frame, text="\u002B Add Resident", style='TButton', width=15)
        add_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        refresh_btn = ttk.Button(button_frame, text="\u21BB Refresh", style='TButton', width=10)
        refresh_btn.pack(side=tk.LEFT)
        
        # Search and Filter Section
        search_frame = ttk.Frame(self.content, style='Content.TFrame')
        search_frame.pack(fill=tk.X, padx=30, pady=(0, 20))
        
        # Create a unified search and filter bar with border
        search_container = ttk.Frame(search_frame, style='SearchBar.TFrame')
        search_container.pack(fill=tk.X, ipady=20, pady=10)  # Increased ipady and pady for taller bar
        
        # Search section (expand to fill all available space)
        search_section = ttk.Frame(search_container, style='SearchBar.TFrame')
        search_section.pack(side=tk.LEFT, padx=(20, 0), pady=0)
        
        # Add search icon
        search_icon = ttk.Label(search_section, text="\U0001F50D", font=('Segoe UI', 12), 
                              background=StyleManager.COLORS['white'])
        search_icon.pack(side=tk.LEFT, padx=(0, 10), ipady=0)
        
        # Configure modern entry style
        style = ttk.Style()
        style.configure('Modern.TEntry', 
                       fieldbackground=StyleManager.COLORS['white'],
                       foreground=StyleManager.COLORS['text'],
                       borderwidth=0,
                       relief='flat',
                       font=('Segoe UI', 10))
        
        # Make the search entry's height independent (e.g., ipady=14 for a taller field)
        search_entry = ttk.Entry(search_section, style='Modern.TEntry', width=160)  # Ultra-long search bar
        search_entry.pack(side=tk.LEFT, ipady=14, pady=0)
        search_entry.insert(0, "Search residents...")
        
        # Function to clear placeholder text on focus
        def on_focus_in(event):
            if search_entry.get() == "Search residents...":
                search_entry.delete(0, tk.END)
                search_entry.configure(foreground=StyleManager.COLORS['text'])
        
        # Function to restore placeholder text if empty
        def on_focus_out(event):
            if not search_entry.get():
                search_entry.insert(0, "Search residents...")
                search_entry.configure(foreground=StyleManager.COLORS['muted'])
        
        # Bind focus events
        search_entry.bind('<FocusIn>', on_focus_in)
        search_entry.bind('<FocusOut>', on_focus_out)
        
        # Set initial text color to muted
        search_entry.configure(foreground=StyleManager.COLORS['muted'])
        
        # Add a subtle separator
        separator = ttk.Separator(search_container, orient='vertical')
        separator.pack(side=tk.LEFT, padx=20, fill=tk.Y, pady=10)
        
        # Filter section (align to the right)
        filter_section = ttk.Frame(search_container, style='SearchBar.TFrame')
        filter_section.pack(side=tk.RIGHT, padx=(0, 20), pady=0)
        
        # Purok filter (was Age Group)
        purok_container = ttk.Frame(filter_section, style='SearchBar.TFrame')
        purok_container.pack(side=tk.LEFT, padx=(0, 20), pady=0)
        purok_label = ttk.Label(purok_container, text="Purok", style='Filter.TLabel', font=('Segoe UI', 9))
        purok_label.pack(side=tk.LEFT, padx=(0, 8), pady=0)
        purok_combo = ttk.Combobox(purok_container, values=["All", "Purok 1", "Purok 2", "Purok 3", "Purok 4", "Purok 5", "Purok 6", "Purok 7"], width=10, state="readonly", style='Modern.TCombobox')
        purok_combo.pack(side=tk.LEFT, ipady=8, pady=0)
        purok_combo.set("All")
        
        # Gender filter (M/F logic)
        gender_container = ttk.Frame(filter_section, style='SearchBar.TFrame')
        gender_container.pack(side=tk.LEFT, padx=(0, 20), pady=0)
        
        gender_label = ttk.Label(gender_container, text="Gender", style='Filter.TLabel',
                               font=('Segoe UI', 9))
        gender_label.pack(side=tk.LEFT, padx=(0, 8), pady=0)
        
        gender_combo = ttk.Combobox(gender_container, values=["All", "Male", "Female", "Other"], 
                                  width=10, state="readonly", style='Modern.TCombobox')
        gender_combo.pack(side=tk.LEFT, ipady=8, pady=0)
        gender_combo.set("All")
        
        # Civil Status filter (fixed choices, robust column matching)
        civil_status_container = ttk.Frame(filter_section, style='SearchBar.TFrame')
        civil_status_container.pack(side=tk.LEFT, pady=0)
        civil_status_label = ttk.Label(civil_status_container, text="Civil Status", style='Filter.TLabel', font=('Segoe UI', 9))
        civil_status_label.pack(side=tk.LEFT, padx=(0, 8), pady=0)
        civil_status_choices = ["All", "Single", "Married", "Widowed", "Divorced"]
        civil_status_combo = ttk.Combobox(civil_status_container, values=civil_status_choices, width=12, state="readonly", style='Modern.TCombobox')
        civil_status_combo.pack(side=tk.LEFT, ipady=8, pady=0)
        civil_status_combo.set("All")
        
        # Configure the search bar style
        style.configure('SearchBar.TFrame', 
                       background=StyleManager.COLORS['white'],
                       relief='solid',
                       borderwidth=1)
        
        # Configure filter label style
        style.configure('Filter.TLabel',
                       background=StyleManager.COLORS['white'],
                       foreground=StyleManager.COLORS['muted'],
                       font=('Segoe UI', 9))
        
        # Residents Table
        table_frame = ttk.Frame(self.content, style='Card.TFrame')
        table_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 20), ipadx=20, ipady=15)
        # Table header (clean, no border, aligned with table content)
        header_frame = ttk.Frame(table_frame, style='Card.TFrame')
        header_frame.pack(fill=tk.X, padx=0, pady=(0, 0))  # Remove extra padding
        header_label = ttk.Label(header_frame, text="Resident Records", style='CardLabel.TLabel')
        header_label.pack(side=tk.LEFT, padx=(10, 0), pady=(0, 0))  # Align with table content
        count_label = ttk.Label(header_frame, text="", style='CardDesc.TLabel')
        count_label.pack(side=tk.RIGHT, padx=(0, 10), pady=(0, 0))
        # Add a subtle separator below the header
        header_separator = ttk.Separator(table_frame, orient='horizontal')
        header_separator.pack(fill=tk.X, padx=0, pady=(0, 5))
        # Create Treeview with custom style
        style = ttk.Style()
        style.configure("Custom.Treeview", 
                       background=StyleManager.COLORS['card_bg'],
                       foreground=StyleManager.COLORS['text'],
                       rowheight=40,
                       fieldbackground=StyleManager.COLORS['card_bg'])
        style.configure("Custom.Treeview.Heading",
                       foreground="#000000",  # Set column name text color to black
                       font=(StyleManager.FONTS['default'][0], 12, 'bold'),  # Bold and larger font
                       background=StyleManager.COLORS['card_border'])  # Optional: subtle background
        # --- Use a subframe and grid for Treeview and scrollbars ---
        treeview_frame = ttk.Frame(table_frame)
        treeview_frame.pack(fill=tk.BOTH, expand=True)
        # Create Treeview
        tree = ttk.Treeview(treeview_frame, show='headings', style="Custom.Treeview")
        # Add scrollbars
        scrollbar_y = ttk.Scrollbar(treeview_frame, orient=tk.VERTICAL, command=tree.yview)
        scrollbar_x = ttk.Scrollbar(treeview_frame, orient=tk.HORIZONTAL, command=tree.xview)
        tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        # Grid layout
        tree.grid(row=0, column=0, sticky='nsew', padx=(2,0))  # Add small left padding
        scrollbar_y.grid(row=0, column=1, sticky='ns')
        scrollbar_x.grid(row=1, column=0, sticky='ew')
        treeview_frame.rowconfigure(0, weight=1)
        treeview_frame.columnconfigure(0, weight=1)
        
        # --- Residents Table Filtering Logic ---
        # Store the DataFrame for filtering
        self.residents_df = None
        self.residents_tree = None
        self.residents_count_label = None
        def filter_residents(*args):
            if self.residents_df is None:
                return
            df = self.residents_df.copy()
            # Apply flexible search filter (key letters/parts of words)
            search_val = search_entry.get().strip().lower()
            if search_val and search_val != "search residents...":
                search_parts = search_val.split()
                def row_match(row):
                    row_str = ' '.join(row.astype(str)).lower()
                    return all(part in row_str for part in search_parts)
                df = df[df.apply(row_match, axis=1)]
            # Purok filter (robust)
            purok_val = purok_combo.get()
            purok_col = None
            for col in df.columns:
                if col.strip().lower() == 'purok':
                    purok_col = col
                    break
            if purok_val != "All" and purok_col:
                df = df[df[purok_col].astype(str).str.strip().str.lower() == purok_val.strip().lower()]
            # Gender filter (M/F logic)
            gender_val = gender_combo.get()
            gender_col = None
            for col in df.columns:
                if col.strip().lower() == 'gender':
                    gender_col = col
                    break
            if gender_val != "All" and gender_col:
                if gender_val == "Male":
                    df = df[df[gender_col].astype(str).str.upper() == 'M']
                elif gender_val == "Female":
                    df = df[df[gender_col].astype(str).str.upper() == 'F']
                elif gender_val == "Other":
                    df = df[~df[gender_col].astype(str).str.upper().isin(['M', 'F'])]
            # Civil Status filter (fixed choices, robust column matching)
            civil_status_val = civil_status_combo.get()
            civil_col = None
            for col in df.columns:
                col_norm = col.strip().lower().replace('_', '').replace(' ', '')
                if col_norm == 'civilstatus':
                    civil_col = col
                    break
            if civil_status_val != "All" and civil_col:
                df = df[df[civil_col].astype(str).str.strip().str.lower() == civil_status_val.strip().lower()]
            # Update table
            tree = self.residents_tree
            tree.delete(*tree.get_children())
            for item in df.values.tolist():
                tree.insert("", tk.END, values=item)
            if self.residents_count_label:
                self.residents_count_label.config(text=f"{len(df)} records found")
        # --- End Filtering Logic ---

        # Load data from Excel
        excel_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'sample_residents.xlsx')
        try:
            df = pd.read_excel(excel_path)
            self.residents_df = df
            columns = list(df.columns)
            tree['columns'] = columns
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=120, anchor='center')
            data_rows = df.values.tolist()
            for item in data_rows:
                tree.insert("", tk.END, values=item)
            count_label.config(text=f"{len(data_rows)} records found")
            # Store for filtering
            self.residents_tree = tree
            self.residents_count_label = count_label
        except Exception as e:
            tree['columns'] = ["Error"]
            tree.heading("Error", text="Error")
            tree.insert("", tk.END, values=(f"Could not load data: {e}",))
            count_label.config(text="0 records found")
        # Bind search and filter events
        search_entry.bind('<KeyRelease>', lambda e: filter_residents())
        purok_combo.bind('<<ComboboxSelected>>', lambda e: filter_residents())
        gender_combo.bind('<<ComboboxSelected>>', lambda e: filter_residents())
        civil_status_combo.bind('<<ComboboxSelected>>', lambda e: filter_residents())

        # --- Context Menu for Residents Table ---
        def on_right_click(event):
            iid = tree.identify_row(event.y)
            if iid:
                tree.selection_set(iid)
                context_menu.tk_popup(event.x_root, event.y_root)
        context_menu = tk.Menu(tree, tearoff=0, foreground='black', activeforeground='black')
        context_menu.add_command(label="Edit Data", command=lambda: print("Edit Data clicked"))
        context_menu.add_command(label="Issue Certificate", command=lambda: print("Issue Certificate clicked"))
        context_menu.add_command(label="Remove Resident", command=lambda: print("Remove Resident clicked"))
        tree.bind("<Button-3>", on_right_click)
        # --- End Context Menu ---

        # --- Add Resident Button Functionality ---
        def open_add_resident_popup():
            if self.residents_df is None:
                messagebox.showerror("Error", "No resident data loaded.")
                return
            columns = list(self.residents_df.columns)
            popup = tk.Toplevel(self.root)
            popup.title("Add Resident")
            popup.transient(self.root)
            popup.grab_set()
            popup.geometry("900x700")
            popup.resizable(False, False)
            # Center the popup
            popup.update_idletasks()
            x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (popup.winfo_width() // 2)
            y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (popup.winfo_height() // 2)
            popup.geometry(f"+{x}+{y}")
            # Handle X button (window close)
            def on_close():
                popup.destroy()
            popup.protocol("WM_DELETE_WINDOW", on_close)
            # Title label
            title_label = ttk.Label(popup, text="Add New Resident", font=("Segoe UI", 18, "bold"))
            title_label.pack(pady=(30, 10))
            # Separator under title
            title_sep = ttk.Separator(popup, orient='horizontal')
            title_sep.pack(fill=tk.X, padx=40, pady=(0, 20))
            # Card-like form area
            card_frame = tk.Frame(popup, bg="#f8f9fa", bd=1, relief="solid", highlightthickness=0)
            card_frame.pack(padx=40, pady=10, fill=tk.BOTH, expand=True)
            # Entry fields in two columns
            entries = {}
            form_frame = tk.Frame(card_frame, bg="#f8f9fa")
            form_frame.pack(padx=40, pady=30, fill=tk.BOTH, expand=True)
            num_fields = len(columns)
            num_rows = (num_fields + 1) // 2
            for idx, col in enumerate(columns):
                row = idx % num_rows
                col_num = idx // num_rows
                label = ttk.Label(form_frame, text=col+":", anchor='e', font=("Segoe UI", 12), background="#f8f9fa")
                label.grid(row=row, column=col_num*2, sticky='e', pady=12, padx=(0, 10))
                entry = ttk.Entry(form_frame, width=30, font=("Segoe UI", 12))
                entry.grid(row=row, column=col_num*2+1, pady=12, sticky='w')
                entries[col] = entry
                form_frame.columnconfigure(col_num*2+1, weight=1)
            # Save/Cancel buttons with hover effects
            btn_frame = tk.Frame(popup, bg="#f8f9fa")
            btn_frame.pack(pady=30)
            def on_enter(e): e.widget.config(background="#e2e6ea")
            def on_leave(e): e.widget.config(background="#f8f9fa")
            def save_new_resident():
                new_data = {col: entries[col].get().strip() for col in columns}
                # Validation: all fields required
                for col, val in new_data.items():
                    if not val:
                        messagebox.showerror("Validation Error", f"'{col}' cannot be empty.")
                        return
                # Specific validation for Age
                if 'Age' in new_data:
                    try:
                        age_val = int(new_data['Age'])
                        if age_val < 0:
                            raise ValueError
                    except ValueError:
                        messagebox.showerror("Validation Error", "'Age' must be a non-negative integer.")
                        return
                # Specific validation for Contact
                if 'Contact' in new_data:
                    contact_val = new_data['Contact']
                    if not contact_val.isdigit() or len(contact_val) < 7:
                        messagebox.showerror("Validation Error", "'Contact' must be at least 7 digits and contain only numbers.")
                        return
                # Add to DataFrame using pd.concat
                import pandas as pd
                new_row_df = pd.DataFrame([new_data], columns=self.residents_df.columns)
                self.residents_df = pd.concat([self.residents_df, new_row_df], ignore_index=True)
                filter_residents()
                popup.destroy()
            save_btn = tk.Button(btn_frame, text="Save", command=save_new_resident, font=("Segoe UI", 11, "bold"), bg="#f8f9fa", relief="ridge", bd=2, padx=20, pady=7, activebackground="#e2e6ea")
            save_btn.pack(side=tk.LEFT, padx=30)
            save_btn.bind("<Enter>", on_enter)
            save_btn.bind("<Leave>", on_leave)
            cancel_btn = tk.Button(btn_frame, text="Cancel", command=on_close, font=("Segoe UI", 11, "bold"), bg="#f8f9fa", relief="ridge", bd=2, padx=20, pady=7, activebackground="#e2e6ea")
            cancel_btn.pack(side=tk.LEFT, padx=30)
            cancel_btn.bind("<Enter>", on_enter)
            cancel_btn.bind("<Leave>", on_leave)
        add_btn.config(command=open_add_resident_popup)
        # --- End Add Resident Button Functionality ---
    
    def _generate_certificate(self):
        self._clear_content()
        # Header
        header = ttk.Label(self.content, text="Issue Certificates", style='Content.TLabel', font=StyleManager.FONTS['title'], foreground=StyleManager.COLORS['navy'])
        header.pack(anchor='nw', padx=30, pady=(30, 10))
        # Search bar
        search_frame = ttk.Frame(self.content, style='Card.TFrame')
        search_frame.pack(fill=tk.X, padx=30, pady=(0, 20), ipadx=20, ipady=10)
        search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=search_var, width=50, font=('Segoe UI', 10))
        search_entry.pack(side=tk.LEFT, ipady=6, padx=(0, 10))
        search_entry.insert(0, "Search templates...")
        def on_focus_in(event):
            if search_entry.get() == "Search templates...":
                search_entry.delete(0, tk.END)
        def on_focus_out(event):
            if not search_entry.get():
                search_entry.insert(0, "Search templates...")
        search_entry.bind('<FocusIn>', on_focus_in)
        search_entry.bind('<FocusOut>', on_focus_out)
        # Scrollable file-explorer-like area
        explorer_canvas = tk.Canvas(self.content, borderwidth=0, highlightthickness=0, bg=StyleManager.COLORS['card_bg'])
        explorer_scroll = ttk.Scrollbar(self.content, orient="vertical", command=explorer_canvas.yview)
        explorer_frame = ttk.Frame(explorer_canvas, style='Card.TFrame')
        explorer_frame_id = explorer_canvas.create_window((0, 0), window=explorer_frame, anchor='nw')
        def _on_frame_configure(event):
            explorer_canvas.configure(scrollregion=explorer_canvas.bbox("all"))
        explorer_frame.bind("<Configure>", _on_frame_configure)
        explorer_canvas.configure(yscrollcommand=explorer_scroll.set)
        explorer_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=30, pady=(0, 20), ipadx=20, ipady=15)
        explorer_scroll.pack(side=tk.RIGHT, fill=tk.Y, pady=(0, 20))
        # 9 file template cards (no resident names)
        file_templates = [
            {"file_name": "Barangay Clearance"},
            {"file_name": "Certificate of Indigency"},
            {"file_name": "Certificate of Residency"},
            {"file_name": "Certificate of Good Moral"},
            {"file_name": "Certificate of Solo Parent"},
            {"file_name": "Certificate of Unemployment"},
            {"file_name": "Certificate of Low Income"},
            {"file_name": "Certificate of No Property"},
            {"file_name": "Certificate of Barangay Business"},
        ]
        card_widgets = []
        def update_explorer():
            for w in card_widgets:
                w.destroy()
            card_widgets.clear()
            search_text = search_var.get().strip().lower()
            filtered = file_templates
            if search_text and search_text != "search templates...":
                filtered = [f for f in file_templates if search_text in f["file_name"].lower()]
            # Configure grid weights for full expansion
            for r in range((len(filtered) + 2) // 3):
                explorer_frame.rowconfigure(r, weight=1)
            for c in range(3):
                explorer_frame.columnconfigure(c, weight=1)
            for i, file in enumerate(filtered):
                card = ttk.Frame(explorer_frame, style='Card.TFrame', padding=40)
                card.grid(row=i//3, column=i%3, padx=30, pady=30, sticky='nsew')
                # Icon (file-like)
                icon = ttk.Label(card, text="\U0001F4C4", font=('Segoe UI', 64), foreground=StyleManager.COLORS['navy'])
                icon.pack(pady=(30, 20))
                # File/template name
                name_label = ttk.Label(card, text=file["file_name"], font=('Segoe UI', 18, 'bold'))
                name_label.pack(pady=(0, 20))
                # Open/Issue button
                issue_btn = ttk.Button(card, text="Open Template", style='TButton', command=lambda f=file: print(f"Open {f['file_name']}"))
                issue_btn.pack(ipadx=10, ipady=5)
                card_widgets.append(card)
        update_explorer()
        search_var.trace_add('write', lambda *args: update_explorer())
    
    def _show_reports(self):
        self._clear_content()
        label = ttk.Label(self.content, text="Reports View", style='Content.TLabel', font=StyleManager.FONTS['heading'], foreground=StyleManager.COLORS['navy'])
        label.pack(padx=30, pady=30)
    
    def _show_settings(self):
        self._clear_content()
        label = ttk.Label(self.content, text="Settings View", style='Content.TLabel', font=StyleManager.FONTS['heading'], foreground=StyleManager.COLORS['navy'])
        label.pack(padx=30, pady=30)
    
    def _logout(self):
        self.root.quit()
    
    def _clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()
    
    def run(self):
        """Start the main application loop"""
        self.root.mainloop() 