"""
Canvas component for displaying PDF content.
"""
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk
from typing import Optional


class PDFCanvas:
    """Canvas widget for displaying PDF pages with scrollbars."""
    
    def __init__(self, parent):
        self.parent = parent
        self.images = []  # Keep references to images to prevent garbage collection
        
        self._create_canvas()
        self._create_scrollbars()
        self._setup_scrolling()
    
    def _create_canvas(self):
        """Create the main canvas."""
        self.canvas = tk.Canvas(self.parent, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)
    
    def _create_scrollbars(self):
        """Create vertical and horizontal scrollbars."""
        # Vertical scrollbar
        self.v_scroll = ttk.Scrollbar(
            self.parent, 
            orient=tk.VERTICAL, 
            command=self.canvas.yview
        )
        self.v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Horizontal scrollbar
        self.h_scroll = ttk.Scrollbar(
            self.parent, 
            orient=tk.HORIZONTAL, 
            command=self.canvas.xview
        )
        self.h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
    
    def _setup_scrolling(self):
        """Setup canvas scrolling configuration."""
        self.canvas.configure(
            yscrollcommand=self.v_scroll.set, 
            xscrollcommand=self.h_scroll.set
        )
        self.canvas.bind('<Configure>', self._on_canvas_configure)
    
    def _on_canvas_configure(self, event):
        """Handle canvas configuration changes."""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def display_image(self, image: ImageTk.PhotoImage, x: int = 20, y: int = 20):
        """
        Display an image on the canvas.
        
        Args:
            image (ImageTk.PhotoImage): The image to display
            x (int): X position to place the image
            y (int): Y position to place the image
        """
        # Clear canvas
        self.clear()
        
        # Keep reference to avoid garbage collection
        self.images.append(image)
        
        # Display on canvas
        self.canvas.create_image(x, y, anchor=tk.NW, image=image)
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
    
    def clear(self):
        """Clear the canvas and remove image references."""
        self.canvas.delete("all")
        self.images.clear()
    
    def get_canvas_size(self) -> tuple:
        """Get the current canvas size."""
        return (self.canvas.winfo_width(), self.canvas.winfo_height())
    
    def scroll_to_top(self):
        """Scroll to the top of the canvas."""
        self.canvas.yview_moveto(0)
        self.canvas.xview_moveto(0)
