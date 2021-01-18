"""
Config file for Yasna
"""


from os import environ, path
from dotenv import load_dotenv
from logger import get_logger

logger = get_logger("yasna.main")


class _Config:
    def __init__(self):
        if environ.get("CI") is None:
            project_folder = path.expanduser(".")
            load_dotenv(path.join(project_folder, ".env"))

        self.config = {
            "webhook_url": self.get_env_value("SLACK_WEBHOOK"),
            "token": self.get_env_value("GITHUB_TOKEN"),
            "actor": self.get_env_value("GITHUB_ACTOR"),
            "sha": self.get_env_value("GITHUB_SHA"),
            "repo": self.get_env_value("GITHUB_REPOSITORY"),
            "event": self.get_env_value("GITHUB_EVENT_NAME"),
            "action": self.get_env_value("GITHUB_WORKFLOW"),
            "server": self.get_env_value("GITHUB_SERVER_URL"),
            "action_id": self.get_env_value("GITHUB_RUN_ID"),
            "ref": self.get_env_value("GITHUB_REF"),
            "build_status": self.get_env_value("STATUS"),
        }
        self.config["base_url"] = f"{self.server}/{self.repo}"

    @classmethod
    def get_env_value(cls, env_var):
        """
        Returns an environment variable,
        raises an exception if varible is not present
        """
        try:
            logger.debug("Loading %s from environment", env_var)
            return environ[env_var]
        except KeyError as key_error_exception:
            logger.error("%s is not present", env_var)
            error_msg = f"{env_var} environment variable is not present"
            raise KeyError(error_msg) from key_error_exception

    def __getattr__(self, name):
        try:
            return self.config[name]
        except KeyError as key_error_exception:
            logger.error("%s is not present in config", name)
            error_msg = f"{name} is not present in config"
            raise KeyError(error_msg) from key_error_exception


config = _Config()
