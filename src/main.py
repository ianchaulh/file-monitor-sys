import os
import time
import datetime
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from threading import Thread, Event

# Import function/ class from separate script
from parse_config import load_config
from file_event_handler import FileEventHandler  # This class handles file system events (created, modified, deleted) and performs related actions.
from directory_monitoring import monitor_directory
from logging_management import get_config_logger, get_file_operation_logger, get_error_logger

# TODO: 9
class ConfigFileEventHandler(FileSystemEventHandler):
    def __init__(self, event_handler, directory_threads, stop_event, last_config_modification_time, config_logger):
        self.event_handler = event_handler
        self.directory_threads = directory_threads
        self.stop_event = stop_event
        self.last_config_modification_time = last_config_modification_time
        self.config_logger = config_logger

    def on_modified(self, event):
        if os.path.basename(event.src_path) == 'config.json':
            # TODO: Use the config_logger to log this event with the DEBUG level
            print("Configuration file has been modified. Reloading settings...")
            self.event_handler, self.directory_threads, self.stop_event, self.last_config_modification_time, self.config_logger = reload_config(
                self.event_handler, self.directory_threads, self.stop_event, self.last_config_modification_time, self.config_logger
            )
            # TODO: Use the config_logger to log this event with the DEBUG level
            print("Configuration reloaded.")

def reload_config(event_handler, directory_threads, stop_event, last_config_modification_time, config_logger):
    try:
        # TODO: Take extra care to handle errors that can occur in the middle of the process.
        # TODO: Add a mechanism to backup the previous configuration and restore it if the new configuration cannot be loaded successfully.
        config = load_config()
        config_logger.debug(str(config))
        directories = config["directories"]["source_dirs"]
        files = config["files"]
        notification_settings = config["parameters"]["notification_settings"]
        log_settings = config["parameters"]["log_settings"]

        # Stop old threads
        stop_event.set()
        for thread in directory_threads.values():
            thread.join()
        directory_threads.clear()
        stop_event = Event()

        # Update the event_handler
        event_handler = FileEventHandler(directories, files, notification_settings, log_settings)

        # Start new threads
        for directory in directories:
            thread = Thread(target=monitor_directory, args=(directory, event_handler, stop_event))
            directory_threads[directory] = thread
            thread.start()

        last_config_modification_time = datetime.datetime.fromtimestamp(time.time())
        # TODO: Use the config_logger to log this event with the INFO level
        print(f'Monitoring updated directories on {last_config_modification_time}')

        return event_handler, directory_threads, stop_event, last_config_modification_time, config_logger

    except Exception as e:
        # TODO: Use the error_logger to log this exception with the ERROR level
        print(f"Error reloading the configuration: {e}")
        print("The configuration change could not be applied, and the application will continue to use the previous configuration.")
        # TODO: Use the config_logger to log these messages with the WARNING level
        print(f"The last config modification time is {last_config_modification_time}")
        return event_handler, directory_threads, stop_event, last_config_modification_time, config_logger

if __name__ == '__main__':
    # Set up the loggers
    config_logger = get_config_logger()
    file_operation_logger = get_file_operation_logger()
    error_logger = get_error_logger()

    directory_threads = {}  # Dictionary to store the directory-to-thread mapping
    stop_event = Event()
    last_config_modification_time = datetime.datetime.fromtimestamp(time.time())  # Keep track of the last modification time of the configuration file

    try:
        # If the configuration file has an incorrect format or the specified directory does not exist,
        # the function load_config() will not handle these cases gracefully and may result in errors.
        # TODO: Please see parse_config.py
        config = load_config()
        config_logger.debug(str(config))
    except Exception as e:
        # TODO: Use the error_logger to log this exception with the ERROR level
        print(f"Error loading configuration: {e}")

    directories = config["directories"]["source_dirs"]
    files = config["files"]
    notification_settings = config["parameters"]["notification_settings"]
    log_settings = config["parameters"]["log_settings"]

    event_handler = FileEventHandler(directories, files, notification_settings, log_settings)

    # Initialize a separate thread to monitor each directory
    for directory in directories:
        thread = Thread(target=monitor_directory, args=(directory, event_handler, stop_event))
        directory_threads[directory] = thread
        thread.start()

    # Set up a watchdog observer to monitor the configuration file
    config_file_event_handler = ConfigFileEventHandler(event_handler, directory_threads, stop_event,
                                                       last_config_modification_time, config_logger)
    observer = Observer()
    observer.schedule(config_file_event_handler, '../config', recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
        print('Exiting...')