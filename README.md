# PDF Viewer Application

A simple PDF viewer application built with Python and Tkinter, featuring page navigation, zoom controls, and a clean modular architecture.

## Features

- Open and view PDF files
- Navigate between pages (Previous/Next)
- Zoom in/out and reset zoom
- Scrollable canvas for large documents
- Clean, modular code architecture

## Project Structure

```
pdf_viewer/
├── main.py                     # Main entry point
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── src/                        # Source code
    ├── __init__.py
    ├── app.py                  # Main application controller
    ├── core/                   # Core functionality
    │   ├── __init__.py
    │   └── pdf_handler.py      # PDF document handling
    ├── ui/                     # User interface components
    │   ├── __init__.py
    │   ├── main_window.py      # Main window and toolbar
    │   └── canvas.py           # PDF display canvas
    └── utils/                  # Utility modules
        ├── __init__.py
        └── file_handler.py     # File operations
```

## Module Description

### Core (`src/core/`)
- **pdf_handler.py**: Handles PDF document operations like opening, rendering, navigation, and zoom functionality

### UI (`src/ui/`)
- **main_window.py**: Contains the main window and toolbar components with navigation and zoom controls
- **canvas.py**: Manages the scrollable canvas for displaying PDF content

### Utils (`src/utils/`)
- **file_handler.py**: Handles file operations like opening file dialogs and file validation

### Main Controller (`src/app.py`)
- **app.py**: Main application controller that coordinates between UI components and core functionality

## Installation

1. Install Python 3.7 or higher
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application:
```bash
python main.py
```

Or alternatively:
```bash
python src/app.py
```

## Controls

- **File → Open**: Open a PDF file
- **Previous/Next**: Navigate between pages
- **+/-**: Zoom in/out
- **Reset**: Reset zoom to 100%
- **Scrollbars**: Navigate large pages

## Dependencies

- **PyMuPDF**: For PDF processing and rendering
- **Pillow**: For image processing and display
- **tkinter**: For the GUI (included with Python)

## Architecture Benefits

The refactored modular architecture provides:

1. **Separation of Concerns**: Each module has a specific responsibility
2. **Maintainability**: Easier to modify and extend individual components
3. **Testability**: Components can be tested independently
4. **Reusability**: Modules can be reused in other projects
5. **Scalability**: Easy to add new features without affecting existing code
