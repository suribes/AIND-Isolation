import logging

def config_log():
    logging.basicConfig(filename='isolation.log', filemode='w', level=logging.DEBUG)
