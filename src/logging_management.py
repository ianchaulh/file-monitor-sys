import logging

# TODO: 2
def get_config_logger():
    config_logger = logging.getLogger(__name__ + '.config')
    config_logger.setLevel(logging.DEBUG)

    config_file_handler = logging.FileHandler('../log/config.log')  # The path to the config log file is constrained. Please follow.
    config_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    config_file_handler.setFormatter(config_formatter)
    config_logger.addHandler(config_file_handler)

    return config_logger

def get_file_operation_logger():
    # TODO: Implmentation details
    file_operation_logger = logging.getLogger(__name__ + '.fo')
    return file_operation_logger

def get_error_logger():
    # TODO: Implmentation details
    error_logger = logging.getLogger(__name__ + '.error')
    return error_logger