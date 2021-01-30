import re
from urllib.parse import urlparse


def strip_tags(string: str, allowed_tags: str = '<a><img><i><u><br><p>'):
    """
    Remove xml style tags from an input string.
    Original source is https://www.calebthorne.com/blog/python/2012/06/08/python-strip-tags
    :param string The input string.
    :param allowed_tags A string to specify tags which should not be removed.
    """
    if allowed_tags != '':
        # Get a list of all allowed tag names.
        allowed_tags_list = re.sub(r'[\\/<> ]+', '', allowed_tags).split(',')
        allowed_pattern = ''
        for s in allowed_tags_list:
            if s == '':
                continue;
            # Add all possible patterns for this tag to the regex.
            if allowed_pattern != '':
                allowed_pattern += '|'
            allowed_pattern += '<' + s + ' [^><]*>$|<' + s + '>|'
        # Get all tags included in the string.
        all_tags = re.findall(r'<]+>', string, re.I)
        for tag in all_tags:
            # If not allowed, replace it.
            if not re.match(allowed_pattern, tag, re.I):
                string = string.replace(tag, '')
    else:
        # If no allowed tags, remove all.
        string = re.sub(r'<[^>]*?>', '', string)

    return string


def clean_urls(html: str) -> str:
    urls = re.findall(
        r'(https?://(www\.)?[-\w\d@:%._+~#=]{1,256}\.[\w\d()]{1,6}\b[-\w\d()!@:%_+.~#?&/=;]*)', html)
    for url, _ in urls:
        url_parts = urlparse(url)
        html = html.replace(url, f"{url_parts.scheme}/{url_parts.hostname}{url_parts.path}")
    return html


def get_url_without_tracking(url: str) -> str:
    return re.sub(r'&refid=.*', '', url)
