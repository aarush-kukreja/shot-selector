import yaml
from pathlib import Path

def load_config(config_path):
    """Load configuration from YAML file"""
    # Convert to Path object
    config_path = Path(config_path)
    
    # If path is relative and file doesn't exist, try looking from project root
    if not config_path.is_absolute() and not config_path.exists():
        project_root = Path(__file__).parent.parent.parent
        config_path = project_root / config_path
    
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
        
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def ensure_directory(directory):
    """Ensure a directory exists"""
    Path(directory).mkdir(parents=True, exist_ok=True)

def get_project_root():
    """Get the project root directory"""
    return Path(__file__).parent.parent.parent
