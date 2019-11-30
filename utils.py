from sys import argv
from exceptions import TooManyArgumentsError, MissingRequiredArgumentError, SiteNameError


def get_protocol(url, allowed_protocols=('http', 'https')):
    protocol = url.strip().split(':')[0]
    if protocol not in allowed_protocols:
        protocol = None
    return protocol


def get_domain_name(url):
    domain_name = url.strip().split('//')[-1].split('/')[0]
    if '.' not in domain_name:
        raise SiteNameError()
    return domain_name


def get_full_domain(url, default_protocol='http'):
    protocol = get_protocol(url)
    domain_name = get_domain_name(url)
    if not protocol:
        protocol = default_protocol
    return f'{protocol}://{domain_name}/'


def get_url_from_terminal():
    if len(argv) < 2:
        raise MissingRequiredArgumentError()

    if len(argv) > 2:
        raise TooManyArgumentsError()

    return get_full_domain(argv[-1])


def clean_link(link, base_url, disallowed_ext=('jpg', 'png', 'gif', 'pdf')):
    domain_name = get_domain_name(base_url)

    if link.startswith('http://' + domain_name) or link.startswith('https://' + domain_name):
        result = link
    elif link.startswith('/'):
        result = get_full_domain(base_url)[:-1] + link
    elif ':' in link or '#' in link:
        result = None
    else:
        result = base_url + link

    if result:
        for ext in disallowed_ext:
            if result.lower().endswith(ext):
                result = None
                break

    return result


