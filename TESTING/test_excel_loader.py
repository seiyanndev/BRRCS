import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from FUNCTIONS.excel_loader import ExcelLoader

def test_excel_loader():
    try:
        # Initialize the loader with your Excel file
        loader = ExcelLoader("residents.xlsx")
        
        # Load the data
        data = loader.load_data()
        print("\nColumns in the file:", loader.get_columns())
        
        # Get data as list of dictionaries
        records = loader.get_data_as_dicts()
        print(f"\nTotal records loaded: {len(records)}")
        
        # Example search
        if 'First Name' in loader.get_columns():
            search_results = loader.search_data('First Name', 'John')
            print(f"\nSearch results for 'John': {len(search_results)} records found")
            
        # Get unique values from a column
        if 'Last Name' in loader.get_columns():
            unique_last_names = loader.get_unique_values('Last Name')
            print("\nUnique last names:", unique_last_names)
            
    except FileNotFoundError:
        print("Error: Excel file not found. Please make sure the file exists.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_excel_loader() 