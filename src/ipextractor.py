import json
import re
from html.parser import HTMLParser

AvailableServices = ['dyndns', 'ipify']

DefaultServiceOptions = {
    'dyndns': None,
    'ipify': 'text'
}


def ip_extractor_factory(service, service_options=DefaultServiceOptions):
    if service == 'dyndns':
        return DynDnsIpExtractor()
    elif service == 'ipify':
        return IpifyIpExtractor(service_options[service])
    else:
        raise Exception("Service not supported. {} not in {}".format(service, AvailableServices))


def _ip_validator(ip):
    pattern = re.compile(
        '^(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[0-9]?[0-9])[.]'
        '(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[0-9]?[0-9])[.]'
        '(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[0-9]?[0-9])[.]'
        '(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[0-9]?[0-9])$'
    )
    pattern.fullmatch(ip)
    return True


class DynDnsIpExtractor(HTMLParser):
    def error(self, message):
        pass

    service = 'dyndns'

    def __init__(self):
        self._ip = ""
        self._body_start = False
        self._body_data = None
        super(DynDnsIpExtractor, self).__init__()

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
        if _ip_validator(self._ip):
            return self._ip
        else:
            raise Exception("Not a valid ip: {}".format(self._ip))


class IpifyIpExtractor:
    service = 'ipify'
    available_type = ['text', 'json']

    def __init__(self, input_type):
        if input_type is None or input_type not in IpifyIpExtractor.available_type:
            raise Exception("{} is not a valid input format. {}".format(input_type, IpifyIpExtractor.available_type))

        self._input_type = 'text' if input_type is None else input_type.lower().strip()
        self._input = None
        self._ip = ""

    def feed(self, input_data):
        if self._input_type == 'json':
            self._input = json.loads(input_data)
            self._ip = self._input['ip'].strip()
        else:
            self._input = input_data
            self._ip = self._input.strip()

    def ip(self):
        if _ip_validator(self._ip):
            return self._ip
        else:
            raise Exception("Not a valid ip: {}".format(self._ip))
