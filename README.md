# Barangay 6 Resident Records and Certification System (BRRCS)

A Python desktop application for managing resident information in Barangay 6. The system uses Excel as the primary data source and features a Tkinter GUI. It supports PDF export, live data interaction, simple analytics, and secure role-based access.

## Project Structure

```
BRRCS/
├── FUNCTIONS/
│   ├── excel_loader.py
│   ├── excel_writer.py
│   ├── template_validator.py
│   └── file_locker.py
├── GUI/
│   ├── main_window.py
│   ├── login_window.py
│   └── resident_form.py
├── TESTING/
│   ├── test_excel_loader.py
│   ├── test_excel_writer.py
│   ├── test_template_validator.py
│   └── test_file_locker.py
├── DATA/
│   └── residents.xlsx
├── requirements.txt
└── README.md
```

## Setup Instructions

1. Install Python 3.8 or higher
2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the test files to verify functionality:
   ```bash
   python TESTING/test_excel_loader.py
   python TESTING/test_excel_writer.py
   python TESTING/test_template_validator.py
   python TESTING/test_file_locker.py
   ```

## Features

- Excel-based data storage
- Tkinter GUI interface
- PDF export functionality
- Live data interaction
- Simple analytics
- Secure role-based access
- Template validation with detailed error reporting
- File locking to prevent simultaneous edits

## Data Structure

The system uses Excel files with the following structure:

### Required Columns
- First Name (text)
- Last Name (text)
- Age (number)
- Birthday (date in YYYY-MM-DD format)

### Optional Columns
- Address (text)
- Contact Number (text)
- Email (text)
- Occupation (text)
- Civil Status (text)
- Gender (text)

## Template Validation

The system includes a template validator that ensures Excel files have the correct structure and data types. The validator checks for:

1. Required columns
2. Data types
3. Required values
4. Data formats

Validation issues are categorized as:
- ERROR: Critical issues that must be fixed
- WARNING: Potential issues that should be reviewed
- INFO: Informational messages

## File Locking

The system implements a file locking mechanism to prevent simultaneous edits to Excel files. Features include:

1. Process-based locking
   - Tracks which process has the file locked
   - Prevents multiple processes from editing simultaneously
   - Automatically releases locks when processes end

2. Stale lock detection
   - Detects and removes stale locks (default 5-minute timeout)
   - Handles crashed processes and system failures
   - Ensures files remain accessible

3. Lock information
   - Tracks which user has the file locked
   - Records lock acquisition time
   - Provides detailed process information

4. Context manager support
   - Easy-to-use `with` statement syntax
   - Automatic lock release
   - Exception-safe locking

Example usage:
```python
with FileLocker('residents.xlsx') as locker:
    # File is locked here
    # Perform operations on the file
    pass
# Lock is automatically released
```

## Security

The system implements role-based access control with the following roles:
- Admin: Full access to all features
- Staff: Can view and edit resident records
- Viewer: Can only view resident records

## Dependencies

- Python 3.8+
- pandas
- openpyxl
- tkinter
- reportlab
- psutil

## License

This project is licensed under the MIT License - see the LICENSE file for details. 