import requests


class PublicIpService:
    END_POINT = "https://api.ipify.org?format=json"

    def _call_remote_service(self):
        resp = requests.get(self.END_POINT)
        if resp.status_code == 200:
            return resp.json()
        else:
            raise Exception("Unable to retrieve current public ip. Remote call returned <{} {}>".format(resp.status_code, resp.reason))

    def get_public_ip(self):
        return self._call_remote_service()['ip']

