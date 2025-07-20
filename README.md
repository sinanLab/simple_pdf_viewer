# Enhanced PDF Viewer Application

A feature-rich PDF viewer application built with Python and Tkinter, featuring advanced page scaling, navigation, zoom controls, search functionality, and a professional modular architecture.

## ✨ Features

### Core Functionality
- **Open and view PDF files** with high-quality rendering
- **Smart page scaling** - Automatically fits pages to window size
- **Multiple fit modes**: Fit Width, Fit Height, Fit Page, Actual Size
- **Page navigation** with Previous/Next, First/Last page controls
- **Direct page navigation** - Jump to any page number
- **Advanced zoom controls** - Zoom in/out with percentage display

### Advanced Features
- **Page rotation** - Rotate pages by 90° increments
- **Text search** - Search for text within PDF pages with highlighting
- **Keyboard shortcuts** - Full keyboard navigation support
- **Mouse wheel scrolling** - Smooth scrolling with mouse wheel
- **Middle-button panning** - Drag to pan around large documents
- **Status bar** - Real-time display of document and view information
- **Professional UI** - Modern interface with organized toolbar sections

### User Experience
- **Responsive design** - Automatically adapts to window resizing
- **Smooth scrolling** - Enhanced scrollbars with proper scroll regions
- **Centered display** - Pages are centered for optimal viewing
- **Memory efficient** - Proper image reference management
- **Error handling** - Graceful error handling with user feedback

## 🏗️ Project Structure

```
pdf_viewer/
├── main.py                     # Main entry point
├── requirements.txt            # Python dependencies
├── README.md                   # This documentation
└── src/                        # Source code
    ├── __init__.py
    ├── app.py                  # Main application controller
    ├── core/                   # Core functionality
    │   ├── __init__.py
    │   └── pdf_handler.py      # PDF document handling & rendering
    ├── ui/                     # User interface components
    │   ├── __init__.py
    │   ├── main_window.py      # Main window & enhanced toolbar
    │   ├── canvas.py           # Advanced PDF display canvas
    │   └── status_bar.py       # Status bar component
    └── utils/                  # Utility modules
        ├── __init__.py
        └── file_handler.py     # File operations & validation
```

## 📋 Module Description

### Core (`src/core/`)
- **pdf_handler.py**: Advanced PDF document operations including:
  - Multi-mode page rendering (fit width/height/page/actual)
  - Zoom control with bounds (10% - 500%)
  - Page rotation (0°, 90°, 180°, 270°)
  - Text search functionality
  - Smart scaling calculations

### UI (`src/ui/`)
- **main_window.py**: Main application window with:
  - Enhanced menu system with keyboard shortcuts
  - Professional toolbar with organized sections
  - Event handling and callback management
- **canvas.py**: Advanced PDF display canvas featuring:
  - Mouse wheel and keyboard scrolling
  - Middle-button panning
  - Smart image centering
  - Search result highlighting
- **status_bar.py**: Information display bar showing:
  - Document information (filename, size)
  - Current page and total pages
  - Zoom level and view mode
  - Status messages

### Utils (`src/utils/`)
- **file_handler.py**: File operations including:
  - PDF file validation
  - File information extraction
  - Dialog management

### Main Controller (`src/app.py`)
- **app.py**: Enhanced application controller that:
  - Coordinates all components
  - Manages application state
  - Handles all user interactions
  - Implements keyboard shortcuts

## 🚀 Installation

1. **Install Python 3.7 or higher**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Usage

**Run the application:**
```bash
python main.py
```

**Or alternatively:**
```bash
python src/app.py
```

## ⌨️ Controls & Shortcuts

### File Operations
- **Ctrl+O**: Open PDF file
- **Ctrl+Q**: Exit application

### Navigation
- **Page Up / ◀**: Previous page
- **Page Down / ▶**: Next page
- **Ctrl+Home / ⏮**: First page
- **Ctrl+End / ⏭**: Last page
- **Ctrl+G**: Go to specific page

### Zoom & View
- **Ctrl++ / Ctrl+=**: Zoom in
- **Ctrl+-**: Zoom out
- **Ctrl+0**: Actual size (100%)
- **Ctrl+1**: Fit width
- **Ctrl+2**: Fit height
- **Ctrl+3**: Fit page

### Tools
- **Ctrl+R**: Rotate page clockwise
- **Ctrl+F**: Focus search box
- **F3**: Find next (planned)
- **Shift+F3**: Find previous (planned)

### Mouse Controls
- **Mouse Wheel**: Vertical scrolling
- **Shift+Mouse Wheel**: Horizontal scrolling
- **Middle Button Drag**: Pan around document
- **Left Click**: Focus canvas for keyboard events

## 🎛️ Toolbar Sections

### Navigation
- First/Previous/Next/Last page buttons
- Page number entry field
- Direct page navigation

### Zoom
- Zoom in/out buttons
- Current zoom percentage display
- Quick zoom controls

### Fit Options
- **Width**: Fit page width to window
- **Height**: Fit page height to window  
- **Page**: Fit entire page to window
- **100%**: Show actual page size

### Tools
- **Rotate**: Rotate page 90° clockwise
- **Search**: Find text in current page

## 📊 Status Bar Information

- **File Info**: Current document name and size
- **Page Info**: Current page / total pages
- **Zoom Info**: Current zoom percentage
- **View Mode**: Current fit mode
- **Status**: Application status messages

## 📦 Dependencies

- **PyMuPDF (fitz)**: PDF processing and rendering
- **Pillow (PIL)**: Image processing and display
- **tkinter**: GUI framework (included with Python)

## 🏛️ Architecture Benefits

The enhanced modular architecture provides:

1. **🎯 Separation of Concerns**: Each module has a specific responsibility
2. **🔧 Maintainability**: Easy to modify and extend individual components
3. **🧪 Testability**: Components can be tested independently
4. **♻️ Reusability**: Modules can be reused in other projects
5. **📈 Scalability**: Easy to add new features without affecting existing code
6. **🎨 Professional UI**: Modern, organized interface design
7. **⚡ Performance**: Efficient rendering and memory management

## 🔮 Future Enhancements

Potential features for future development:
- **Bookmarks support**
- **Annotation tools**
- **Print functionality**
- **Full document search** (all pages)
- **Thumbnail navigation panel**
- **Recent files menu**
- **Dark theme support**
- **Multi-tab interface**
