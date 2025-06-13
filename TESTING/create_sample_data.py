import sys
import os
import pandas as pd
from datetime import datetime, timedelta
import random

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def generate_sample_data(num_records=10):
    """Generate sample resident data."""
    # Sample first names
    first_names = ['John', 'Maria', 'James', 'Sarah', 'Michael', 'Anna', 'David', 'Emma', 'Robert', 'Sophia']
    
    # Sample middle names
    middle_names = ['Santos', 'Reyes', 'Cruz', 'Garcia', 'Torres', 'Aquino', 'Mendoza', 'Ramos', 'Flores', 'Dela Cruz']
    
    # Sample last names
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez']
    
    # Sample addresses
    streets = ['Main St', 'Oak Ave', 'Pine Rd', 'Maple Dr', 'Cedar Ln', 'Elm St', 'Birch Way', 'Willow Rd', 'Spruce St', 'Cypress Ave']
    barangays = ['Barangay 1', 'Barangay 2', 'Barangay 3', 'Barangay 4', 'Barangay 5', 'Barangay 6']
    
    # Generate data
    data = {
        'First Name': [],
        'Middle Name': [],
        'Last Name': [],
        'Age': [],
        'Birthday': [],
        'Address': []
    }
    
    # Generate random dates for birthdays (ages between 18 and 80)
    start_date = datetime.now() - timedelta(days=365*80)
    end_date = datetime.now() - timedelta(days=365*18)
    
    for _ in range(num_records):
        data['First Name'].append(random.choice(first_names))
        data['Middle Name'].append(random.choice(middle_names))
        data['Last Name'].append(random.choice(last_names))
        
        # Generate random birthday
        random_days = random.randint(0, (end_date - start_date).days)
        birthday = start_date + timedelta(days=random_days)
        data['Birthday'].append(birthday.strftime('%Y-%m-%d'))
        
        # Calculate age
        age = (datetime.now() - birthday).days // 365
        data['Age'].append(age)
        
        # Generate address
        street_num = random.randint(1, 999)
        street = random.choice(streets)
        barangay = random.choice(barangays)
        data['Address'].append(f"{street_num} {street}, {barangay}")
    
    return data

def create_sample_excel():
    """Create a sample Excel file with resident data."""
    # Generate sample data
    data = generate_sample_data(20)  # Generate 20 sample records
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Save to Excel
    excel_file = 'residents.xlsx'
    df.to_excel(excel_file, index=False)
    print(f"Sample Excel file created: {excel_file}")
    print("\nSample data preview:")
    print(df.head())

if __name__ == "__main__":
    create_sample_excel() 