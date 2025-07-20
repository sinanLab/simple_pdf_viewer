"""
PDF handling functionality for the PDF viewer application.
"""
import fitz  # PyMuPDF
from PIL import Image, ImageTk
from typing import Optional, Tuple, List
import math


class PDFHandler:
    """Handles PDF document operations and rendering."""
    
    def __init__(self):
        self.document: Optional[fitz.Document] = None
        self.current_page: int = 0
        self.zoom_factor: float = 1.0
        self.rotation: int = 0  # 0, 90, 180, 270 degrees
        self.fit_mode: str = "width"  # "width", "height", "page", "actual"
        self.canvas_size: Tuple[int, int] = (800, 600)
        self.page_margins: int = 20
    
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
            self.rotation = 0
            self.fit_mode = "width"
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
            self.rotation = 0
    
    def set_canvas_size(self, width: int, height: int):
        """Set the canvas size for fit calculations."""
        self.canvas_size = (width, height)
    
    def get_page_count(self) -> int:
        """Get total number of pages in the document."""
        return len(self.document) if self.document else 0
    
    def get_current_page_number(self) -> int:
        """Get current page number (1-indexed)."""
        return self.current_page + 1
    
    def go_to_page(self, page_number: int) -> bool:
        """Go to specific page (1-indexed)."""
        if self.document and 1 <= page_number <= len(self.document):
            self.current_page = page_number - 1
            return True
        return False
    
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
    
    def go_to_first_page(self) -> bool:
        """Go to first page."""
        if self.document and len(self.document) > 0:
            self.current_page = 0
            return True
        return False
    
    def go_to_last_page(self) -> bool:
        """Go to last page."""
        if self.document and len(self.document) > 0:
            self.current_page = len(self.document) - 1
            return True
        return False
    
    def set_zoom_factor(self, zoom_factor: float):
        """Set zoom factor."""
        self.zoom_factor = max(0.1, min(5.0, zoom_factor))  # Min 0.1, Max 5.0
    
    def zoom_in(self, factor: float = 1.2):
        """Zoom in by the specified factor."""
        self.zoom_factor = min(5.0, self.zoom_factor * factor)
    
    def zoom_out(self, factor: float = 1.2):
        """Zoom out by the specified factor."""
        self.zoom_factor = max(0.1, self.zoom_factor / factor)
    
    def reset_zoom(self):
        """Reset zoom to 100%."""
        self.zoom_factor = 1.0
    
    def set_fit_mode(self, mode: str):
        """Set fit mode: 'width', 'height', 'page', 'actual'."""
        if mode in ["width", "height", "page", "actual"]:
            self.fit_mode = mode
            self._calculate_fit_zoom()
    
    def _calculate_fit_zoom(self):
        """Calculate zoom factor based on fit mode."""
        if not self.document or not (0 <= self.current_page < len(self.document)):
            return
        
        try:
            page = self.document.load_page(self.current_page)
            page_rect = page.rect
            
            # Apply rotation
            if self.rotation == 90 or self.rotation == 270:
                page_width, page_height = page_rect.height, page_rect.width
            else:
                page_width, page_height = page_rect.width, page_rect.height
            
            canvas_width = self.canvas_size[0] - 2 * self.page_margins
            canvas_height = self.canvas_size[1] - 2 * self.page_margins
            
            if self.fit_mode == "width":
                self.zoom_factor = canvas_width / page_width
            elif self.fit_mode == "height":
                self.zoom_factor = canvas_height / page_height
            elif self.fit_mode == "page":
                width_scale = canvas_width / page_width
                height_scale = canvas_height / page_height
                self.zoom_factor = min(width_scale, height_scale)
            elif self.fit_mode == "actual":
                self.zoom_factor = 1.0
            
            # Ensure zoom is within bounds
            self.zoom_factor = max(0.1, min(5.0, self.zoom_factor))
        except Exception:
            self.zoom_factor = 1.0
    
    def rotate_page(self, degrees: int = 90):
        """Rotate page by degrees (90, 180, 270)."""
        self.rotation = (self.rotation + degrees) % 360
    
    def reset_rotation(self):
        """Reset page rotation."""
        self.rotation = 0
    
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
            
            # Apply rotation
            if self.rotation != 0:
                rotation_matrix = fitz.Matrix(1, 0, 0, 1, 0, 0)
                rotation_matrix = rotation_matrix.prerotate(self.rotation)
            else:
                rotation_matrix = fitz.Matrix(1, 0, 0, 1, 0, 0)
            
            # Apply zoom
            zoom_matrix = fitz.Matrix(self.zoom_factor, self.zoom_factor)
            final_matrix = rotation_matrix * zoom_matrix
            
            # Render page
            pix = page.get_pixmap(matrix=final_matrix, alpha=False)
            
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
            
            # Apply rotation
            if self.rotation != 0:
                rotation_matrix = fitz.Matrix(1, 0, 0, 1, 0, 0)
                rotation_matrix = rotation_matrix.prerotate(self.rotation)
            else:
                rotation_matrix = fitz.Matrix(1, 0, 0, 1, 0, 0)
            
            # Apply zoom
            zoom_matrix = fitz.Matrix(self.zoom_factor, self.zoom_factor)
            final_matrix = rotation_matrix * zoom_matrix
            
            pix = page.get_pixmap(matrix=final_matrix, alpha=False)
            return (pix.width, pix.height)
        except Exception:
            return (0, 0)
    
    def get_page_info(self) -> dict:
        """Get information about the current page."""
        if not self.document or not (0 <= self.current_page < len(self.document)):
            return {}
        
        try:
            page = self.document.load_page(self.current_page)
            rect = page.rect
            return {
                'page_number': self.current_page + 1,
                'total_pages': len(self.document),
                'width': rect.width,
                'height': rect.height,
                'rotation': self.rotation,
                'zoom': round(self.zoom_factor * 100, 1),
                'fit_mode': self.fit_mode
            }
        except Exception:
            return {}
    
    def search_text(self, text: str, case_sensitive: bool = False) -> List[dict]:
        """
        Search for text in the current page.
        
        Args:
            text (str): Text to search for
            case_sensitive (bool): Whether search is case sensitive
            
        Returns:
            List[dict]: List of found text instances with positions
        """
        if not self.document or not text:
            return []
        
        try:
            page = self.document.load_page(self.current_page)
            flags = 0 if case_sensitive else fitz.TEXT_DEHYPHENATE
            
            text_instances = page.search_for(text, flags=flags)
            results = []
            
            for i, rect in enumerate(text_instances):
                results.append({
                    'text': text,
                    'page': self.current_page + 1,
                    'instance': i + 1,
                    'rect': (rect.x0, rect.y0, rect.x1, rect.y1)
                })
            
            return results
        except Exception as e:
            print(f"Error searching text: {e}")
            return []
    
    def get_zoom_percentage(self) -> str:
        """Get current zoom as percentage string."""
        return f"{round(self.zoom_factor * 100)}%"
