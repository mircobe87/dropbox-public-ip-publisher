import uuid
import os

DEFAULT_TOKEN_FILE_NAME = "dpx.token"
DEFAULT_CHECK_INTERVAL = 30  # minutes
DEFAULT_CHECK_SERVICE = "dyndns"  # check pubic_ip_finder.service for available services
DEFAULT_CLIENT_NAME = uuid.getnode()


class DropBoxSettings:
    TOKEN_LOCATION = "tokens/"

    def __init__(self, api_key, api_secret, token_file_name):
        if api_key is None:
            raise Exception("Missing mandatory settings 'api_key'")
        if api_secret is None:
            raise Exception("Missing mandatory settings 'api_secret'")

        self.api_key = api_key
        self.api_secret = api_secret
        self.token_file_name = self.TOKEN_LOCATION + (token_file_name if not None else DEFAULT_TOKEN_FILE_NAME)

    def __str__(self):
        return (
            "DropBoxSettings[api_key: *****, api_secret: *****, token_file_name: {}]"
        ).format(self.token_file_name)


class CheckSettings:

    def __init__(self, interval, service_name):
        self.interval = int(interval) if not None else DEFAULT_CHECK_INTERVAL
        self.service = service_name if not None else DEFAULT_CHECK_SERVICE

    def __str__(self):
        return "CheckSettings[service: {}, interval: {}]".format(self.service, self.interval)


class ClientSettings:

    def __init__(self, name):
        self.name = name if not None else DEFAULT_CLIENT_NAME

    def __str__(self):
        return "ClientSettings[name: {}]".format(self.name)


class AppSettings:

    def __init__(self, api_key, api_secret, token_file_name, client_name, check_interval, check_service):
        self.dropbox = DropBoxSettings(api_key, api_secret, token_file_name)
        self.check = CheckSettings(check_interval, check_service)
        self.client = ClientSettings(client_name)

    def __str__(self):
        return (
            "AppSettings[dropbox: {}, check: {}, client: {}]"
        ).format(str(self.dropbox), str(self.check), str(self.client))


def retrieve_tmp_data(tmp_filename):
    data = None
    full_path = "/tmp/{}".format(tmp_filename)
    try:
        f = open(full_path, 'r')
        data = "\n".join(f.readlines())
        f.close()
    except Exception as e:
        print("{}: {}".format(full_path, str(e)))

    if os.path.exists(full_path):
        os.remove(full_path)

    return data
