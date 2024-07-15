import time
from watchdog.observers import Observer
from logging_management import get_config_logger, get_file_operation_logger, get_error_logger


# TODO: 2
def monitor_directory(directory, event_handler, stop_event):
    observer = Observer()
    observer.schedule(event_handler, directory, recursive=True)
    observer.start()
    # TODO: Use the config_logger to log this event with the DEBUG level
    print(f'Monitoring directory: {directory}')
    while not stop_event.is_set():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break

    observer.stop()
    observer.join()
    # TODO: Use the config_logger to log this event with the DEBUG level
    print(f'Stopped monitoring directory: {directory}')