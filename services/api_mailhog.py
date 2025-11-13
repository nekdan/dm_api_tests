from restclient.configuration import Configuration
from api_mailhog.apis.mailhog_api import MailhogAPI


class ApiMailhog:
    def __init__(self, configuration: Configuration):
        self.configuration = configuration
        self.mailhog_api = MailhogAPI(self.configuration)
