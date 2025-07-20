"""
Main PDF Viewer application controller.
"""
import sys
import os

# Add src directory to path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.pdf_handler import PDFHandler
from src.ui.main_window import MainWindow, Toolbar
from src.ui.canvas import PDFCanvas
from src.utils.file_handler import FileHandler


class PDFViewerApp:
    """Main PDF Viewer application controller."""
    
    def __init__(self):
        # Initialize components
        self.pdf_handler = PDFHandler()
        self.file_handler = FileHandler()
        
        # Create main window
        self.main_window = MainWindow("PDF Viewer", "800x600")
        
        # Create toolbar
        self.toolbar = Toolbar(self.main_window.root)
        
        # Create canvas
        self.canvas = PDFCanvas(self.main_window.root)
        
        # Setup event handlers
        self._setup_event_handlers()
    
    def _setup_event_handlers(self):
        """Setup event handlers for UI components."""
        # Main window events
        self.main_window.set_open_callback(self._open_pdf)
        self.main_window.set_exit_callback(self._exit_app)
        
        # Toolbar events
        self.toolbar.set_prev_page_callback(self._prev_page)
        self.toolbar.set_next_page_callback(self._next_page)
        self.toolbar.set_zoom_in_callback(self._zoom_in)
        self.toolbar.set_zoom_out_callback(self._zoom_out)
        self.toolbar.set_reset_zoom_callback(self._reset_zoom)
    
    def _open_pdf(self):
        """Handle open PDF action."""
        file_path = self.file_handler.open_pdf_dialog()
        if file_path:
            if self.file_handler.is_valid_pdf(file_path):
                if self.pdf_handler.open_document(file_path):
                    self._update_display()
                    self._update_ui_state()
                    # Set window title to include filename
                    filename = os.path.basename(file_path)
                    self.main_window.root.title(f"PDF Viewer - {filename}")
                else:
                    print("Error: Could not open PDF file")
            else:
                print("Error: Invalid PDF file")
    
    def _exit_app(self):
        """Handle exit application action."""
        self.pdf_handler.close_document()
        self.main_window.quit()
    
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
    
    def _zoom_in(self):
        """Handle zoom in action."""
        self.pdf_handler.zoom_in()
        self._update_display()
    
    def _zoom_out(self):
        """Handle zoom out action."""
        self.pdf_handler.zoom_out()
        self._update_display()
    
    def _reset_zoom(self):
        """Handle reset zoom action."""
        self.pdf_handler.reset_zoom()
        self._update_display()
    
    def _update_display(self):
        """Update the PDF display."""
        image = self.pdf_handler.render_current_page()
        if image:
            self.canvas.display_image(image)
            # Scroll to top for new pages
            self.canvas.scroll_to_top()
    
    def _update_ui_state(self):
        """Update UI state based on current document state."""
        # Update page info
        current_page = self.pdf_handler.get_current_page_number()
        total_pages = self.pdf_handler.get_page_count()
        self.toolbar.update_page_info(current_page, total_pages)
        
        # Update button states
        self.toolbar.set_prev_button_state(self.pdf_handler.can_go_previous())
        self.toolbar.set_next_button_state(self.pdf_handler.can_go_next())
    
    def run(self):
        """Start the application."""
        self.main_window.run()


def main():
    """Main entry point."""
    app = PDFViewerApp()
    app.run()


if __name__ == "__main__":
    main()
