"""Creates a unique FileStorage instance of the application"""
from models.engine.file_storage import FileStorage


storage = FileStorage()
storage.reload()
