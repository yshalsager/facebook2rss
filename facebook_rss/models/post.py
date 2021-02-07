class Post:
    def __init__(self, url, title, content, author, logo=None):
        self.url = url
        self.content = content
        self.title = f"{content[:30]}..." if not title else title
        self.author = author
        self.logo = logo if logo else "https://static.xx.fbcdn.net/rsrc.php/yo/r/iRmz9lCMBD2.ico"
