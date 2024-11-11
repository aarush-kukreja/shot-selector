from src.app.server import app
from src.utils.helpers import load_config

if __name__ == "__main__":
    config = load_config('src/config/config.yaml')
    app.run(
        host=config['server']['host'],
        port=config['server']['port'],
        debug=config['server']['debug']
    ) 