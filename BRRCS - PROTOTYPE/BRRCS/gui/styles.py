import tkinter as tk
from tkinter import ttk
import os

class StyleManager:
    """Manages the application's visual style and theme"""
    
    # Screenshot-inspired color palette
    COLORS = {
        'navy': '#223047',           # Sidebar navy
        'sidebar': '#223047',        # Sidebar
        'sidebar_active': '#F5F6FA', # Active/hover sidebar button
        'sidebar_border': '#E5E9F0', # Sidebar button border
        'sidebar_text': '#FFFFFF',   # Sidebar text
        'sidebar_icon': '#000000',   # Sidebar icon (if using black)
        'content_bg': '#F5F6FA',     # Main content background
        'card_bg': '#FFFFFF',        # Card background
        'card_border': '#E5E9F0',    # Card border
        'card_icon': '#000000',      # Card icon
        'header': '#000000',         # Main header text
        'subheader': '#223047',      # Subheader text
        'text': '#000000',           # Main text
        'muted': '#7F8C8D',          # Muted/secondary text
        'accent': '#E5E9F0',         # Accent/border
        'button_bg': '#F5F6FA',      # Button background
        'button_fg': '#223047',      # Button text
        'button_border': '#E5E9F0',  # Button border
        'button_hover': '#E5E9F0',   # Button hover
        'logout_bg': '#F5F6FA',      # Logout button
        'logout_border': '#E74C3C',  # Logout border
        'status_bg': '#F5F6FA',      # Status bar
        'status_text': '#223047',    # Status text
        'white': '#FFFFFF',          # White (for entries, etc.)
        'dark': '#223047',           # For tooltips, etc.
        'text_dark': '#223047',      # For tooltips, etc.
    }
    
    # Modern fonts
    FONTS = {
        'default': ('Segoe UI', 10),
        'heading': ('Segoe UI', 12, 'bold'),
        'title': ('Segoe UI', 22, 'bold'),
        'subtitle': ('Segoe UI', 12),
        'card_number': ('Segoe UI', 18, 'bold'),
        'card_label': ('Segoe UI', 11, 'bold'),
        'card_desc': ('Segoe UI', 9),
        'button': ('Segoe UI', 10),
        'menu': ('Segoe UI', 10),
        'status': ('Segoe UI', 9),
        'sidebar': ('Segoe UI', 11, 'bold'),
        'sidebar_button': ('Segoe UI', 10),
    }
    
    @classmethod
    def configure_styles(cls, root: tk.Tk):
        """
        Configure the application's visual styles.
        
        Args:
            root (tk.Tk): The root window
        """
        style = ttk.Style()
        
        # Configure the theme
        if os.name == 'nt':  # Windows
            style.theme_use('vista')
        else:  # Linux/Mac
            style.theme_use('clam')
        
        # Configure common styles
        style.configure('TFrame', background=cls.COLORS['content_bg'])
        style.configure('TLabel', 
                       background=cls.COLORS['content_bg'],
                       foreground=cls.COLORS['text'],
                       font=cls.FONTS['default'])
        
        # Configure sidebar styles
        style.configure('Sidebar.TFrame',
                       background=cls.COLORS['sidebar'],
                       relief='flat',
                       width=250)
        
        style.configure('Sidebar.TLabel',
                       background=cls.COLORS['sidebar'],
                       foreground=cls.COLORS['sidebar_text'],
                       font=cls.FONTS['sidebar'])
        
        style.configure('Sidebar.TButton',
                       background=cls.COLORS['sidebar'],
                       foreground='#000000',
                       font=cls.FONTS['sidebar_button'],
                       padding=(20, 12),
                       relief='flat',
                       width=20)
        
        style.map('Sidebar.TButton',
                 background=[('active', cls.COLORS['sidebar_active']),
                           ('disabled', cls.COLORS['muted'])],
                 foreground=[('active', cls.COLORS['sidebar_text'])])
        
        # Configure content styles
        style.configure('Content.TFrame',
                       background=cls.COLORS['content_bg'],
                       relief='flat')
        
        style.configure('Content.TLabel',
                       background=cls.COLORS['content_bg'],
                       foreground=cls.COLORS['text'],
                       font=cls.FONTS['default'])
        
        # Configure button styles
        style.configure('TButton',
                       background=cls.COLORS['button_bg'],
                       foreground=cls.COLORS['button_fg'],
                       font=cls.FONTS['button'],
                       padding=5)
        
        style.map('TButton',
                 background=[('active', cls.COLORS['button_hover']),
                           ('disabled', cls.COLORS['muted'])])
        
        # Configure entry styles
        style.configure('TEntry',
                       fieldbackground=cls.COLORS['white'],
                       foreground=cls.COLORS['text'],
                       font=cls.FONTS['default'],
                       padding=5,
                       borderwidth=1)
        
        # Configure combobox styles
        style.configure('TCombobox',
                       background=cls.COLORS['white'],
                       foreground=cls.COLORS['text'],
                       font=cls.FONTS['default'],
                       padding=5,
                       borderwidth=1)
        
        # Configure treeview styles
        style.configure('Treeview',
                       background=cls.COLORS['white'],
                       foreground=cls.COLORS['text'],
                       fieldbackground=cls.COLORS['white'],
                       font=cls.FONTS['default'],
                       rowheight=25)
        
        style.configure('Treeview.Heading',
                       background=cls.COLORS['navy'],
                       foreground=cls.COLORS['sidebar_text'],
                       font=cls.FONTS['default'],
                       relief='flat')
        
        # Configure notebook (tab) styles
        style.configure('TNotebook',
                       background=cls.COLORS['content_bg'],
                       tabmargins=[2, 5, 2, 0])
        
        style.configure('TNotebook.Tab',
                       background=cls.COLORS['content_bg'],
                       foreground=cls.COLORS['sidebar_text'],
                       padding=[10, 2],
                       font=cls.FONTS['default'])
        
        style.map('TNotebook.Tab',
                 background=[('selected', cls.COLORS['navy'])],
                 foreground=[('selected', cls.COLORS['sidebar_text'])])
        
        # Configure scrollbar styles
        style.configure('TScrollbar',
                       background=cls.COLORS['content_bg'],
                       arrowcolor=cls.COLORS['text_dark'],
                       troughcolor=cls.COLORS['content_bg'],
                       width=12,
                       relief='flat')
        
        # Configure menu styles
        root.option_add('*Menu.background', cls.COLORS['white'])
        root.option_add('*Menu.foreground', cls.COLORS['text_dark'])
        root.option_add('*Menu.font', cls.FONTS['menu'])
        root.option_add('*Menu.activeBackground', cls.COLORS['sidebar_active'])
        root.option_add('*Menu.activeForeground', cls.COLORS['sidebar_text'])
        
        # Configure status bar style
        style.configure('Status.TLabel',
                       background=cls.COLORS['status_bg'],
                       foreground=cls.COLORS['status_text'],
                       font=cls.FONTS['status'],
                       padding=5)
        
        # Configure search bar style
        style.configure('Search.TEntry',
                       fieldbackground=cls.COLORS['white'],
                       foreground=cls.COLORS['text_dark'],
                       font=cls.FONTS['default'],
                       padding=5,
                       borderwidth=1)
        
        # Configure tooltip style
        style.configure('Tooltip.TLabel',
                       background=cls.COLORS['dark'],
                       foreground=cls.COLORS['sidebar_text'],
                       font=cls.FONTS['default'],
                       padding=5)
        
        # Configure section header style
        style.configure('Section.TLabel',
                       background=cls.COLORS['sidebar'],
                       foreground=cls.COLORS['sidebar_text'],
                       font=cls.FONTS['heading'])
        
        # Sidebar
        style.configure('Sidebar.TFrame', background=cls.COLORS['sidebar'], width=250)
        style.configure('Sidebar.TLabel', background=cls.COLORS['sidebar'], foreground=cls.COLORS['sidebar_text'], font=cls.FONTS['sidebar'])
        style.configure('Sidebar.TButton', background=cls.COLORS['sidebar'], foreground='#000000', font=cls.FONTS['sidebar_button'], borderwidth=0, relief='flat', anchor='w', padding=(20, 12))
        style.map('Sidebar.TButton', background=[('active', cls.COLORS['sidebar_active'])], foreground=[('active', cls.COLORS['sidebar'])])
        # Active/selected sidebar button
        style.configure('SidebarActive.TButton', background=cls.COLORS['sidebar_active'], foreground='#000000', font=cls.FONTS['sidebar_button'], borderwidth=2, relief='flat', anchor='w', padding=(20, 12))
        # Logout button
        style.configure('Logout.TButton', background=cls.COLORS['logout_bg'], foreground=cls.COLORS['sidebar'], font=cls.FONTS['sidebar_button'], borderwidth=1, relief='flat', anchor='center', padding=(20, 12))
        style.map('Logout.TButton', bordercolor=[('active', cls.COLORS['logout_border'])])
        # Content
        style.configure('Content.TFrame', background=cls.COLORS['content_bg'])
        style.configure('Content.TLabel', background=cls.COLORS['content_bg'], foreground=cls.COLORS['text'], font=cls.FONTS['default'])
        # Card
        style.configure('Card.TFrame', background=cls.COLORS['card_bg'], borderwidth=1, relief='solid', padding=(20, 15))
        style.configure('Card.TLabel', background=cls.COLORS['card_bg'], foreground=cls.COLORS['text'], font=cls.FONTS['default'])
        # Card number, label, desc
        style.configure('CardNumber.TLabel', background=cls.COLORS['card_bg'], foreground=cls.COLORS['navy'], font=('Segoe UI', 24, 'bold'))
        style.configure('CardLabel.TLabel', background=cls.COLORS['card_bg'], foreground=cls.COLORS['navy'], font=('Segoe UI', 12, 'bold'))
        style.configure('CardDesc.TLabel', background=cls.COLORS['card_bg'], foreground=cls.COLORS['muted'], font=('Segoe UI', 10))
        # Section header
        style.configure('Section.TLabel', background=cls.COLORS['content_bg'], foreground=cls.COLORS['navy'], font=cls.FONTS['heading'])
        # Button
        style.configure('TButton', background=cls.COLORS['button_bg'], foreground=cls.COLORS['button_fg'], font=cls.FONTS['button'], borderwidth=1, relief='flat', padding=(10, 5))
        style.map('TButton', background=[('active', cls.COLORS['button_hover']), ('disabled', cls.COLORS['muted'])])
        # Status bar
        style.configure('Status.TLabel', background=cls.COLORS['status_bg'], foreground=cls.COLORS['status_text'], font=cls.FONTS['status'], padding=5)
        # Entry
        style.configure('TEntry', fieldbackground=cls.COLORS['card_bg'], foreground=cls.COLORS['text'], font=cls.FONTS['default'], padding=5, borderwidth=1)
        # Treeview
        style.configure('Treeview', background=cls.COLORS['card_bg'], foreground=cls.COLORS['text'], fieldbackground=cls.COLORS['card_bg'], font=cls.FONTS['default'], rowheight=25)
        style.configure('Treeview.Heading', background=cls.COLORS['navy'], foreground=cls.COLORS['sidebar_text'], font=cls.FONTS['default'], relief='flat')
        # Menu
        root.option_add('*Menu.background', cls.COLORS['card_bg'])
        root.option_add('*Menu.foreground', cls.COLORS['text'])
        root.option_add('*Menu.font', cls.FONTS['menu'])
        root.option_add('*Menu.activeBackground', cls.COLORS['sidebar_active'])
        root.option_add('*Menu.activeForeground', cls.COLORS['sidebar_text']) 