import pytest
import pandas as pd
from pathlib import Path
from src.data.data_loader import DataLoader
from src.utils.helpers import load_config

@pytest.fixture
def config():
    return load_config('src/config/config.yaml')

@pytest.fixture
def data_loader(config):
    return DataLoader(config)

@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'prompt_text': ['Sample prompt 1', 'Sample prompt 2'],
        'optimal_strategy': ['one-shot', 'chain-of-thought']
    })

def test_data_loader_initialization(data_loader):
    assert data_loader is not None
    assert isinstance(data_loader.data_dir, Path)

def test_load_csv_data(data_loader, tmp_path):
    # Create temporary CSV file
    test_file = tmp_path / "test_data.csv"
    pd.DataFrame({
        'prompt_text': ['Test prompt'],
        'optimal_strategy': ['one-shot']
    }).to_csv(test_file, index=False)
    
    data = data_loader.load_raw_data(test_file)
    assert isinstance(data, pd.DataFrame)
    assert 'prompt_text' in data.columns
    assert 'optimal_strategy' in data.columns

def test_load_json_data(data_loader, tmp_path):
    # Create temporary JSON file
    test_file = tmp_path / "test_data.json"
    pd.DataFrame({
        'prompt_text': ['Test prompt'],
        'optimal_strategy': ['one-shot']
    }).to_json(test_file)
    
    data = data_loader.load_raw_data(test_file)
    assert isinstance(data, pd.DataFrame)

def test_save_processed_data(data_loader, sample_data, tmp_path):
    # Set temporary data directory
    data_loader.data_dir = tmp_path
    
    data_loader.save_processed_data(sample_data, 'test_processed.csv')
    saved_file = tmp_path / 'processed' / 'test_processed.csv'
    
    assert saved_file.exists()
    loaded_data = pd.read_csv(saved_file)
    assert loaded_data.shape == sample_data.shape

def test_load_training_data_missing_file(data_loader):
    with pytest.raises(FileNotFoundError):
        data_loader.load_training_data()
