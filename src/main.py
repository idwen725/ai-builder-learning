from app import App
from config import Config
from logger import setup_logging

setup_logging()
Config.validate()

app = App()
app.run()