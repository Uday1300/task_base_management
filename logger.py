import logging

def configure_data_logger():
    data_logger = logging.getLogger('data_logger')
    data_logger.setLevel(logging.DEBUG)
    data_handler = logging.FileHandler("data.log")
    data_logger.addHandler(data_handler)
    return data_logger

def configure_error_logger():
    error_logger = logging.getLogger('error_logger')
    error_logger.setLevel(logging.ERROR)
    error_handler = logging.FileHandler("error.log")
    error_logger.addHandler(error_handler)
    return error_logger