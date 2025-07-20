"""
Enhanced PDF Viewer application controller with advanced features.
"""
import sys
import os
from tkinter import messagebox

# Add src directory to path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.pdf_handler import PDFHandler
from src.ui.main_window import MainWindow, Toolbar
from src.ui.canvas import PDFCanvas
from src.ui.status_bar import StatusBar
from src.utils.file_handler import FileHandler


class PDFViewerApp:
    """Enhanced PDF Viewer application controller."""
    
    def __init__(self):
        # Initialize components
        self.pdf_handler = PDFHandler()
        self.file_handler = FileHandler()
        
        # Create main window
        self.main_window = MainWindow("Enhanced PDF Viewer", "1000x700")
        
        # Create toolbar
        self.toolbar = Toolbar(self.main_window.root)
        
        # Create canvas
        self.canvas = PDFCanvas(self.main_window.root)
        
        # Create status bar
        self.status_bar = StatusBar(self.main_window.root)
        
        # Setup event handlers
        self._setup_event_handlers()
        
        # Setup keyboard shortcuts
        self._setup_keyboard_shortcuts()
        
        # Current search results
        self.search_results = []
        self.current_search_index = 0
    
    def _setup_event_handlers(self):
        """Setup event handlers for UI components."""
        # Main window events
        self.main_window.set_open_callback(self._open_pdf)
        self.main_window.set_exit_callback(self._exit_app)
        self.main_window.set_window_resize_callback(self._on_window_resize)
        
        # Canvas events
        self.canvas.set_size_change_callback(self._on_canvas_resize)
        self.canvas.set_page_change_callback(self._on_auto_page_change)
        
        # Toolbar events - Navigation
        self.toolbar.set_prev_page_callback(self._prev_page)
        self.toolbar.set_next_page_callback(self._next_page)
        self.toolbar.set_first_page_callback(self._first_page)
        self.toolbar.set_last_page_callback(self._last_page)
        self.toolbar.set_go_to_page_callback(self._go_to_page)
        
        # Toolbar events - Zoom
        self.toolbar.set_zoom_in_callback(self._zoom_in)
        self.toolbar.set_zoom_out_callback(self._zoom_out)
        self.toolbar.set_reset_zoom_callback(self._reset_zoom)
        
        # Toolbar events - Fit
        self.toolbar.set_fit_width_callback(self._fit_width)
        self.toolbar.set_fit_height_callback(self._fit_height)
        self.toolbar.set_fit_page_callback(self._fit_page)
        self.toolbar.set_actual_size_callback(self._actual_size)
        
        # Toolbar events - Tools
        self.toolbar.set_rotate_callback(self._rotate_page)
        self.toolbar.set_search_callback(self._search_text)
    
    def _setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts."""
        root = self.main_window.root
        
        # Navigation shortcuts
        root.bind('<Prior>', lambda e: self._prev_page())  # Page Up
        root.bind('<Next>', lambda e: self._next_page())   # Page Down
        root.bind('<Control-Home>', lambda e: self._first_page())
        root.bind('<Control-End>', lambda e: self._last_page())
        root.bind('<Control-g>', lambda e: self._show_go_to_dialog())
        
        # Zoom shortcuts
        root.bind('<Control-plus>', lambda e: self._zoom_in())
        root.bind('<Control-equal>', lambda e: self._zoom_in())  # = key
        root.bind('<Control-minus>', lambda e: self._zoom_out())
        root.bind('<Control-0>', lambda e: self._actual_size())
        
        # Fit shortcuts
        root.bind('<Control-1>', lambda e: self._fit_width())
        root.bind('<Control-2>', lambda e: self._fit_height())
        root.bind('<Control-3>', lambda e: self._fit_page())
        
        # Other shortcuts
        root.bind('<Control-r>', lambda e: self._rotate_page())
        root.bind('<Control-f>', lambda e: self._focus_search())
        root.bind('<F3>', lambda e: self._find_next())
        root.bind('<Shift-F3>', lambda e: self._find_previous())
    
    def _on_window_resize(self, width: int, height: int):
        """Handle window resize events."""
        # Update PDF handler canvas size for fit calculations
        canvas_size = self.canvas.get_canvas_size()
        self.pdf_handler.set_canvas_size(canvas_size[0], canvas_size[1])
        
        # If in fit mode, recalculate and update display
        if self.pdf_handler.fit_mode in ["width", "height", "page"]:
            self._update_display()
    
    def _on_canvas_resize(self, width: int, height: int):
        """Handle canvas resize events."""
        # Update PDF handler canvas size
        self.pdf_handler.set_canvas_size(width, height)
        
        # If in fit mode, recalculate and update display
        if self.pdf_handler.fit_mode in ["width", "height", "page"]:
            self._update_display()
    
    def _on_auto_page_change(self, direction: str) -> bool:
        """
        Handle automatic page changes from scrolling.
        
        Args:
            direction (str): 'next' or 'prev'
            
        Returns:
            bool: True if page was changed, False otherwise
        """
        if direction == 'next':
            if self.pdf_handler.can_go_next():
                self.pdf_handler.go_to_next_page()
                self._update_display(from_auto_scroll=True)
                self._update_ui_state()
                self.status_bar.set_status("Next page")
                # Clear status after 2 seconds
                self.main_window.root.after(2000, lambda: self.status_bar.set_status("Ready"))
                return True
        elif direction == 'prev':
            if self.pdf_handler.can_go_previous():
                self.pdf_handler.go_to_previous_page()
                self._update_display(from_auto_scroll=True)
                self._update_ui_state()
                self.status_bar.set_status("Previous page")
                # Clear status after 2 seconds
                self.main_window.root.after(2000, lambda: self.status_bar.set_status("Ready"))
                return True
        
        return False
    
    def _open_pdf(self):
        """Handle open PDF action."""
        file_path = self.file_handler.open_pdf_dialog()
        if file_path:
            if self.file_handler.is_valid_pdf(file_path):
                if self.pdf_handler.open_document(file_path):
                    # Set initial canvas size
                    canvas_size = self.canvas.get_canvas_size()
                    self.pdf_handler.set_canvas_size(canvas_size[0], canvas_size[1])
                    
                    # Set initial fit mode to page
                    self.pdf_handler.set_fit_mode("page")
                    
                    self._update_display()
                    self._update_ui_state()
                    
                    # Set window title to include filename
                    filename = os.path.basename(file_path)
                    self.main_window.root.title(f"Enhanced PDF Viewer - {filename}")
                    
                    # Update status bar
                    file_info = self.file_handler.get_file_info(file_path)
                    size_text = f"{file_info.get('size_mb', 0)} MB" if file_info else ""
                    self.status_bar.update_document_info(filename, size_text)
                    self.status_bar.set_status("Document loaded successfully")
                else:
                    messagebox.showerror("Error", "Could not open PDF file")
            else:
                messagebox.showerror("Error", "Invalid PDF file")
    
    def _exit_app(self):
        """Handle exit application action."""
        self.pdf_handler.close_document()
        self.main_window.quit()
    
    # Navigation methods
    def _prev_page(self):
        """Handle previous page action."""
        if self.pdf_handler.go_to_previous_page():
            self._update_display()
            self._update_ui_state()
    
    def _next_page(self):
        """Handle next page action."""
        if self.pdf_handler.go_to_next_page():
            self._update_display()
            self._update_ui_state()
    
    def _first_page(self):
        """Handle first page action."""
        if self.pdf_handler.go_to_first_page():
            self._update_display()
            self._update_ui_state()
    
    def _last_page(self):
        """Handle last page action."""
        if self.pdf_handler.go_to_last_page():
            self._update_display()
            self._update_ui_state()
    
    def _go_to_page(self, page_number: int):
        """Handle go to page action."""
        if self.pdf_handler.go_to_page(page_number):
            self._update_display()
            self._update_ui_state()
        else:
            messagebox.showerror("Error", f"Invalid page number: {page_number}")
    
    def _show_go_to_dialog(self):
        """Show go to page dialog."""
        from tkinter import simpledialog
        
        total_pages = self.pdf_handler.get_page_count()
        if total_pages == 0:
            return
        
        page_num = simpledialog.askinteger(
            "Go to Page",
            f"Enter page number (1-{total_pages}):",
            minvalue=1,
            maxvalue=total_pages,
            initialvalue=self.pdf_handler.get_current_page_number()
        )
        
        if page_num:
            self._go_to_page(page_num)
    
    # Zoom methods
    def _zoom_in(self):
        """Handle zoom in action."""
        self.pdf_handler.zoom_in()
        self._update_display()
        self._update_zoom_info()
    
    def _zoom_out(self):
        """Handle zoom out action."""
        self.pdf_handler.zoom_out()
        self._update_display()
        self._update_zoom_info()
    
    def _reset_zoom(self):
        """Handle reset zoom action."""
        self.pdf_handler.reset_zoom()
        self._update_display()
        self._update_zoom_info()
    
    # Fit methods
    def _fit_width(self):
        """Handle fit width action."""
        self.pdf_handler.set_fit_mode("width")
        self._update_display()
        self._update_zoom_info()
    
    def _fit_height(self):
        """Handle fit height action."""
        self.pdf_handler.set_fit_mode("height")
        self._update_display()
        self._update_zoom_info()
    
    def _fit_page(self):
        """Handle fit page action."""
        self.pdf_handler.set_fit_mode("page")
        self._update_display()
        self._update_zoom_info()
    
    def _actual_size(self):
        """Handle actual size action."""
        self.pdf_handler.set_fit_mode("actual")
        self._update_display()
        self._update_zoom_info()
    
    # Other methods
    def _rotate_page(self):
        """Handle rotate page action."""
        self.pdf_handler.rotate_page()
        self._update_display()
    
    def _search_text(self, text: str):
        """Handle search text action."""
        self.search_results = self.pdf_handler.search_text(text)
        self.current_search_index = 0
        
        if self.search_results:
            self.canvas.highlight_search_results(self.search_results)
            messagebox.showinfo("Search", f"Found {len(self.search_results)} instances of '{text}'")
        else:
            self.canvas.highlight_search_results([])  # Clear highlights
            messagebox.showinfo("Search", f"'{text}' not found on current page")
    
    def _focus_search(self):
        """Focus on search entry field."""
        self.toolbar.search_entry.focus_set()
    
    def _find_next(self):
        """Find next search result."""
        if self.search_results and self.current_search_index < len(self.search_results) - 1:
            self.current_search_index += 1
            # Could implement highlighting of current result here
    
    def _find_previous(self):
        """Find previous search result."""
        if self.search_results and self.current_search_index > 0:
            self.current_search_index -= 1
            # Could implement highlighting of current result here
    
    def _update_display(self, from_auto_scroll: bool = False):
        """Update the PDF display."""
        image = self.pdf_handler.render_current_page()
        if image:
            # Center the image for better viewing
            center = self.pdf_handler.fit_mode in ["width", "height", "page"]
            self.canvas.display_image(image, center=center, from_scroll=from_auto_scroll)
    
    def _update_ui_state(self):
        """Update UI state based on current document state."""
        # Update page info
        current_page = self.pdf_handler.get_current_page_number()
        total_pages = self.pdf_handler.get_page_count()
        self.toolbar.update_page_info(current_page, total_pages)
        self.status_bar.update_page_info(current_page, total_pages)
        
        # Update navigation button states
        can_prev = self.pdf_handler.can_go_previous()
        can_next = self.pdf_handler.can_go_next()
        can_first = current_page > 1
        can_last = current_page < total_pages
        
        self.toolbar.set_navigation_state(can_prev, can_next, can_first, can_last)
    
    def _update_zoom_info(self):
        """Update zoom information display."""
        zoom_text = self.pdf_handler.get_zoom_percentage()
        self.toolbar.update_zoom_info(zoom_text)
        self.status_bar.update_zoom_info(zoom_text)
        self.status_bar.update_view_mode(self.pdf_handler.fit_mode)
    
    def run(self):
        """Start the application."""
        self.main_window.run()


def main():
    """Main entry point."""
    app = PDFViewerApp()
    app.run()


if __name__ == "__main__":
    main()
