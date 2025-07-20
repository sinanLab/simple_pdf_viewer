"""
PDF handling functionality for the PDF viewer application.
"""
import fitz  # PyMuPDF
from PIL import Image, ImageTk
from typing import Optional, Tuple


class PDFHandler:
    """Handles PDF document operations and rendering."""
    
    def __init__(self):
        self.document: Optional[fitz.Document] = None
        self.current_page: int = 0
        self.zoom_factor: float = 1.0
    
    def open_document(self, file_path: str) -> bool:
        """
        Open a PDF document.
        
        Args:
            file_path (str): Path to the PDF file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.document = fitz.open(file_path)
            self.current_page = 0
            self.zoom_factor = 1.0
            return True
        except Exception as e:
            print(f"Error opening PDF: {e}")
            return False
    
    def close_document(self):
        """Close the current document."""
        if self.document:
            self.document.close()
            self.document = None
            self.current_page = 0
            self.zoom_factor = 1.0
    
    def get_page_count(self) -> int:
        """Get total number of pages in the document."""
        return len(self.document) if self.document else 0
    
    def get_current_page_number(self) -> int:
        """Get current page number (1-indexed)."""
        return self.current_page + 1
    
    def can_go_previous(self) -> bool:
        """Check if we can go to previous page."""
        return self.document is not None and self.current_page > 0
    
    def can_go_next(self) -> bool:
        """Check if we can go to next page."""
        return (self.document is not None and 
                self.current_page < len(self.document) - 1)
    
    def go_to_previous_page(self) -> bool:
        """Go to previous page."""
        if self.can_go_previous():
            self.current_page -= 1
            return True
        return False
    
    def go_to_next_page(self) -> bool:
        """Go to next page."""
        if self.can_go_next():
            self.current_page += 1
            return True
        return False
    
    def set_zoom_factor(self, zoom_factor: float):
        """Set zoom factor."""
        self.zoom_factor = max(0.1, zoom_factor)  # Minimum zoom of 0.1
    
    def zoom_in(self, factor: float = 1.2):
        """Zoom in by the specified factor."""
        self.zoom_factor *= factor
    
    def zoom_out(self, factor: float = 1.2):
        """Zoom out by the specified factor."""
        self.zoom_factor /= factor
        self.zoom_factor = max(0.1, self.zoom_factor)  # Minimum zoom of 0.1
    
    def reset_zoom(self):
        """Reset zoom to 100%."""
        self.zoom_factor = 1.0
    
    def render_current_page(self) -> Optional[ImageTk.PhotoImage]:
        """
        Render the current page as an ImageTk.PhotoImage.
        
        Returns:
            ImageTk.PhotoImage or None if no document is loaded
        """
        if not self.document or not (0 <= self.current_page < len(self.document)):
            return None
        
        try:
            # Get the page
            page = self.document.load_page(self.current_page)
            zoom_matrix = fitz.Matrix(self.zoom_factor, self.zoom_factor)
            pix = page.get_pixmap(matrix=zoom_matrix)
            
            # Convert to ImageTk
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            img_tk = ImageTk.PhotoImage(img)
            
            return img_tk
        except Exception as e:
            print(f"Error rendering page: {e}")
            return None
    
    def get_page_size(self) -> Tuple[int, int]:
        """
        Get the size of the current page in pixels.
        
        Returns:
            Tuple[int, int]: (width, height) or (0, 0) if no document
        """
        if not self.document or not (0 <= self.current_page < len(self.document)):
            return (0, 0)
        
        try:
            page = self.document.load_page(self.current_page)
            zoom_matrix = fitz.Matrix(self.zoom_factor, self.zoom_factor)
            pix = page.get_pixmap(matrix=zoom_matrix)
            return (pix.width, pix.height)
        except Exception:
            return (0, 0)
