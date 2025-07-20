"""
Status bar component for displaying application status and document information.
"""
import tkinter as tk
from tkinter import ttk
from typing import Optional


class StatusBar:
    """Status bar widget for displaying application status."""
    
    def __init__(self, parent):
        self.frame = ttk.Frame(parent, relief=tk.SUNKEN)
        self.frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Create status sections
        self._create_sections()
    
    def _create_sections(self):
        """Create status bar sections."""
        # Document info section
        self.doc_info_frame = ttk.Frame(self.frame)
        self.doc_info_frame.pack(side=tk.LEFT, padx=5)
        
        self.doc_info_label = ttk.Label(
            self.doc_info_frame, 
            text="No document loaded",
            relief=tk.SUNKEN,
            padding=2
        )
        self.doc_info_label.pack(side=tk.LEFT)
        
        # Separator
        ttk.Separator(self.frame, orient=tk.VERTICAL).pack(
            side=tk.LEFT, fill=tk.Y, padx=5
        )
        
        # Page info section
        self.page_info_frame = ttk.Frame(self.frame)
        self.page_info_frame.pack(side=tk.LEFT, padx=5)
        
        self.page_info_label = ttk.Label(
            self.page_info_frame,
            text="Page: - / -",
            relief=tk.SUNKEN,
            padding=2
        )
        self.page_info_label.pack(side=tk.LEFT)
        
        # Separator
        ttk.Separator(self.frame, orient=tk.VERTICAL).pack(
            side=tk.LEFT, fill=tk.Y, padx=5
        )
        
        # Zoom info section
        self.zoom_info_frame = ttk.Frame(self.frame)
        self.zoom_info_frame.pack(side=tk.LEFT, padx=5)
        
        self.zoom_info_label = ttk.Label(
            self.zoom_info_frame,
            text="Zoom: -",
            relief=tk.SUNKEN,
            padding=2
        )
        self.zoom_info_label.pack(side=tk.LEFT)
        
        # Separator
        ttk.Separator(self.frame, orient=tk.VERTICAL).pack(
            side=tk.LEFT, fill=tk.Y, padx=5
        )
        
        # View mode section
        self.view_mode_frame = ttk.Frame(self.frame)
        self.view_mode_frame.pack(side=tk.LEFT, padx=5)
        
        self.view_mode_label = ttk.Label(
            self.view_mode_frame,
            text="Mode: -",
            relief=tk.SUNKEN,
            padding=2
        )
        self.view_mode_label.pack(side=tk.LEFT)
        
        # Status message section (expandable)
        self.status_frame = ttk.Frame(self.frame)
        self.status_frame.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=5)
        
        self.status_label = ttk.Label(
            self.status_frame,
            text="Ready",
            relief=tk.SUNKEN,
            padding=2,
            anchor=tk.W
        )
        self.status_label.pack(side=tk.RIGHT, fill=tk.X, expand=True)
    
    def update_document_info(self, filename: str, file_size: str = ""):
        """Update document information."""
        if filename:
            info_text = f"File: {filename}"
            if file_size:
                info_text += f" ({file_size})"
        else:
            info_text = "No document loaded"
        
        self.doc_info_label.config(text=info_text)
    
    def update_page_info(self, current_page: int, total_pages: int):
        """Update page information."""
        self.page_info_label.config(text=f"Page: {current_page} / {total_pages}")
    
    def update_zoom_info(self, zoom_text: str):
        """Update zoom information."""
        self.zoom_info_label.config(text=f"Zoom: {zoom_text}")
    
    def update_view_mode(self, mode: str):
        """Update view mode information."""
        mode_display = {
            "width": "Fit Width",
            "height": "Fit Height", 
            "page": "Fit Page",
            "actual": "Actual Size"
        }.get(mode, mode)
        
        self.view_mode_label.config(text=f"Mode: {mode_display}")
    
    def set_status(self, message: str):
        """Set status message."""
        self.status_label.config(text=message)
    
    def clear_status(self):
        """Clear status message."""
        self.status_label.config(text="Ready")
