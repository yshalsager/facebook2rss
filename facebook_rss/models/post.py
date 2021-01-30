class Post:
    def __init__(self, url, html, title, content, author, text, logo=None):
        self.url = url
        self.html = html
        self.content = content
        self.title = f"{content[:30]}..." if not title else title
        self.author = author
        self.text = text
        self.logo = logo if logo else "https://static.xx.fbcdn.net/rsrc.php/yo/r/iRmz9lCMBD2.ico"
