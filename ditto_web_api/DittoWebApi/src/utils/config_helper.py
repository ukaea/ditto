from configparser import ConfigParser


def config_to_string(configparser):
    if not isinstance(configparser, ConfigParser):
        raise ValueError('Method only accepts a ConfigParser object')
    output = ''
    for section in configparser.sections():
        output += f'[{section}]\n'
        for key, value in configparser[section].items():
            output += f'{key} = {value}\n'
        output += '\n'
    return output
