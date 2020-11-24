import json
import re
from html.parser import HTMLParser

AvailableServices = ['dyndns', 'ipify']

DefaultServiceOptions = {
    'dyndns': None,
    'ipify': 'text'
}

def IpExtractorFactory(service, service_options=DefaultServiceOptions):
    if service == 'dyndns':
        return DynDnsIpExtractor()
    elif service == 'ipify':
        return IpfyIpExtractor(service_options[service])
    else:
        raise Exception("Service not supported. {} not in {}".format(service, AvailableServices))

def IpValidator(ip):
    pattern = re.compile('(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[0-9]?[0-9])[.](25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[0-9]?[0-9])[.](25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[0-9]?[0-9])[.](25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[0-9]?[0-9])')
    pattern.fullmatch(ip)
    return True

class DynDnsIpExtractor(HTMLParser):

    service = 'dyndns'

    def __init__(self):
        self._ip = None
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
            if (len(splited_data) == 2):
                self._ip = splited_data[1].strip()
            else:
                raise Exception('Unparsable body content (i.e. "Current IP Address: xx.y.zzz.hhh"): "{}"'.format(data))

    def ip(self):
        if IpValidator(self._ip):
            return self._ip
        else:
            raise Exception("Not a valid ip: {}".format(self._ip))

class IpfyIpExtractor():

    service = 'ipify'
    available_type = ['text', 'json']

    def __init__(self, input_type):
        if (input_type == None or input_type not in IpfyIpExtractor.available_type):
            raise Exception("{} is not a valid input format. {}".format(input_type, IpfyIpExtractor.available_type))

        self._input_type = 'text' if input_type == None else input_type.lower().strip()
        self._input = None
        self._ip = None
    
    def feed(self, input):
        if self._input_type == 'json':
            self._input = json.loads(input)
            self._ip = self._input['ip']
        else:
            self._input = input
            self._ip = self._input
    
    def ip(self):
        if IpValidator(self._ip):
            return self._ip
        else:
            raise Exception("Not a valid ip: {}".format(self._ip))
