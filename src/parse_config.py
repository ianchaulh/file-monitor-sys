import json
import os
from logging_management import get_config_logger, get_file_operation_logger, get_error_logger


"""
Required format of the nested dictionary:
    config = \
    {
        # Directories to monitor for changes
        "directories": {
            "source_dirs": ["C:\\Users\\Ian Chau\\Desktop\\test__", "C:\\Users\\Ian Chau\\Desktop\\test_"]  # Monitor source directories
        },
        # File-related settings
        "files": {
            "target_files": [],
            # Trigger a system notification if the filename of a file in target_files is created, modified, or deleted
            "keywords": ['hello', 'test'],
            # Trigger a system notification if the filename of a file contains any of the specified keywords is created, modified or deleted
            "formats": ['.xlsx', '.py']
            # Trigger a system notification if a file with the specified formats is created, modified, or deleted
        },
        # Notification and logging settings
        "parameters": {
            "notification_settings": {
                "enabled": True,  # Enable/disable notifications
                "notification_types": ["system", "email"],  # Types of notifications to send
                "recipients": ["ianchau379@gmail.com"]  # Email recipients for notifications
            },
            "log_settings": {
                "log_file_path": "/log/records.log",  # Path to the main log file
                "log_level": "INFO",  # Minimum log level to record in the main log
                "error_log_file_path": "/log/errors.log",  # Path to the error log file
                "error_log_level": "ERROR"  # Minimum log level to record in the error log
            }
        }
    }
"""

# TODO: 5
def load_config():
    """
    Loads the configuration from a JSON file.

    Returns:
        dict: The configuration data.
    """

    config_file_path = '../config/config.json' # The path to the configuration file is constrained. Please follow.

    try:
        # Check if the file exists
        if not os.path.exists(config_file_path):
            raise FileNotFoundError(f"Configuration file not found at: {config_file_path}")

        # Try to read the file contents
        with open(config_file_path, 'r') as f:
            config_json = f.read()

        # Try to parse the JSON data
        config = json.loads(config_json)

        # TODO: Validate the format of the nested dictionary matches requirements

        # TODO: Validate the source_dirs exists

        return config

    except json.JSONDecodeError as e:
        # TODO: Use the error_logger to log this exception with the ERROR level
        print(f"Error parsing the JSON file: {e}")
        print(f"Check the file at: {config_file_path}")
        raise

    except FileNotFoundError as e:
        # TODO: Use the error_logger to log this exception with the ERROR level
        print(f"Error loading the configuration file: {e}")
        raise

    except Exception as e:
        # TODO: Use the error_logger to log this exception with the ERROR level
        print(f"Unexpected error occurred: {e}")
        raise
