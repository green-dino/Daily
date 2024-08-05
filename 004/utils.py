from urllib.parse import urlparse
import time
import requests

def extract_base_url(url):
    """
    Extract the base URL from a given URL.
    Example: 'https://example.com/path' -> 'https://example.com'
    """
    return '/'.join(url.split('/')[:3])

def fix_url(url):
    """
    Ensure the URL has a scheme (http or https). 
    If not, prepend 'https://' to the URL.
    Example: 'example.com' -> 'https://example.com'
    """
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        return "https://" + url
    return url

def delay(seconds):
    """
    Pause execution for a specified number of seconds.
    Example: delay(5) will pause for 5 seconds.
    """
    time.sleep(seconds)

def create_session(user_agent=None, referer=None):
    """
    Create a requests.Session with optional headers.
    Example:
    session = create_session(user_agent='Mozilla/5.0', referer='https://example.com')
    response = session.get('https://example.com')
    """
    session = requests.Session()
    
    headers = {}
    if user_agent:
        headers['User-Agent'] = user_agent
    if referer:
        headers['Referer'] = referer
    
    session.headers.update(headers)
    
    return session
