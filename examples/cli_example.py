import logging

from src.gajou_cli import BaseCLI


# Representation of some CLI, it should use BaseCLI as a session analogue, and it unites all subcommand group
class KubeCLI:
    def __init__(self, custom_path):
        self.cli = BaseCLI('kubectl', custom_path)

        self.get = GetCommand(self.cli)  # connected subcommand group

    def version(self):
        return self('version')

    def __call__(self, command, *args):
        return BaseCommand(command, self.cli)(*args)


# BaseCommand implements ability to self call command without args
class BaseCommand:
    def __init__(self, name, cli):
        self.cli = cli
        self.name = name

    # to call command with BaseCLI need to use method "do"
    def __call__(self, *args):
        rs = self.cli.do(self.name, *args)
        return rs


# Simple group of command
class GetCommand(BaseCommand):
    def __init__(self, cli):
        super().__init__('get', cli)

    def pods(self, *args):
        return self('pods', *args)

    def services(self, *args):
        return self('services', *args)


if __name__ == '__main__':
    # logger configuration to demonstrate "out-of-the-box" logs
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(fmt='[%(levelname)s] %(asctime)s  %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    kubectl_dir = '/usr/local/bin/'  # without binary name
    kubectl = KubeCLI(kubectl_dir)
    kubectl('version')
    kubectl.version()
    pods = kubectl.get.pods('-n my_namespace')
    services = kubectl.get.services('-n', 'my_namespace')
