from urllib.parse import urlparse

def extract_base_url(url):
    return '/'.join(url.split('/')[:3])

def fix_url(url):
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        return "https://" + url
    return url
