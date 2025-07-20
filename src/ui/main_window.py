"""
Main window UI components for the PDF viewer application.
"""
import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional


class MainWindow:
    """Main application window."""
    
    def __init__(self, title: str = "PDF Viewer", geometry: str = "800x600"):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(geometry)
        
        # Callbacks
        self.on_open_pdf: Optional[Callable] = None
        self.on_exit: Optional[Callable] = None
        
        self._create_menu()
    
    def _create_menu(self):
        """Create the menu bar."""
        menubar = tk.Menu(self.root)
        
        # File menu
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self._handle_open)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self._handle_exit)
        menubar.add_cascade(label="File", menu=filemenu)
        
        self.root.config(menu=menubar)
    
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
    
    def run(self):
        """Start the main event loop."""
        self.root.mainloop()
    
    def quit(self):
        """Quit the application."""
        self.root.quit()


class Toolbar:
    """Toolbar with navigation and zoom controls."""
    
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.frame.pack(side=tk.TOP, fill=tk.X)
        
        # Callbacks
        self.on_prev_page: Optional[Callable] = None
        self.on_next_page: Optional[Callable] = None
        self.on_zoom_in: Optional[Callable] = None
        self.on_zoom_out: Optional[Callable] = None
        self.on_reset_zoom: Optional[Callable] = None
        
        self._create_controls()
    
    def _create_controls(self):
        """Create toolbar controls."""
        # Navigation buttons
        self.prev_btn = ttk.Button(
            self.frame, 
            text="Previous", 
            command=self._handle_prev_page,
            state=tk.DISABLED
        )
        self.prev_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        self.next_btn = ttk.Button(
            self.frame, 
            text="Next", 
            command=self._handle_next_page,
            state=tk.DISABLED
        )
        self.next_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        # Page info
        self.page_label = ttk.Label(self.frame, text="Page: 0/0")
        self.page_label.pack(side=tk.LEFT, padx=10)
        
        # Zoom controls
        ttk.Label(self.frame, text="Zoom:").pack(side=tk.LEFT, padx=(10, 2))
        
        self.zoom_in_btn = ttk.Button(
            self.frame, 
            text="+", 
            command=self._handle_zoom_in, 
            width=3
        )
        self.zoom_in_btn.pack(side=tk.LEFT, padx=2)
        
        self.zoom_out_btn = ttk.Button(
            self.frame, 
            text="-", 
            command=self._handle_zoom_out, 
            width=3
        )
        self.zoom_out_btn.pack(side=tk.LEFT, padx=2)
        
        self.reset_zoom_btn = ttk.Button(
            self.frame, 
            text="Reset", 
            command=self._handle_reset_zoom
        )
        self.reset_zoom_btn.pack(side=tk.LEFT, padx=10)
    
    def _handle_prev_page(self):
        """Handle previous page button click."""
        if self.on_prev_page:
            self.on_prev_page()
    
    def _handle_next_page(self):
        """Handle next page button click."""
        if self.on_next_page:
            self.on_next_page()
    
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
    
    def set_prev_page_callback(self, callback: Callable):
        """Set callback for previous page action."""
        self.on_prev_page = callback
    
    def set_next_page_callback(self, callback: Callable):
        """Set callback for next page action."""
        self.on_next_page = callback
    
    def set_zoom_in_callback(self, callback: Callable):
        """Set callback for zoom in action."""
        self.on_zoom_in = callback
    
    def set_zoom_out_callback(self, callback: Callable):
        """Set callback for zoom out action."""
        self.on_zoom_out = callback
    
    def set_reset_zoom_callback(self, callback: Callable):
        """Set callback for reset zoom action."""
        self.on_reset_zoom = callback
    
    def update_page_info(self, current_page: int, total_pages: int):
        """Update page information display."""
        self.page_label.config(text=f"Page: {current_page}/{total_pages}")
    
    def set_prev_button_state(self, enabled: bool):
        """Enable/disable previous button."""
        state = tk.NORMAL if enabled else tk.DISABLED
        self.prev_btn.config(state=state)
    
    def set_next_button_state(self, enabled: bool):
        """Enable/disable next button."""
        state = tk.NORMAL if enabled else tk.DISABLED
        self.next_btn.config(state=state)
