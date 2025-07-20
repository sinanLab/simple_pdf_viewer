"""
File handling utilities for the PDF viewer application.
"""
from tkinter import filedialog
from typing import Optional
import os


class FileHandler:
    """Handles file operations for the PDF viewer."""
    
    @staticmethod
    def open_pdf_dialog() -> Optional[str]:
        """
        Open a file dialog to select a PDF file.
        
        Returns:
            str or None: Path to selected PDF file, or None if cancelled
        """
        file_path = filedialog.askopenfilename(
            title="Open PDF File",
            filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")]
        )
        return file_path if file_path else None
    
    @staticmethod
    def is_valid_pdf(file_path: str) -> bool:
        """
        Check if the file is a valid PDF file.
        
        Args:
            file_path (str): Path to the file to check
            
        Returns:
            bool: True if valid PDF, False otherwise
        """
        if not os.path.exists(file_path):
            return False
        
        if not file_path.lower().endswith('.pdf'):
            return False
        
        try:
            # Basic check - read first few bytes to check PDF header
            with open(file_path, 'rb') as file:
                header = file.read(4)
                return header == b'%PDF'
        except Exception:
            return False
    
    @staticmethod
    def get_file_info(file_path: str) -> dict:
        """
        Get basic file information.
        
        Args:
            file_path (str): Path to the file
            
        Returns:
            dict: File information including name, size, and path
        """
        if not os.path.exists(file_path):
            return {}
        
        try:
            stat = os.stat(file_path)
            return {
                'name': os.path.basename(file_path),
                'path': file_path,
                'size': stat.st_size,
                'size_mb': round(stat.st_size / (1024 * 1024), 2),
                'modified': stat.st_mtime
            }
        except Exception:
            return {}
