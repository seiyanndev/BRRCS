from typing import List, Dict, Optional
import pandas as pd
import os
from dataclasses import dataclass
from enum import Enum

class ValidationSeverity(Enum):
    """Severity levels for validation issues."""
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"

@dataclass
class ValidationIssue:
    """Class to represent a validation issue."""
    message: str
    severity: ValidationSeverity
    column: Optional[str] = None
    expected: Optional[str] = None
    found: Optional[str] = None

class TemplateValidator:
    """Validates Excel file structure against expected template."""
    
    REQUIRED_COLUMNS = [
        'First Name',
        'Middle Name',
        'Last Name',
        'Age',
        'Birthday',
        'Address'
    ]
    
    COLUMN_TYPES = {
        'First Name': str,
        'Middle Name': str,
        'Last Name': str,
        'Age': int,
        'Birthday': str,
        'Address': str
    }
    
    def __init__(self, file_path: str):
        """
        Initialize the validator with the Excel file path.
        
        Args:
            file_path (str): Path to the Excel file to validate
        """
        self.file_path = file_path
        self.issues: List[ValidationIssue] = []
        self._validate_file_exists()
    
    def _validate_file_exists(self) -> None:
        """Validate that the file exists."""
        if not os.path.exists(self.file_path):
            self.issues.append(ValidationIssue(
                message=f"File not found: {self.file_path}",
                severity=ValidationSeverity.ERROR
            ))
    
    def validate(self) -> List[ValidationIssue]:
        """
        Perform all validations on the Excel file.
        
        Returns:
            List[ValidationIssue]: List of validation issues found
        """
        if not os.path.exists(self.file_path):
            return self.issues
            
        try:
            # Load the Excel file
            df = pd.read_excel(self.file_path)
            
            # Validate headers
            self._validate_headers(df.columns)
            
            # Validate data types
            self._validate_data_types(df)
            
            # Validate required values
            self._validate_required_values(df)
            
            # Validate data formats
            self._validate_data_formats(df)
            
        except Exception as e:
            self.issues.append(ValidationIssue(
                message=f"Error reading file: {str(e)}",
                severity=ValidationSeverity.ERROR
            ))
        
        return self.issues
    
    def _validate_headers(self, columns: pd.Index) -> None:
        """
        Validate that all required columns are present.
        
        Args:
            columns (pd.Index): DataFrame columns to validate
        """
        found_columns = set(columns)
        required_columns = set(self.REQUIRED_COLUMNS)
        
        # Check for missing columns
        missing_columns = required_columns - found_columns
        for col in missing_columns:
            self.issues.append(ValidationIssue(
                message=f"Missing required column: {col}",
                severity=ValidationSeverity.ERROR,
                column=col,
                expected=col,
                found=None
            ))
        
        # Check for extra columns
        extra_columns = found_columns - required_columns
        for col in extra_columns:
            self.issues.append(ValidationIssue(
                message=f"Extra column found: {col}",
                severity=ValidationSeverity.WARNING,
                column=col,
                expected=None,
                found=col
            ))
    
    def _validate_data_types(self, df: pd.DataFrame) -> None:
        """
        Validate that data types match expected types.
        
        Args:
            df (pd.DataFrame): DataFrame to validate
        """
        for col, expected_type in self.COLUMN_TYPES.items():
            if col not in df.columns:
                continue
                
            try:
                if expected_type == int:
                    # Try to convert to int, but allow NaN values
                    df[col].fillna(-1).astype(int)
                elif expected_type == str:
                    # Convert to string, but allow NaN values
                    df[col].fillna('').astype(str)
            except Exception as e:
                self.issues.append(ValidationIssue(
                    message=f"Invalid data type in column {col}: {str(e)}",
                    severity=ValidationSeverity.ERROR,
                    column=col,
                    expected=str(expected_type),
                    found=str(df[col].dtype)
                ))
    
    def _validate_required_values(self, df: pd.DataFrame) -> None:
        """
        Validate that required columns have no empty values.
        
        Args:
            df (pd.DataFrame): DataFrame to validate
        """
        required_columns = ['First Name', 'Last Name', 'Age', 'Birthday']
        
        for col in required_columns:
            if col not in df.columns:
                continue
                
            empty_count = df[col].isna().sum()
            if empty_count > 0:
                self.issues.append(ValidationIssue(
                    message=f"Column {col} has {empty_count} empty values",
                    severity=ValidationSeverity.ERROR,
                    column=col
                ))
    
    def _validate_data_formats(self, df: pd.DataFrame) -> None:
        """
        Validate specific data formats (e.g., date format, age range).
        
        Args:
            df (pd.DataFrame): DataFrame to validate
        """
        # Validate birthday format (YYYY-MM-DD)
        if 'Birthday' in df.columns:
            try:
                pd.to_datetime(df['Birthday'], format='%Y-%m-%d')
            except Exception as e:
                self.issues.append(ValidationIssue(
                    message=f"Invalid date format in Birthday column: {str(e)}",
                    severity=ValidationSeverity.ERROR,
                    column='Birthday',
                    expected='YYYY-MM-DD'
                ))
        
        # Validate age range (0-120)
        if 'Age' in df.columns:
            invalid_ages = df[df['Age'].between(0, 120) == False]
            if not invalid_ages.empty:
                self.issues.append(ValidationIssue(
                    message=f"Found {len(invalid_ages)} invalid ages (should be between 0 and 120)",
                    severity=ValidationSeverity.ERROR,
                    column='Age'
                ))
    
    def has_errors(self) -> bool:
        """
        Check if there are any validation errors.
        
        Returns:
            bool: True if there are any ERROR severity issues
        """
        return any(issue.severity == ValidationSeverity.ERROR for issue in self.issues)
    
    def has_warnings(self) -> bool:
        """
        Check if there are any validation warnings.
        
        Returns:
            bool: True if there are any WARNING severity issues
        """
        return any(issue.severity == ValidationSeverity.WARNING for issue in self.issues)
    
    def get_errors(self) -> List[ValidationIssue]:
        """
        Get all validation errors.
        
        Returns:
            List[ValidationIssue]: List of ERROR severity issues
        """
        return [issue for issue in self.issues if issue.severity == ValidationSeverity.ERROR]
    
    def get_warnings(self) -> List[ValidationIssue]:
        """
        Get all validation warnings.
        
        Returns:
            List[ValidationIssue]: List of WARNING severity issues
        """
        return [issue for issue in self.issues if issue.severity == ValidationSeverity.WARNING] 