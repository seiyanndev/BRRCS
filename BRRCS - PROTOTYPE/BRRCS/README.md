# Barangay 6 Resident Records and Certification System (BRRCS)

A desktop-based information management and document automation system for Barangay-level governance.

## Features
- Resident record management
- Document generation (certifications, clearances)
- Offline-first operation
- Excel-based database
- User authentication
- Search and filter capabilities

## Installation
1. Ensure Python 3.8+ is installed
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   python main.py
   ```

## Development
- `main.py`: Application entry point
- `gui/`: User interface components
- `core/`: Core business logic
- `data/`: Excel database files
- `templates/`: Document templates
- `certs/`: Generated documents

## Building Executable
```
pyinstaller --onefile --windowed main.py
```

## License
Proprietary - Barangay 6 