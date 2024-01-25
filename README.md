# Shot Selector

An intelligent system that helps select and optimize prompting strategies for different AI models and use cases.

## Installation

1. Clone the repository:
   ```
   git clone aarush-kukreja/shot-selector.git
   cd shot-selector
   ```

2. Set up the environment:
   ```
   ./scripts/setup.sh
   ```

   This script will create a virtual environment, install dependencies, and set up the project structure.

## Usage

1. Activate the virtual environment:
   ```
   source venv/bin/activate
   ```

2. Run the CLI application:
   ```
   python src/main.py
   ```

   You can use the following commands:
   - `--prompt "Your prompt here"`: Get a strategy prediction for a single prompt
   - `--train`: Train the model with available data
   - `--evaluate`: Evaluate model performance

3. For API usage, run the server:
   ```
   python src/app/server.py
   ```

   The API will be available at `http://localhost:5000`.

## Features

- Intelligent selection of prompting strategies (zero-shot, one-shot, two-shot, three-shot)
- CLI interface for easy interaction
- RESTful API for integration with other applications
- Model training and evaluation capabilities
- Configurable settings for data processing and model parameters

## Configuration

The project configuration is stored in `src/config/config.yaml`. You can modify this file to adjust various settings, including:

- Data paths
- Model parameters
- Logging configuration
- Server settings

## Development

To set up the development environment:

1. Install development dependencies:
   ```
   pip install -e ".[dev]"
   ```

2. Use the provided scripts for common tasks:
   - `scripts/train_model.sh`: Train the model
   - `scripts/evaluate_model.sh`: Evaluate model performance
   - `scripts/run_app.sh`: Run the CLI application

## Testing

Run the test suite using pytest:

```
pytest
```

## API Reference

The API provides the following endpoints:

- `GET /health`: Health check
- `POST /predict`: Get strategy prediction for a single prompt
- `POST /batch-predict`: Get strategy predictions for multiple prompts

For detailed API documentation, refer to the `docs/api.rst` file.

## Contributing

Contributions are welcome! Please read the [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines on how to contribute to this project.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.