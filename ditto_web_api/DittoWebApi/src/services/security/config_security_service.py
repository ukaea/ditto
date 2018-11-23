import configparser

from DittoWebApi.src.services.security.isecurity_service import ISecurityService
from DittoWebApi.src.utils.parse_strings import str2list


class User:
    def __init__(self, properties):
        self._groups = str2list(properties['groups'])
        self._password = properties['password']

    def is_password(self, password):
        return password == self._password

    def is_in_group(self, group):
        return group in self._groups


class ConfigSecurityService(ISecurityService):
    def __init__(self, configuration_path, logger):
        self._users = None
        self._logger = logger
        self._parse(configuration_path)

    def _parse(self, configuration_path):
        config = configparser.ConfigParser()
        config.read(configuration_path)
        self._users = {ConfigSecurityService._format_name(name): User(config[name]) for name in config.sections()}
        self._logger.info(
            f'Security Service found {len(self._users)} users in configuration file "{configuration_path}"'
        )

    def is_authenticated(self, name, password):
        self._logger.info(f'Trying to authenticate user "{name}"')
        user = self._get_user(name)
        if user is None:
            return False
        password_correct = user.is_password(password)
        self._logger.info(f'User "{name}" {"authenticated successfully" if password_correct else "password invalid"}')
        return password_correct

    def is_in_group(self, name, group):
        self._logger.info(f'Trying to check group "{group}" for user "{name}"')
        user = self._get_user(name)
        if user is None:
            return False
        is_in_group = user.is_in_group(group)
        self._logger.info(f'User "{name}" {"is" if is_in_group else "is not"} in group "{group}"')
        return is_in_group

    def _get_user(self, name):
        formatted_name = ConfigSecurityService._format_name(name)
        if formatted_name not in self._users:
            self._logger.info(f'User "{name}" does not exist')
            return None
        return self._users[formatted_name]

    @staticmethod
    def _format_name(name):
        return name.lower().strip()
