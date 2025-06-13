import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

class StatisticsManager:
    """Manages statistics for the dashboard."""
    
    def __init__(self):
        """Initialize the statistics manager."""
        self.data_file = Path("DATA/statistics.json")
        self._ensure_data_file()
        self._load_data()
    
    def _ensure_data_file(self) -> None:
        """Ensure the statistics data file exists."""
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        if not self.data_file.exists():
            self._initialize_data()
    
    def _initialize_data(self) -> None:
        """Initialize the statistics data structure."""
        initial_data = {
            "total_residents": 0,
            "new_residencies": {
                "current_month": 0,
                "last_updated": datetime.now().strftime("%Y-%m")
            },
            "certificates": {
                "today": 0,
                "last_updated": datetime.now().strftime("%Y-%m-%d")
            },
            "completed_tasks": {
                "today": 0,
                "last_updated": datetime.now().strftime("%Y-%m-%d")
            }
        }
        self._save_data(initial_data)
    
    def _load_data(self) -> None:
        """Load statistics data from file."""
        with open(self.data_file, 'r') as f:
            self.data = json.load(f)
    
    def _save_data(self, data: Dict[str, Any]) -> None:
        """Save statistics data to file."""
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=4)
        self.data = data
    
    def _check_date_reset(self) -> None:
        """Check and reset daily statistics if needed."""
        current_date = datetime.now().strftime("%Y-%m-%d")
        current_month = datetime.now().strftime("%Y-%m")
        
        # Reset daily certificates if it's a new day
        if self.data["certificates"]["last_updated"] != current_date:
            self.data["certificates"]["today"] = 0
            self.data["certificates"]["last_updated"] = current_date
        
        # Reset daily tasks if it's a new day
        if self.data["completed_tasks"]["last_updated"] != current_date:
            self.data["completed_tasks"]["today"] = 0
            self.data["completed_tasks"]["last_updated"] = current_date
        
        # Reset monthly residencies if it's a new month
        if self.data["new_residencies"]["last_updated"] != current_month:
            self.data["new_residencies"]["current_month"] = 0
            self.data["new_residencies"]["last_updated"] = current_month
        
        self._save_data(self.data)
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get current statistics.
        
        Returns:
            Dictionary containing current statistics
        """
        self._check_date_reset()
        return {
            "total_residents": self.data["total_residents"],
            "new_residencies": self.data["new_residencies"]["current_month"],
            "certificates_today": self.data["certificates"]["today"],
            "completed_today": self.data["completed_tasks"]["today"]
        }
    
    def increment_total_residents(self) -> None:
        """Increment total residents count."""
        self.data["total_residents"] += 1
        self._save_data(self.data)
    
    def increment_new_residencies(self) -> None:
        """Increment new residencies count for current month."""
        self._check_date_reset()
        self.data["new_residencies"]["current_month"] += 1
        self._save_data(self.data)
    
    def increment_certificates(self) -> None:
        """Increment certificates issued today."""
        self._check_date_reset()
        self.data["certificates"]["today"] += 1
        self._save_data(self.data)
    
    def increment_completed_tasks(self) -> None:
        """Increment completed tasks today."""
        self._check_date_reset()
        self.data["completed_tasks"]["today"] += 1
        self._save_data(self.data) 