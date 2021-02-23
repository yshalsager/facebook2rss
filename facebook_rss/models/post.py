from dateparser import parse


class Post:
    def __init__(self, url, title, content, author, date, logo=None):
        self.url = url
        self.content = content
        self.title = f"{content[:30]}..." if not title else title
        self.author = author
        if isinstance(date, int):
            self.date = date
        elif isinstance(date, str):
            self.date = parse(date, settings={'RETURN_AS_TIMEZONE_AWARE': True})
        else:
            self.date = None
        self.logo = logo if logo else "https://static.xx.fbcdn.net/rsrc.php/yo/r/iRmz9lCMBD2.ico"
