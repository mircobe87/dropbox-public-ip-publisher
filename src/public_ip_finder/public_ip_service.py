import re
parent_name = '.'.join(__name__.split('.')[:-1])


def get_all_services():
    public_attributes = list(filter(lambda x: not x.startswith("__"), dir(services)))
    public_values = list(map(lambda x: getattr(services, x), public_attributes))
    return public_values


def check_service(name):
    return name in get_all_services()


def get_service(name):
    fully_qualified_name = "{}.service.{}.PublicIpService".format(parent_name, name)
    service = _get_object(fully_qualified_name)
    return service()


def check_ip(ip_str):
    pattern = re.compile(
        '^(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[0-9]?[0-9])[.]'
        '(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[0-9]?[0-9])[.]'
        '(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[0-9]?[0-9])[.]'
        '(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[0-9]?[0-9])$'
    )
    return pattern.fullmatch(ip_str) is not None


def _get_object(fully_qualified_name):
    parts = fully_qualified_name.split('.')
    module = ".".join(parts[:-1])
    m = __import__(module)
    for comp in parts[1:]:
        m = getattr(m, comp)
    return m


class services:

    DYNDNS = 'dyndns'
    IPIFY = 'ipify'

