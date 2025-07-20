"""
Enhanced canvas component for displaying PDF content with improved scaling and scrolling.
"""
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk
from typing import Optional, Callable


class PDFCanvas:
    """Enhanced canvas widget for displaying PDF pages with scrollbars and scaling."""
    
    def __init__(self, parent):
        self.parent = parent
        self.images = []  # Keep references to images to prevent garbage collection
        self.canvas_width = 800
        self.canvas_height = 600
        self.on_size_change: Optional[Callable] = None
        self.on_page_change: Optional[Callable] = None  # Callback for automatic page navigation
        
        self._create_canvas_frame()
        self._create_canvas()
        self._create_scrollbars()
        self._setup_scrolling()
        self._setup_mouse_events()
    
    def _create_canvas_frame(self):
        """Create frame to hold canvas and scrollbars."""
        self.canvas_frame = ttk.Frame(self.parent)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Configure grid weights
        self.canvas_frame.grid_rowconfigure(0, weight=1)
        self.canvas_frame.grid_columnconfigure(0, weight=1)
    
    def _create_canvas(self):
        """Create the main canvas."""
        self.canvas = tk.Canvas(
            self.canvas_frame, 
            bg='white',
            highlightthickness=0,
            relief='flat'
        )
        self.canvas.grid(row=0, column=0, sticky='nsew')
    
    def _create_scrollbars(self):
        """Create vertical and horizontal scrollbars."""
        # Vertical scrollbar
        self.v_scroll = ttk.Scrollbar(
            self.canvas_frame, 
            orient=tk.VERTICAL, 
            command=self.canvas.yview
        )
        self.v_scroll.grid(row=0, column=1, sticky='ns')
        
        # Horizontal scrollbar
        self.h_scroll = ttk.Scrollbar(
            self.canvas_frame, 
            orient=tk.HORIZONTAL, 
            command=self.canvas.xview
        )
        self.h_scroll.grid(row=1, column=0, sticky='ew')
    
    def _setup_scrolling(self):
        """Setup canvas scrolling configuration."""
        self.canvas.configure(
            yscrollcommand=self.v_scroll.set, 
            xscrollcommand=self.h_scroll.set
        )
        self.canvas.bind('<Configure>', self._on_canvas_configure)
    
    def _setup_mouse_events(self):
        """Setup mouse wheel scrolling and other events."""
        # Mouse wheel scrolling
        self.canvas.bind('<MouseWheel>', self._on_mousewheel)
        self.canvas.bind('<Button-4>', self._on_mousewheel)  # Linux
        self.canvas.bind('<Button-5>', self._on_mousewheel)  # Linux
        
        # Horizontal scrolling with Shift+MouseWheel
        self.canvas.bind('<Shift-MouseWheel>', self._on_shift_mousewheel)
        
        # Middle mouse button panning
        self.canvas.bind('<Button-2>', self._start_pan)
        self.canvas.bind('<B2-Motion>', self._do_pan)
        
        # Allow canvas to receive focus for keyboard events
        self.canvas.bind('<Button-1>', lambda e: self.canvas.focus_set())
        
        self.pan_start_x = 0
        self.pan_start_y = 0
    
    def _on_canvas_configure(self, event):
        """Handle canvas configuration changes."""
        # Update canvas size
        self.canvas_width = event.width
        self.canvas_height = event.height
        
        # Update scroll region
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
        # Notify size change
        if self.on_size_change:
            self.on_size_change(self.canvas_width, self.canvas_height)
    
    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling with automatic page navigation."""
        # Determine scroll direction and amount
        if event.delta:  # Windows
            delta = -1 * (event.delta / 120)
        elif event.num == 4:  # Linux scroll up
            delta = -1
        elif event.num == 5:  # Linux scroll down
            delta = 1
        else:
            return
        
        # Get current scroll position
        current_y_top, current_y_bottom = self.canvas.yview()
        
        # Check if we're at the boundaries and should change pages
        scroll_threshold = 0.05  # 5% threshold for page change
        
        if delta > 0:  # Scrolling down
            if current_y_bottom >= (1.0 - scroll_threshold):
                # At bottom, try to go to next page
                if self.on_page_change:
                    if self.on_page_change('next'):
                        return  # Page changed, don't scroll
                # If page didn't change, continue with normal scrolling
        else:  # Scrolling up
            if current_y_top <= scroll_threshold:
                # At top, try to go to previous page
                if self.on_page_change:
                    if self.on_page_change('prev'):
                        # When going to previous page, scroll to bottom
                        self.canvas.after(10, lambda: self.canvas.yview_moveto(1.0))
                        return  # Page changed
                # If page didn't change, continue with normal scrolling
        
        # Normal scrolling
        self.canvas.yview_scroll(int(delta), "units")
    
    def _on_shift_mousewheel(self, event):
        """Handle horizontal scrolling with Shift+MouseWheel."""
        if event.delta:  # Windows
            delta = -1 * (event.delta / 120)
        else:
            return
        
        # Scroll horizontally
        self.canvas.xview_scroll(int(delta), "units")
    
    def _start_pan(self, event):
        """Start panning with middle mouse button."""
        self.pan_start_x = event.x
        self.pan_start_y = event.y
    
    def _do_pan(self, event):
        """Perform panning motion."""
        # Calculate movement
        dx = self.pan_start_x - event.x
        dy = self.pan_start_y - event.y
        
        # Get current scroll positions
        x_view = self.canvas.canvasx(0)
        y_view = self.canvas.canvasy(0)
        
        # Update scroll positions
        self.canvas.scan_dragto(int(x_view + dx), int(y_view + dy), gain=1)
        
        # Update start position
        self.pan_start_x = event.x
        self.pan_start_y = event.y
    
    def display_image(self, image: ImageTk.PhotoImage, center: bool = True, from_scroll: bool = False):
        """
        Display an image on the canvas.
        
        Args:
            image (ImageTk.PhotoImage): The image to display
            center (bool): Whether to center the image in the canvas
            from_scroll (bool): Whether this is from auto-scroll page change
        """
        # Clear canvas
        self.clear()
        
        # Keep reference to avoid garbage collection
        self.images.append(image)
        
        # Calculate position
        if center:
            # Center the image in the canvas
            img_width = image.width()
            img_height = image.height()
            
            x = max(20, (self.canvas_width - img_width) // 2)
            y = max(20, (self.canvas_height - img_height) // 2)
        else:
            x, y = 20, 20
        
        # Display on canvas
        self.canvas.create_image(x, y, anchor=tk.NW, image=image)
        
        # Update scroll region with some padding
        self.canvas.update_idletasks()
        bbox = self.canvas.bbox("all")
        if bbox:
            padx, pady = 50, 50
            scroll_region = (
                bbox[0] - padx, bbox[1] - pady, 
                bbox[2] + padx, bbox[3] + pady
            )
            self.canvas.configure(scrollregion=scroll_region)
        
        # If this is from auto-scroll, provide visual feedback
        if from_scroll:
            self._show_page_transition_effect()
    
    def clear(self):
        """Clear the canvas and remove image references."""
        self.canvas.delete("all")
        self.images.clear()
    
    def get_canvas_size(self) -> tuple:
        """Get the current canvas size."""
        return (self.canvas_width, self.canvas_height)
    
    def scroll_to_top(self):
        """Scroll to the top of the canvas."""
        self.canvas.yview_moveto(0)
        self.canvas.xview_moveto(0)
    
    def center_view(self):
        """Center the view on the content."""
        # Get scroll region
        scroll_region = self.canvas.cget('scrollregion')
        if not scroll_region:
            return
        
        # Parse scroll region
        x1, y1, x2, y2 = map(float, scroll_region.split())
        
        # Calculate center positions
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2
        
        # Get canvas dimensions
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # Calculate scroll fractions to center the view
        if x2 - x1 > canvas_width:
            x_fraction = (center_x - canvas_width / 2) / (x2 - x1 - canvas_width)
            x_fraction = max(0, min(1, x_fraction))
            self.canvas.xview_moveto(x_fraction)
        
        if y2 - y1 > canvas_height:
            y_fraction = (center_y - canvas_height / 2) / (y2 - y1 - canvas_height)
            y_fraction = max(0, min(1, y_fraction))
            self.canvas.yview_moveto(y_fraction)
    
    def set_size_change_callback(self, callback: Callable):
        """Set callback for canvas size changes."""
        self.on_size_change = callback
    
    def set_page_change_callback(self, callback: Callable):
        """Set callback for automatic page navigation."""
        self.on_page_change = callback
    
    def highlight_search_results(self, results: list):
        """Highlight search results on the canvas."""
        # Remove previous highlights
        self.canvas.delete("search_highlight")
        
        # Add new highlights
        for result in results:
            x1, y1, x2, y2 = result['rect']
            self.canvas.create_rectangle(
                x1, y1, x2, y2,
                outline='red', width=2, fill='yellow', stipple='gray50',
                tags="search_highlight"
            )
    
    def _show_page_transition_effect(self):
        """Show a subtle visual effect when changing pages automatically."""
        # Create a temporary border effect
        bbox = self.canvas.bbox("all")
        if bbox:
            border = self.canvas.create_rectangle(
                bbox[0]-2, bbox[1]-2, bbox[2]+2, bbox[3]+2,
                outline='#00ff00', width=3, tags="page_transition"
            )
            # Remove the border after a short time
            self.canvas.after(300, lambda: self.canvas.delete("page_transition"))
