import pytest
from unittest.mock import Mock, patch
from src.app.cli import CLI

@pytest.fixture
def cli():
    with patch('src.app.cli.load_config') as mock_config:
        mock_config.return_value = {'model': {'name': 'test-model'}}
        return CLI()

def test_cli_initialization(cli):
    assert cli is not None
    assert cli.parser is not None

def test_setup_commands(cli):
    # Check if all required arguments are set up
    actions = {action.dest for action in cli.parser._actions}
    assert 'prompt' in actions
    assert 'train' in actions
    assert 'evaluate' in actions

@patch('builtins.print')
def test_display_result(mock_print, cli):
    result = {
        'strategy': 'one-shot',
        'confidence': 0.85,
        'explanation': 'Test explanation'
    }
    
    cli._display_result(result)
    mock_print.assert_called()

@patch('builtins.input', side_effect=['test prompt', 'quit'])
@patch.object(CLI, '_handle_prediction')
def test_interactive_mode(mock_handle_prediction, mock_input, cli):
    cli._interactive_mode()
    mock_handle_prediction.assert_called_once_with('test prompt')

@patch.object(CLI, '_handle_prediction')
def test_run_with_prompt(mock_handle_prediction, cli):
    with patch('argparse.ArgumentParser.parse_args') as mock_args:
        mock_args.return_value = Mock(
            prompt='test prompt',
            train=False,
            evaluate=False
        )
        cli.run()
        mock_handle_prediction.assert_called_once_with('test prompt')

def test_handle_prediction_error(cli):
    with patch.object(cli.model, 'predict', side_effect=Exception('Test error')):
        with patch('builtins.print') as mock_print:
            cli._handle_prediction('test prompt')
            mock_print.assert_called_with('Error making prediction: Test error')
