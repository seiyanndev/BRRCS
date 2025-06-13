import pandas as pd
from typing import List, Dict, Union, Optional
import os

class ExcelLoader:
    def __init__(self, file_path: str):
        """
        Initialize ExcelLoader with the path to the Excel file.
        
        Args:
            file_path (str): Path to the Excel file (.xlsx or .csv)
        """
        self.file_path = file_path
        self.data: Optional[pd.DataFrame] = None
        self._validate_file()

    def _validate_file(self) -> None:
        """
        Validate if the file exists and has the correct extension.
        Raises FileNotFoundError or ValueError if validation fails.
        """
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File not found: {self.file_path}")
        
        file_ext = os.path.splitext(self.file_path)[1].lower()
        if file_ext not in ['.xlsx', '.csv']:
            raise ValueError("File must be either .xlsx or .csv")

    def load_data(self) -> pd.DataFrame:
        """
        Load data from Excel file into a pandas DataFrame.
        
        Returns:
            pd.DataFrame: Loaded data
        
        Raises:
            Exception: If there's an error loading the file
        """
        try:
            if self.file_path.endswith('.csv'):
                self.data = pd.read_csv(self.file_path)
            else:
                self.data = pd.read_excel(self.file_path)
            return self.data
        except Exception as e:
            raise Exception(f"Error loading file: {str(e)}")

    def get_data_as_dicts(self) -> List[Dict]:
        """
        Convert DataFrame to list of dictionaries.
        
        Returns:
            List[Dict]: List of dictionaries containing the data
        """
        if self.data is None:
            self.load_data()
        return self.data.to_dict('records')

    def get_columns(self) -> List[str]:
        """
        Get list of column names from the data.
        
        Returns:
            List[str]: List of column names
        """
        if self.data is None:
            self.load_data()
        return list(self.data.columns)

    def search_data(self, column: str, value: str) -> pd.DataFrame:
        """
        Search data in a specific column for a given value.
        
        Args:
            column (str): Column name to search in
            value (str): Value to search for
            
        Returns:
            pd.DataFrame: Filtered data matching the search criteria
        """
        if self.data is None:
            self.load_data()
        
        if column not in self.data.columns:
            raise ValueError(f"Column '{column}' not found in data")
        
        return self.data[self.data[column].astype(str).str.contains(value, case=False, na=False)]

    def get_unique_values(self, column: str) -> List[str]:
        """
        Get unique values from a specific column.
        
        Args:
            column (str): Column name to get unique values from
            
        Returns:
            List[str]: List of unique values
        """
        if self.data is None:
            self.load_data()
        
        if column not in self.data.columns:
            raise ValueError(f"Column '{column}' not found in data")
        
        return sorted(self.data[column].unique().tolist()) 