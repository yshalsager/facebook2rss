from dateparser import parse


class Notification:
    def __init__(self, url, content, date, logo=None):
        self.url = url
        self.content = content
        self.title = content
        self.date = parse(date, settings={'RETURN_AS_TIMEZONE_AWARE': True}) if date else None
        self.logo = logo if logo else "https://static.xx.fbcdn.net/rsrc.php/yo/r/iRmz9lCMBD2.ico"
