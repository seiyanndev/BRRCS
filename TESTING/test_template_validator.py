import sys
import os
import pandas as pd
from datetime import datetime

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from FUNCTIONS.template_validator import TemplateValidator, ValidationSeverity

def create_test_files():
    """Create test Excel files with various validation scenarios."""
    # Create a valid file
    valid_data = {
        'First Name': ['John', 'Maria'],
        'Middle Name': ['Santos', 'Reyes'],
        'Last Name': ['Smith', 'Johnson'],
        'Age': [30, 25],
        'Birthday': ['1993-01-15', '1998-05-20'],
        'Address': ['123 Main St', '456 Oak Ave']
    }
    pd.DataFrame(valid_data).to_excel('valid_residents.xlsx', index=False)
    
    # Create a file with missing columns
    missing_cols_data = {
        'First Name': ['John', 'Maria'],
        'Last Name': ['Smith', 'Johnson'],
        'Age': [30, 25]
    }
    pd.DataFrame(missing_cols_data).to_excel('missing_cols.xlsx', index=False)
    
    # Create a file with invalid data types
    invalid_types_data = {
        'First Name': ['John', 'Maria'],
        'Middle Name': ['Santos', 'Reyes'],
        'Last Name': ['Smith', 'Johnson'],
        'Age': ['thirty', 'twenty-five'],  # Should be integers
        'Birthday': ['1993-01-15', '1998-05-20'],
        'Address': ['123 Main St', '456 Oak Ave']
    }
    pd.DataFrame(invalid_types_data).to_excel('invalid_types.xlsx', index=False)
    
    # Create a file with invalid formats
    invalid_formats_data = {
        'First Name': ['John', 'Maria'],
        'Middle Name': ['Santos', 'Reyes'],
        'Last Name': ['Smith', 'Johnson'],
        'Age': [150, -5],  # Invalid ages
        'Birthday': ['01-15-1993', '05-20-1998'],  # Wrong date format
        'Address': ['123 Main St', '456 Oak Ave']
    }
    pd.DataFrame(invalid_formats_data).to_excel('invalid_formats.xlsx', index=False)

def test_template_validator():
    """Test the template validator with various scenarios."""
    # Create test files
    create_test_files()
    
    # Test valid file
    print("\nTesting valid file:")
    validator = TemplateValidator('valid_residents.xlsx')
    issues = validator.validate()
    print(f"Found {len(issues)} issues")
    for issue in issues:
        print(f"- {issue.severity.value}: {issue.message}")
    
    # Test missing columns
    print("\nTesting file with missing columns:")
    validator = TemplateValidator('missing_cols.xlsx')
    issues = validator.validate()
    print(f"Found {len(issues)} issues")
    for issue in issues:
        print(f"- {issue.severity.value}: {issue.message}")
    
    # Test invalid data types
    print("\nTesting file with invalid data types:")
    validator = TemplateValidator('invalid_types.xlsx')
    issues = validator.validate()
    print(f"Found {len(issues)} issues")
    for issue in issues:
        print(f"- {issue.severity.value}: {issue.message}")
    
    # Test invalid formats
    print("\nTesting file with invalid formats:")
    validator = TemplateValidator('invalid_formats.xlsx')
    issues = validator.validate()
    print(f"Found {len(issues)} issues")
    for issue in issues:
        print(f"- {issue.severity.value}: {issue.message}")
    
    # Test non-existent file
    print("\nTesting non-existent file:")
    validator = TemplateValidator('nonexistent.xlsx')
    issues = validator.validate()
    print(f"Found {len(issues)} issues")
    for issue in issues:
        print(f"- {issue.severity.value}: {issue.message}")

if __name__ == "__main__":
    test_template_validator() 