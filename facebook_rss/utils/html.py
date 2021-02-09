import re
from urllib.parse import urlparse


def strip_tags(string, allowed_tags='a,img,i,u,br,p,strong'):
    """
    Remove html tags from an input string.
    based on https://www.calebthorne.com/blog/python/2012/06/08/python-strip-tags
    :param string The input string.
    :param allowed_tags A string to specify tags which should not be removed, separated by commas.
    """
    if allowed_tags != '':
        # Get a list of all allowed tag names.
        allowed_tags = allowed_tags.split(',')
        allowed_tags_pattern = ['</?' + allowed_tag + '[^>]*>' for allowed_tag in allowed_tags]
        all_tags = re.findall(r'<[^>]+>', string, re.I)
        not_allowed_tags = []
        for tag in all_tags:
            if not [True for pattern in allowed_tags_pattern if re.match(pattern, tag)]:
                not_allowed_tags.append(tag)
        for not_allowed_tag in not_allowed_tags:
            string = re.sub(re.escape(not_allowed_tag), '', string)
    else:
        # If no allowed tags, remove all.
        string = re.sub(r'<[^>]*?>', '', string)

    return string


def clean_urls(html: str) -> str:
    urls = re.findall(
        r'(https?://(www\.)?[-\w\d@:%._+~#=]{1,256}\.[\w\d()]{1,6}\b[-\w\d()!@:%_+.~#?&/=;]*)', html)
    for url, _ in urls:
        if 'photo.php' in url or 'video_redirect' in url:
            html = html.replace(url, get_url_without_tracking(url))
        else:
            url_parts = urlparse(url)
            html = html.replace(url, f"{url_parts.scheme}/{url_parts.hostname}{url_parts.path}")
    return html


def get_url_without_tracking(url: str) -> str:
    return re.sub(r'&refid=.*', '', url)
