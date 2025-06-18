from dataclasses import dataclass
from typing import List, Dict, Any
import logging

@dataclass
class ResidentSchema:
    """Defines the schema for resident records"""
    REQUIRED_COLUMNS = {
        'resident_id': str,      # Unique identifier
        'last_name': str,        # Last name
        'first_name': str,       # First name
        'middle_name': str,      # Middle name (optional)
        'birth_date': str,       # Date of birth (YYYY-MM-DD)
        'gender': str,           # M/F
        'civil_status': str,     # Single/Married/Widowed/Divorced
        'address': str,          # Complete address
        'purok': str,           # Purok number/name
        'contact_number': str,   # Phone number (optional)
        'email': str,           # Email address (optional)
        'voter_id': str,        # Voter's ID number (optional)
        'date_registered': str,  # Date registered in barangay
        'status': str           # Active/Inactive
    }

    OPTIONAL_COLUMNS = {
        'middle_name': str,
        'contact_number': str,
        'email': str,
        'voter_id': str
    }

    @classmethod
    def get_required_columns(cls) -> List[str]:
        """Get list of required column names"""
        return [col for col in cls.REQUIRED_COLUMNS.keys() 
                if col not in cls.OPTIONAL_COLUMNS]

    @classmethod
    def get_all_columns(cls) -> List[str]:
        """Get list of all possible column names"""
        return list(cls.REQUIRED_COLUMNS.keys())

    @classmethod
    def get_column_types(cls) -> Dict[str, type]:
        """Get dictionary of column names and their expected types"""
        return cls.REQUIRED_COLUMNS.copy()

class SchemaValidator:
    """Validates Excel file structure against required schema"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.schema = ResidentSchema()

    def validate_headers(self, headers: List[str]) -> tuple[bool, List[str]]:
        """
        Validate if the Excel file headers match the required schema.
        
        Args:
            headers: List of column headers from Excel file
            
        Returns:
            tuple: (is_valid, list of missing columns)
        """
        required_columns = self.schema.get_required_columns()
        missing_columns = [col for col in required_columns if col not in headers]
        
        if missing_columns:
            self.logger.error(f"Missing required columns: {missing_columns}")
            return False, missing_columns
            
        return True, []

    def validate_data_types(self, df) -> tuple[bool, List[str]]:
        """
        Validate if the data types in the DataFrame match the schema.
        
        Args:
            df: pandas DataFrame containing resident records
            
        Returns:
            tuple: (is_valid, list of columns with type mismatches)
        """
        type_mismatches = []
        expected_types = self.schema.get_column_types()
        
        for column, expected_type in expected_types.items():
            if column in df.columns:
                # Check if the column's data type matches the expected type
                if not all(isinstance(x, expected_type) for x in df[column].dropna()):
                    type_mismatches.append(column)
                    self.logger.error(f"Type mismatch in column: {column}")
        
        return len(type_mismatches) == 0, type_mismatches

    def validate_record(self, record: Dict[str, Any]) -> tuple[bool, List[str]]:
        """
        Validate a single resident record against the schema.
        
        Args:
            record: Dictionary containing resident data
            
        Returns:
            tuple: (is_valid, list of validation errors)
        """
        errors = []
        required_columns = self.schema.get_required_columns()
        
        # Check for missing required fields
        for column in required_columns:
            if column not in record or not record[column]:
                errors.append(f"Missing required field: {column}")
                
        # Check data types
        for column, value in record.items():
            if column in self.schema.REQUIRED_COLUMNS:
                expected_type = self.schema.REQUIRED_COLUMNS[column]
                if value is not None and not isinstance(value, expected_type):
                    errors.append(f"Invalid type for {column}: expected {expected_type.__name__}")
        
        return len(errors) == 0, errors 