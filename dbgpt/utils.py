import configparser
import logging
import os

from pkg_resources import resource_filename

from dbgpt.drivers import PostgresDriver, MySQLDriver


def _read_config():
    config_parser = configparser.ConfigParser()
    f = resource_filename("dbgpt", "../resources/config.ini")
    config_parser.read(f)
    return config_parser


def get_dbms_driver(system, db=None, user=None, password=None):
    config_parser = _read_config()

    if not user:
        user = config_parser[system]["user"]

    if not password:
        password = config_parser[system]["password"] if "password" in config_parser[system] else None

    if not db:
        db = config_parser["DBGPT"]["database"]

    logging.info(f"Getting DBMS driver for {system} with user {user} and db {db}")

    if system.lower() == "postgres":
        return PostgresDriver({"user": user, "password": password, "db": db})
    elif system.lower() == "mysql":
        return MySQLDriver({"user": user, "password": password, "db": db})
    else:
        raise Exception(f"Unsupported DBMS: {system}")


def get_openai_key():
    key = os.getenv("OPENAI_API_KEY")
    if key:
        return key
    config_parser = _read_config()
    return config_parser["DBGPT"].get("openai_key")


def get_llm():
    config_parser = _read_config()
    return config_parser["DBGPT"]["llm"]
