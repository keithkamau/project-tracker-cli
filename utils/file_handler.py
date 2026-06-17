import json
import os
from pathlib import Path

def get_data_path():
    """Get configurable data directory path from environment or default."""
    data_dir = os.environ.get('PROJECTS_DATA_DIR', str(Path.home() / '.project_manager'))
    return os.path.join(data_dir, 'projects.json')

DATA_FILE = get_data_path()

def load_data():
    """Load data with comprehensive error handling."""
    try:
        if not os.path.exists(DATA_FILE):
            print(f"Info: Creating new data file at {DATA_FILE}")
            return {"users": [], "projects": [], "tasks": []}
        
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
            
        if not isinstance(data, dict):
            raise ValueError("Data file is corrupted")
            
        required_keys = {"users", "projects", "tasks"}
        for key in required_keys:
            if key not in data:
                data[key] = []
                
        return data
        
    except json.JSONDecodeError as e:
        print(f"Warning: JSON decode error: {e}")
        backup_file = DATA_FILE + '.backup'
        if os.path.exists(DATA_FILE):
            os.rename(DATA_FILE, backup_file)
            print(f"Corrupted file backed up to {backup_file}")
        return {"users": [], "projects": [], "tasks": []}
        
    except PermissionError:
        print(f"Error: Permission denied accessing {DATA_FILE}")
        raise
        
    except Exception as e:
        print(f"Error: Unexpected error loading data: {e}")
        raise

def save_data(data):
    """Save data with atomic write and validation."""
    if not isinstance(data, dict):
        raise ValueError("Invalid data format")
        
    try:
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        
        temp_file = DATA_FILE + '.tmp'
        with open(temp_file, 'w') as f:
            json.dump(data, f, indent=2, default=str)
            
        if os.path.exists(DATA_FILE):
            os.replace(temp_file, DATA_FILE)
        else:
            os.rename(temp_file, DATA_FILE)
            
    except PermissionError:
        print(f"Error: Permission denied writing to {DATA_FILE}")
        raise
        
    except Exception as e:
        print(f"Error saving data: {e}")
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except:
                pass
        raise