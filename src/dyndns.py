from html.parser import HTMLParser

class DynDnsIpExtractor(HTMLParser):

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
        return self._ip
