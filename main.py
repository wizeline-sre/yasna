"""
yasna (Yet Another Slack Notifier Action)

"""
from enum import Enum

from slack_sdk.webhook import WebhookClient
from github import Github

from config_loader import config
from logger import get_logger

logger = get_logger("yasna.main")


class Status(Enum):
    """
    Declares any possible status that can
    be used within this action
    """

    success = "#36B37E"
    fail = "#FF5630"
    failure = "#FF5630"
    cancelled = "#CDCDCD"


class Yasna:
    """
    Yasna class contains all the methods to create the message and to
    send it to Slack
    """

    def __init__(self):
        pass

    @classmethod
    def get_author(cls):
        """
        Returns a dictionary with the author informatin which is placed
        at the top of the attachement.
        """
        logger.info("setting up author information")
        return {
            "author_name": config.actor,
            "author_link": f"{config.server}/{config.actor}",
            "author_icon": f"{config.server}/{config.actor}.png?size=32",
        }

    @classmethod
    def get_footer(cls):
        """
        Returns a dictionary with the footer information
        """
        logger.info("setting up footer information")
        return {
            "footer": "<https://wizeline.com|Powered by Wizeline SRE Team>",
            "footer_icon": "https://www.wizeline.com/favicon.ico",
        }

    def _get_origin(self):
        """
        Based on the event type, returns a dictionary with the right information.
        """
        logger.info("setting up origin for branch %s", config.ref)
        origin = {
            "title": "Branch",
            "ref": config.ref,
            "url": f"{config.base_url}/{config.sha}",
        }
        logger.debug("event type is %s", config.event)
        if config.event == "pull_request":
            logger.debug("calling GitHub API to get Pull Request information")
            pulls = (
                Github(config.token)
                .get_repo(config.repo)
                .get_commit(config.sha)
                .get_pulls()
            )
            logger.debug("commit is associated with %d PRs", pulls.totalCount)
            if pulls.totalCount > 0:
                origin = {
                    "title": "Pull Request",
                    "ref": pulls[0].title,
                    "url": f"{config.base_url}/pull/{pulls[0].number}",
                }
        return origin

    def get_fields(self):
        """
        Return the fields that composes the slack message.
        They will appear stacked in two columns.
        |Action | Status |
        |Origin | Event  |
        """
        logger.info("setting up fields for action %s", config.action)
        action_url = f"{config.base_url}/actions/runs/{config.action_id}"
        origin = self._get_origin()
        return [
            {
                "title": "Action",
                "value": f"<{action_url}|{config.action}>",
                "short": True,
            },
            {
                "title": "Status",
                "value": Status[config.build_status].name.title(),
                "short": True,
            },
            {
                "title": origin["title"],
                "value": f"<{origin['url']}| {origin['ref']}>",
                "short": True,
            },
            {"title": "Event", "value": config.event, "short": True},
        ]

    def send(self):
        """
        sends a message to the slack webhook
        """

        attachment = {
            "color": Status[config.build_status].value,
            **self.get_author(),
            "fields": self.get_fields(),
            **self.get_footer(),
        }

        logger.info("sending message to Slack")
        WebhookClient(config.webhook_url).send(attachments=[attachment])
        logger.debug("message to Slack was sent")


if __name__ == "__main__":
    Yasna().send()
