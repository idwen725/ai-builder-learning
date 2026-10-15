from app import App
from config import Config
from logger import setup_logging

Config.validate()
setup_logging()

app = App()
app.run()