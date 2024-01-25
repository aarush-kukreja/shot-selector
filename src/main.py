from app.cli import CLI
from utils.logger import setup_logger

def main():
    logger = setup_logger()
    logger.info("Starting Shot-Selector")
    
    cli = CLI()
    cli.run()

if __name__ == "__main__":
    main()
