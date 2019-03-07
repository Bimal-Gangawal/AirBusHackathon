import configparser

_config = configparser.ConfigParser()
_config.read('../Configuration/properties_config.ini')


class GlobalConstants:
    def __init__(self):
        self.env = _config['DEFAULT']['ENVIRNOMENT']
        self.MYSQL_END_POINT = _config[self.env]['MYSQL_END_POINT']
        self.MYSQL_USER_NAME = _config[self.env]['MYSQL_USER_NAME']
        self.MYSQL_PASSWORD = _config[self.env]['MYSQL_PASSWORD']
        self.MYSQL_PORT = int(_config[self.env]['MYSQL_PORT'])
        self.MYSQL_SCHEMA = _config[self.env]['MYSQL_SCHEMA']
