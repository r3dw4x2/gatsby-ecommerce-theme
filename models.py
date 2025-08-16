from datetime import datetime
from typing import List, Dict, Optional
from config import get_supabase_client

class DataEntry:
    """Model for handling data entries in Supabase"""
    
    def __init__(self):
        self.supabase = get_supabase_client()
        self.table_name = "data_entries"
    
    def create_table_if_not_exists(self):
        """
        SQL to create the table in Supabase:
        
        CREATE TABLE IF NOT EXISTS data_entries (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255),
            phone VARCHAR(50),
            category VARCHAR(100),
            description TEXT,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        );
        """
        pass  # This would be executed in Supabase SQL editor
    
    def create(self, data: Dict) -> Dict:
        """Create a new data entry"""
        try:
            entry_data = {
                "name": data.get("name"),
                "email": data.get("email"),
                "phone": data.get("phone"),
                "category": data.get("category"),
                "description": data.get("description"),
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            
            result = self.supabase.table(self.table_name).insert(entry_data).execute()
            return {"success": True, "data": result.data[0] if result.data else None}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_all(self) -> List[Dict]:
        """Get all data entries"""
        try:
            result = self.supabase.table(self.table_name).select("*").order("created_at", desc=True).execute()
            return {"success": True, "data": result.data}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_by_id(self, entry_id: int) -> Dict:
        """Get a single data entry by ID"""
        try:
            result = self.supabase.table(self.table_name).select("*").eq("id", entry_id).execute()
            return {"success": True, "data": result.data[0] if result.data else None}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def update(self, entry_id: int, data: Dict) -> Dict:
        """Update a data entry"""
        try:
            update_data = {
                "name": data.get("name"),
                "email": data.get("email"),
                "phone": data.get("phone"),
                "category": data.get("category"),
                "description": data.get("description"),
                "updated_at": datetime.now().isoformat()
            }
            
            result = self.supabase.table(self.table_name).update(update_data).eq("id", entry_id).execute()
            return {"success": True, "data": result.data[0] if result.data else None}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def delete(self, entry_id: int) -> Dict:
        """Delete a data entry"""
        try:
            result = self.supabase.table(self.table_name).delete().eq("id", entry_id).execute()
            return {"success": True, "data": result.data}
        except Exception as e:
            return {"success": False, "error": str(e)}