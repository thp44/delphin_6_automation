__author__ = "Thomas Perkov"
__license__ = 'MIT'

# -------------------------------------------------------------------------------------------------------------------- #
# IMPORTS

# Modules:
from sshtunnel import SSHTunnelForwarder
import mongoengine
import typing
from delphin_6_automation.logging.ribuild_logger import ribuild_logger

# Logger
logger = ribuild_logger()

# RiBuild Modules:
# -------------------------------------------------------------------------------------------------------------------- #
# MONGO SETUP:


def global_init(auth_dict: dict) -> typing.Optional[SSHTunnelForwarder]:
    if auth_dict['ssh']:

        server = SSHTunnelForwarder(
            (auth_dict['ssh_ip'], auth_dict['ssh_port']),
            ssh_username=auth_dict['ssh_user'],
            ssh_password=auth_dict['ssh_password'],
            remote_bind_address=('localhost', 27017)
        )

        logger.debug(f'Starting Connection through SSH')
        server.start()

        mongoengine.register_connection(
            alias=auth_dict['alias'],
            name=auth_dict['name'],
            host=auth_dict['ip'],
            port=server.local_bind_port,
            username=auth_dict['username'],
            password=auth_dict['password']
        )

        logger.info(f'Connected to server')
        return server

    else:
        mongoengine.register_connection(
            alias=auth_dict['alias'],
            name=auth_dict['name'],
            host=auth_dict['ip'],
            port=auth_dict['port']
        )


def global_end_ssh(server: typing.Optional[SSHTunnelForwarder]) -> None:

    if server:
        server._transport.close()
        server.stop()

    logger.info('Connection ended.')
    return None
