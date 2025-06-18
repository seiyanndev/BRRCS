import pandas as pd
import os
from datetime import datetime, timedelta
import random

def generate_sample_data(num_records=20):
    """Generate sample resident data"""
    
    # Sample data for generating realistic records
    first_names = ['Juan', 'Maria', 'Pedro', 'Ana', 'Jose', 'Carmen', 'Antonio', 'Isabel', 
                  'Francisco', 'Rosa', 'Miguel', 'Luz', 'Carlos', 'Elena', 'Manuel']
    last_names = ['Santos', 'Reyes', 'Cruz', 'Garcia', 'Torres', 'Flores', 'Rivera', 
                 'Mendoza', 'Aquino', 'Dela Cruz', 'Ramos', 'Gonzales', 'Villanueva']
    puroks = ['Purok 1', 'Purok 2', 'Purok 3', 'Purok 4', 'Purok 5']
    civil_statuses = ['Single', 'Married', 'Widowed', 'Divorced']
    genders = ['M', 'F']
    
    # Generate records
    records = []
    for i in range(num_records):
        # Generate random dates
        birth_date = (datetime.now() - timedelta(days=random.randint(365*18, 365*80))).strftime('%Y-%m-%d')
        date_registered = (datetime.now() - timedelta(days=random.randint(0, 365*5))).strftime('%Y-%m-%d')
        
        # Generate random contact info
        contact = f"09{random.randint(100000000, 999999999)}"
        email = f"resident{i}@example.com"
        
        record = {
            'resident_id': f"BRG6-{str(i+1).zfill(4)}",
            'last_name': random.choice(last_names),
            'first_name': random.choice(first_names),
            'middle_name': random.choice(first_names) if random.random() > 0.3 else '',
            'birth_date': birth_date,
            'gender': random.choice(genders),
            'civil_status': random.choice(civil_statuses),
            'address': f"{random.randint(1, 999)} {random.choice(['St.', 'Ave.', 'Blvd.'])} {random.choice(['Main', 'Rizal', 'Bonifacio', 'Aguinaldo'])}",
            'purok': random.choice(puroks),
            'contact_number': contact if random.random() > 0.2 else '',
            'email': email if random.random() > 0.5 else '',
            'voter_id': f"V{random.randint(100000, 999999)}" if random.random() > 0.3 else '',
            'date_registered': date_registered,
            'status': 'Active' if random.random() > 0.1 else 'Inactive'
        }
        records.append(record)
    
    return pd.DataFrame(records)

def create_sample_excel():
    """Create sample Excel file with resident data"""
    try:
        # Create data directory if it doesn't exist
        data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        os.makedirs(data_dir, exist_ok=True)
        
        # Generate sample data
        df = generate_sample_data()
        
        # Save to Excel
        output_path = os.path.join(data_dir, 'sample_residents.xlsx')
        df.to_excel(output_path, index=False, engine='openpyxl')
        print(f"Sample data created successfully at: {output_path}")
        print(f"Generated {len(df)} sample records")
        
    except Exception as e:
        print(f"Error creating sample data: {e}")

if __name__ == "__main__":
    create_sample_excel() 