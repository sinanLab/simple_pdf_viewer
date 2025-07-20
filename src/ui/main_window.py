"""
Main window UI components for the PDF viewer application.
"""
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from typing import Callable, Optional


class MainWindow:
    """Main application window."""
    
    def __init__(self, title: str = "PDF Viewer", geometry: str = "1000x700"):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(geometry)
        self.root.minsize(600, 400)
        
        # Callbacks
        self.on_open_pdf: Optional[Callable] = None
        self.on_exit: Optional[Callable] = None
        
        self._create_menu()
        self._setup_window()
    
    def _setup_window(self):
        """Setup window properties."""
        # Configure grid weights for proper resizing
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Bind window resize event
        self.root.bind('<Configure>', self._on_window_resize)
    
    def _on_window_resize(self, event):
        """Handle window resize events."""
        # Only handle main window resize, not child widget resizes
        if event.widget == self.root:
            if hasattr(self, 'on_window_resize') and self.on_window_resize:
                self.on_window_resize(event.width, event.height)
    
    def _create_menu(self):
        """Create the menu bar."""
        menubar = tk.Menu(self.root)
        
        # File menu
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open...", command=self._handle_open, accelerator="Ctrl+O")
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self._handle_exit, accelerator="Ctrl+Q")
        menubar.add_cascade(label="File", menu=filemenu)
        
        # View menu
        viewmenu = tk.Menu(menubar, tearoff=0)
        viewmenu.add_command(label="Zoom In", accelerator="Ctrl++")
        viewmenu.add_command(label="Zoom Out", accelerator="Ctrl+-")
        viewmenu.add_command(label="Actual Size", accelerator="Ctrl+0")
        viewmenu.add_separator()
        viewmenu.add_command(label="Fit Width", accelerator="Ctrl+1")
        viewmenu.add_command(label="Fit Height", accelerator="Ctrl+2")
        viewmenu.add_command(label="Fit Page", accelerator="Ctrl+3")
        viewmenu.add_separator()
        viewmenu.add_command(label="Rotate Clockwise", accelerator="Ctrl+R")
        menubar.add_cascade(label="View", menu=viewmenu)
        
        # Go menu
        gomenu = tk.Menu(menubar, tearoff=0)
        gomenu.add_command(label="First Page", accelerator="Ctrl+Home")
        gomenu.add_command(label="Previous Page", accelerator="Page Up")
        gomenu.add_command(label="Next Page", accelerator="Page Down")
        gomenu.add_command(label="Last Page", accelerator="Ctrl+End")
        gomenu.add_separator()
        gomenu.add_command(label="Go to Page...", accelerator="Ctrl+G")
        menubar.add_cascade(label="Go", menu=gomenu)
        
        self.root.config(menu=menubar)
        
        # Bind keyboard shortcuts
        self._bind_shortcuts()
    
    def _bind_shortcuts(self):
        """Bind keyboard shortcuts."""
        self.root.bind('<Control-o>', lambda e: self._handle_open())
        self.root.bind('<Control-q>', lambda e: self._handle_exit())
    
    def _handle_open(self):
        """Handle open menu item click."""
        if self.on_open_pdf:
            self.on_open_pdf()
    
    def _handle_exit(self):
        """Handle exit menu item click."""
        if self.on_exit:
            self.on_exit()
        else:
            self.root.quit()
    
    def set_open_callback(self, callback: Callable):
        """Set callback for open PDF action."""
        self.on_open_pdf = callback
    
    def set_exit_callback(self, callback: Callable):
        """Set callback for exit action."""
        self.on_exit = callback
    
    def set_window_resize_callback(self, callback: Callable):
        """Set callback for window resize."""
        self.on_window_resize = callback
    
    def run(self):
        """Start the main event loop."""
        self.root.mainloop()
    
    def quit(self):
        """Quit the application."""
        self.root.quit()
    
    def get_size(self) -> tuple:
        """Get current window size."""
        return (self.root.winfo_width(), self.root.winfo_height())


class Toolbar:
    """Enhanced toolbar with navigation, zoom, and view controls."""
    
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=2)
        
        # Callbacks
        self.on_prev_page: Optional[Callable] = None
        self.on_next_page: Optional[Callable] = None
        self.on_first_page: Optional[Callable] = None
        self.on_last_page: Optional[Callable] = None
        self.on_go_to_page: Optional[Callable] = None
        self.on_zoom_in: Optional[Callable] = None
        self.on_zoom_out: Optional[Callable] = None
        self.on_reset_zoom: Optional[Callable] = None
        self.on_fit_width: Optional[Callable] = None
        self.on_fit_height: Optional[Callable] = None
        self.on_fit_page: Optional[Callable] = None
        self.on_actual_size: Optional[Callable] = None
        self.on_rotate: Optional[Callable] = None
        self.on_search: Optional[Callable] = None
        
        self._create_controls()
    
    def _create_controls(self):
        """Create enhanced toolbar controls."""
        # Navigation section
        nav_frame = ttk.LabelFrame(self.frame, text="Navigation", padding=5)
        nav_frame.pack(side=tk.LEFT, padx=(0, 10), pady=2)
        
        # First/Previous buttons
        self.first_btn = ttk.Button(
            nav_frame, text="⏮", command=self._handle_first_page,
            state=tk.DISABLED, width=3, style="Toolbar.TButton"
        )
        self.first_btn.pack(side=tk.LEFT, padx=1)
        
        self.prev_btn = ttk.Button(
            nav_frame, text="◀", command=self._handle_prev_page,
            state=tk.DISABLED, width=3, style="Toolbar.TButton"
        )
        self.prev_btn.pack(side=tk.LEFT, padx=1)
        
        # Page info and entry
        page_frame = ttk.Frame(nav_frame)
        page_frame.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(page_frame, text="Page:").pack(side=tk.LEFT)
        
        self.page_entry = ttk.Entry(page_frame, width=6, justify='center')
        self.page_entry.pack(side=tk.LEFT, padx=2)
        self.page_entry.bind('<Return>', self._handle_page_entry)
        
        self.page_total_label = ttk.Label(page_frame, text="/ 0")
        self.page_total_label.pack(side=tk.LEFT, padx=2)
        
        # Next/Last buttons
        self.next_btn = ttk.Button(
            nav_frame, text="▶", command=self._handle_next_page,
            state=tk.DISABLED, width=3, style="Toolbar.TButton"
        )
        self.next_btn.pack(side=tk.LEFT, padx=1)
        
        self.last_btn = ttk.Button(
            nav_frame, text="⏭", command=self._handle_last_page,
            state=tk.DISABLED, width=3, style="Toolbar.TButton"
        )
        self.last_btn.pack(side=tk.LEFT, padx=1)
        
        # Zoom section
        zoom_frame = ttk.LabelFrame(self.frame, text="Zoom", padding=5)
        zoom_frame.pack(side=tk.LEFT, padx=(0, 10), pady=2)
        
        self.zoom_out_btn = ttk.Button(
            zoom_frame, text="−", command=self._handle_zoom_out, 
            width=3, style="Toolbar.TButton"
        )
        self.zoom_out_btn.pack(side=tk.LEFT, padx=1)
        
        self.zoom_label = ttk.Label(zoom_frame, text="100%", width=6)
        self.zoom_label.pack(side=tk.LEFT, padx=5)
        
        self.zoom_in_btn = ttk.Button(
            zoom_frame, text="+", command=self._handle_zoom_in, 
            width=3, style="Toolbar.TButton"
        )
        self.zoom_in_btn.pack(side=tk.LEFT, padx=1)
        
        # Fit options
        fit_frame = ttk.LabelFrame(self.frame, text="Fit", padding=5)
        fit_frame.pack(side=tk.LEFT, padx=(0, 10), pady=2)
        
        self.fit_width_btn = ttk.Button(
            fit_frame, text="Width", command=self._handle_fit_width, width=6
        )
        self.fit_width_btn.pack(side=tk.LEFT, padx=1)
        
        self.fit_height_btn = ttk.Button(
            fit_frame, text="Height", command=self._handle_fit_height, width=6
        )
        self.fit_height_btn.pack(side=tk.LEFT, padx=1)
        
        self.fit_page_btn = ttk.Button(
            fit_frame, text="Page", command=self._handle_fit_page, width=6
        )
        self.fit_page_btn.pack(side=tk.LEFT, padx=1)
        
        self.actual_size_btn = ttk.Button(
            fit_frame, text="100%", command=self._handle_actual_size, width=6
        )
        self.actual_size_btn.pack(side=tk.LEFT, padx=1)
        
        # Tools section
        tools_frame = ttk.LabelFrame(self.frame, text="Tools", padding=5)
        tools_frame.pack(side=tk.LEFT, padx=(0, 10), pady=2)
        
        self.rotate_btn = ttk.Button(
            tools_frame, text="↻", command=self._handle_rotate, 
            width=3, style="Toolbar.TButton"
        )
        self.rotate_btn.pack(side=tk.LEFT, padx=1)
        
        # Search section
        search_frame = ttk.Frame(tools_frame)
        search_frame.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        
        self.search_entry = ttk.Entry(search_frame, width=15)
        self.search_entry.pack(side=tk.LEFT, padx=2)
        self.search_entry.bind('<Return>', self._handle_search)
        
        self.search_btn = ttk.Button(
            search_frame, text="🔍", command=self._handle_search, width=3
        )
        self.search_btn.pack(side=tk.LEFT, padx=1)
    
    
    def _handle_prev_page(self):
        """Handle previous page button click."""
        if self.on_prev_page:
            self.on_prev_page()
    
    def _handle_next_page(self):
        """Handle next page button click."""
        if self.on_next_page:
            self.on_next_page()
    
    def _handle_first_page(self):
        """Handle first page button click."""
        if self.on_first_page:
            self.on_first_page()
    
    def _handle_last_page(self):
        """Handle last page button click."""
        if self.on_last_page:
            self.on_last_page()
    
    def _handle_page_entry(self, event=None):
        """Handle page entry field."""
        try:
            page_num = int(self.page_entry.get())
            if self.on_go_to_page:
                self.on_go_to_page(page_num)
        except ValueError:
            pass  # Invalid page number
    
    def _handle_zoom_in(self):
        """Handle zoom in button click."""
        if self.on_zoom_in:
            self.on_zoom_in()
    
    def _handle_zoom_out(self):
        """Handle zoom out button click."""
        if self.on_zoom_out:
            self.on_zoom_out()
    
    def _handle_reset_zoom(self):
        """Handle reset zoom button click."""
        if self.on_reset_zoom:
            self.on_reset_zoom()
    
    def _handle_fit_width(self):
        """Handle fit width button click."""
        if self.on_fit_width:
            self.on_fit_width()
    
    def _handle_fit_height(self):
        """Handle fit height button click."""
        if self.on_fit_height:
            self.on_fit_height()
    
    def _handle_fit_page(self):
        """Handle fit page button click."""
        if self.on_fit_page:
            self.on_fit_page()
    
    def _handle_actual_size(self):
        """Handle actual size button click."""
        if self.on_actual_size:
            self.on_actual_size()
    
    def _handle_rotate(self):
        """Handle rotate button click."""
        if self.on_rotate:
            self.on_rotate()
    
    def _handle_search(self, event=None):
        """Handle search functionality."""
        search_text = self.search_entry.get().strip()
        if search_text and self.on_search:
            self.on_search(search_text)
    
    # Callback setters
    def set_prev_page_callback(self, callback: Callable):
        """Set callback for previous page action."""
        self.on_prev_page = callback
    
    def set_next_page_callback(self, callback: Callable):
        """Set callback for next page action."""
        self.on_next_page = callback
    
    def set_first_page_callback(self, callback: Callable):
        """Set callback for first page action."""
        self.on_first_page = callback
    
    def set_last_page_callback(self, callback: Callable):
        """Set callback for last page action."""
        self.on_last_page = callback
    
    def set_go_to_page_callback(self, callback: Callable):
        """Set callback for go to page action."""
        self.on_go_to_page = callback
    
    def set_zoom_in_callback(self, callback: Callable):
        """Set callback for zoom in action."""
        self.on_zoom_in = callback
    
    def set_zoom_out_callback(self, callback: Callable):
        """Set callback for zoom out action."""
        self.on_zoom_out = callback
    
    def set_reset_zoom_callback(self, callback: Callable):
        """Set callback for reset zoom action."""
        self.on_reset_zoom = callback
    
    def set_fit_width_callback(self, callback: Callable):
        """Set callback for fit width action."""
        self.on_fit_width = callback
    
    def set_fit_height_callback(self, callback: Callable):
        """Set callback for fit height action."""
        self.on_fit_height = callback
    
    def set_fit_page_callback(self, callback: Callable):
        """Set callback for fit page action."""
        self.on_fit_page = callback
    
    def set_actual_size_callback(self, callback: Callable):
        """Set callback for actual size action."""
        self.on_actual_size = callback
    
    def set_rotate_callback(self, callback: Callable):
        """Set callback for rotate action."""
        self.on_rotate = callback
    
    def set_search_callback(self, callback: Callable):
        """Set callback for search action."""
        self.on_search = callback
    
    # UI update methods
    def update_page_info(self, current_page: int, total_pages: int):
        """Update page information display."""
        self.page_total_label.config(text=f"/ {total_pages}")
        self.page_entry.delete(0, tk.END)
        self.page_entry.insert(0, str(current_page))
    
    def update_zoom_info(self, zoom_text: str):
        """Update zoom information display."""
        self.zoom_label.config(text=zoom_text)
    
    def set_navigation_state(self, can_prev: bool, can_next: bool, 
                           can_first: bool, can_last: bool):
        """Set navigation button states."""
        prev_state = tk.NORMAL if can_prev else tk.DISABLED
        next_state = tk.NORMAL if can_next else tk.DISABLED
        first_state = tk.NORMAL if can_first else tk.DISABLED
        last_state = tk.NORMAL if can_last else tk.DISABLED
        
        self.prev_btn.config(state=prev_state)
        self.next_btn.config(state=next_state)
        self.first_btn.config(state=first_state)
        self.last_btn.config(state=last_state)
    
    def set_prev_button_state(self, enabled: bool):
        """Enable/disable previous button."""
        state = tk.NORMAL if enabled else tk.DISABLED
        self.prev_btn.config(state=state)
    
    def set_next_button_state(self, enabled: bool):
        """Enable/disable next button."""
        state = tk.NORMAL if enabled else tk.DISABLED
        self.next_btn.config(state=state)
