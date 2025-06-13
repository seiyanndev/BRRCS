import sys
import os
import pandas as pd

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from FUNCTIONS.excel_writer import ExcelWriter

def create_sample_excel():
    """Create a sample Excel file with resident data."""
    # Sample data
    data = {
        'First Name': ['John', 'Maria', 'James', 'Sarah', 'Michael'],
        'Middle Name': ['Santos', 'Reyes', 'Cruz', 'Garcia', 'Torres'],
        'Last Name': ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones'],
        'Age': [30, 25, 45, 28, 35],
        'Birthday': ['1993-01-15', '1998-05-20', '1978-11-30', '1995-03-10', '1988-07-25'],
        'Address': ['123 Main St', '456 Oak Ave', '789 Pine Rd', '321 Elm St', '654 Maple Dr']
    }
    
    # Create DataFrame and save to Excel
    df = pd.DataFrame(data)
    df.to_excel('residents.xlsx', index=False)
    print("Sample Excel file created: residents.xlsx")

def test_excel_writer():
    try:
        # Create sample Excel file if it doesn't exist
        if not os.path.exists('residents.xlsx'):
            create_sample_excel()

        # Initialize writer
        writer = ExcelWriter('residents.xlsx')
        
        # Test appending a new row
        new_resident = {
            'First Name': 'Alice',
            'Middle Name': 'Mendoza',
            'Last Name': 'Brown',
            'Age': 28,
            'Birthday': '1995-08-15',
            'Address': '987 Cedar Ln'
        }
        writer.append_row(new_resident)
        print("\nAppended new resident:", new_resident['First Name'])
        
        # Test updating a row
        update_data = {
            'Age': 31,
            'Address': '123 Main St Apt 4'
        }
        if writer.update_row('First Name', 'John', update_data):
            print("\nUpdated John's information")
        
        # Test getting a row
        resident = writer.get_row('First Name', 'Maria')
        if resident:
            print("\nRetrieved Maria's information:", resident)
        
        # Test deleting a row
        if writer.delete_row('First Name', 'James'):
            print("\nDeleted James's record")
        
        # Close the writer
        writer.close()
        
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        if 'writer' in locals():
            writer.close()

if __name__ == "__main__":
    test_excel_writer() 