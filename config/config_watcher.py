

"""
Configuration file watcher for automatic reloading
"""
import logging
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from typing import Callable, Optional
import time

logger = logging.getLogger(__name__)

class ConfigWatcher(FileSystemEventHandler):
    """
    Watcher for configuration file changes with debounce support
    """

    def __init__(self, config_file: str, reload_callback: Callable[[], None], debounce_seconds: float = 1.0):
        """
        Initialize configuration watcher

        Args:
            config_file: Path to configuration file to watch
            reload_callback: Function to call when config changes
            debounce_seconds: Debounce time to avoid rapid successive reloads
        """
        self.config_file = config_file
        self.reload_callback = reload_callback
        self.debounce_seconds = debounce_seconds
        self.last_modified_time = 0
        self.lock = threading.Lock()

    def on_modified(self, event):
        """Handle file modification events"""
        if not event.src_path.endswith(self.config_file):
            return

        current_time = time.time()

        with self.lock:
            if current_time - self.last_modified_time > self.debounce_seconds:
                logger.info(f"Configuration file {self.config_file} changed, reloading...")
                try:
                    self.reload_callback()
                    self.last_modified_time = current_time
                except Exception as e:
                    logger.error(f"Error during configuration reload: {e}")

class ConfigFileWatcher:
    """
    Context manager for watching configuration files
    """

    def __init__(self, config_file: str, reload_callback: Callable[[], None], debounce_seconds: float = 1.0):
        """
        Initialize configuration file watcher

        Args:
            config_file: Path to configuration file to watch
            reload_callback: Function to call when config changes
            debounce_seconds: Debounce time to avoid rapid successive reloads
        """
        self.config_file = config_file
        self.reload_callback = reload_callback
        self.debounce_seconds = debounce_seconds
        self.observer = Observer()
        self.event_handler = ConfigWatcher(config_file, reload_callback, debounce_seconds)

    def start(self):
        """Start watching the configuration file"""
        self.observer.schedule(self.event_handler, path='.', recursive=False)
        self.observer.start()
        logger.info(f"Started watching configuration file: {self.config_file}")

    def stop(self):
        """Stop watching the configuration file"""
        self.observer.stop()
        self.observer.join()
        logger.info(f"Stopped watching configuration file: {self.config_file}")

    def __enter__(self):
        """Context manager entry"""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.stop()

