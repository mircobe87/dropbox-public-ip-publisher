import requests
from html.parser import HTMLParser


class PublicIpService:
    END_POINT = "https://checkip.dyndns.it/"

    def _call_remote_service(self):
        resp = requests.get(self.END_POINT)
        if resp.status_code == 200:
            return resp.text
        else:
            raise Exception("Unable to retrieve current public ip. Remote call returned <{} {}>".format(resp.status_code, resp.reason))

    def get_public_ip(self):
        raw_response = self._call_remote_service()
        html_parser = _DynDnsIpExtractor()
        html_parser.feed(raw_response)
        ip = html_parser.ip()
        return ip


class _DynDnsIpExtractor(HTMLParser):

    def __init__(self):
        self._ip = ""
        self._body_start = False
        self._body_data = None
        super(_DynDnsIpExtractor, self).__init__()

    def error(self, message):
        pass

    def handle_starttag(self, tag, attrs):
        if tag == 'body':
            self._body_start = True

    def handle_endtag(self, tag):
        self._body_start = False

    def handle_data(self, data):
        if self._body_start:
            self._body_data = data
            splited_data = data.split(':')
            if len(splited_data) == 2:
                self._ip = splited_data[1].strip()
            else:
                raise Exception('Unparsable body content (i.e. "Current IP Address: xx.y.zzz.hhh"): "{}"'.format(data))

    def ip(self):
        return self._ip
