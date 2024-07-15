import os
import time
import datetime
from watchdog.events import FileSystemEventHandler
from win10toast import ToastNotifier
from threading import Thread, Lock, Event
from logging_management import get_config_logger, get_file_operation_logger, get_error_logger

# TODO: 5
class FileEventHandler(FileSystemEventHandler): # FileEventHandler is the subclass of FileSystemEventHandler
    """
    This class handles file system events (created, modified, deleted) and performs related actions.

    Methods:
        on_created(self, event): Handles file creation events and performs associated actions.
        on_modified(self, event): Handles file modification events and performs associated actions.
        on_deleted(self, event): Handles file deletion events and performs associated actions.
        meet_formats(self, file_path): Checks if a file has a specified format.
        meet_keywords(self, file_path): Checks if a file's filename contains any of the specified keywords.
        meet_target_files(self, file_path): Checks if a file's filename matches any of the target filenames.
        notify_recipients(self, event_type, msg): Sends notifications to the specified recipients.
        log_event(self, msg): Logs the event message.
    """

    def __init__(self, directories, files, notification_settings, log_settings):
        self.directories = directories
        self.files = files
        self.notification_settings = notification_settings
        self.log_settings = log_settings
        self.lock = Lock()  # Introduce a lock for thread-safe file operations

    def on_created(self, event):
        if event.is_directory:
            return
        file_path = event.src_path
        if (self.meet_formats(file_path) or self.meet_keywords(file_path) or self.meet_target_files(file_path)) \
            and not os.path.basename(event.src_path).startswith('~$'):  # Ignore temporary files
            with self.lock:  # Acquire the lock before performing file operations
                created_at = time.time()
                created_at = datetime.datetime.fromtimestamp(created_at)
                msg = f'CREATED file: {file_path} on {created_at}.'
                self.notify_recipients('CREATED', msg)
                # TODO: log the message to records
                print(msg)

    def on_modified(self, event):
        if event.is_directory:
            return
        file_path = event.src_path
        if (self.meet_formats(file_path) or self.meet_keywords(file_path) or self.meet_target_files(file_path)) \
            and not os.path.basename(event.src_path).startswith('~$'):  # Ignore temporary files
            with self.lock:  # Acquire the lock before performing file operations
                modified_at = time.time()
                modified_at = datetime.datetime.fromtimestamp(modified_at)
                msg = f'MODIFIED file: {file_path} on {modified_at}.'
                self.notify_recipients('MODIFIED', msg)
                # TODO: log the message to records
                print(msg)

    def on_deleted(self, event):
        # ISSUE: When a sub-directory that contains desired files moves away from a monitoring directory, the triggered event cannot detected by on_deleted()
        # However, when a desired file moves away from a monitoring directory, the triggered event can be detected by on_deleted()
        # Moreover, a sub-directory that contains desired files moves to a monitoring directory, the triggered event can be detected by on_created()
        # TODO: May need on_moved() plus some conditions to handle above observations
        if event.is_directory:
            return
        file_path = event.src_path
        if (self.meet_formats(file_path) or self.meet_keywords(file_path) or self.meet_target_files(file_path)) \
            and not os.path.basename(event.src_path).startswith('~$'):  # Ignore temporary files
            with self.lock:  # Acquire the lock before performing file operations
                deleted_at = time.time()
                deleted_at = datetime.datetime.fromtimestamp(deleted_at)
                msg = f'DELETED file: {file_path} on {deleted_at}.'
                self.notify_recipients('DELETED', msg)
                # TODO: log the message to records
                print(msg)

    def meet_formats(self, file_path):
        # return True if a file with the specified formats
        return any(file_path.endswith(format) for format in self.files["formats"])

    def meet_keywords(self, file_path):
        # return True if the filename of a file contains any of the specified keywords
        return any(keyword in os.path.basename(file_path) for keyword in self.files["keywords"])

    def meet_target_files(self, file_path):
        # return True if the filename of a file in target_files
        return any(os.path.basename(file_path) == filename for filename in self.files["target_files"])

    def notify_recipients(self, event_type, msg):
        if self.notification_settings["enabled"]:
            if "system" in self.notification_settings["notification_types"]:
                toaster = ToastNotifier()
                toaster.show_toast(event_type, msg, duration=1)
            if "email" in self.notification_settings["notification_types"]:
                # TODO: email notification
                pass
        return

    def log_event(self, msg):
        # TODO: Log activity operations
        return
