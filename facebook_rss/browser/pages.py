from .main.group import GroupPage as MainGroupPage
from .main.login import LoginPage as MainLoginPage
from .main.login_checkpoint import LoginCheckpointPage as MainLoginCheckpointPage
from .main.notification import NotificationPage as MainNotificationPage
from .main.page import FBPage as MainPage
from .main.profile import ProfilePage as MainProfilePage
from .mbasic.group import GroupPage as MBasicGroupPage
from .mbasic.login import LoginPage as MBasicLoginPage
from .mbasic.login_checkpoint import LoginCheckpointPage as MBasicLoginCheckpointPage
from .mbasic.notification import NotificationPage as MBasicNotificationPage
from .mbasic.page import FBPage as MBasicPage
from .mbasic.profile import ProfilePage as MBasicProfilePage
from .mobile.login import LoginPage as MobileLoginPage

pages = {
    "main": {
        "login": MainLoginPage,
        "login_checkpoint": MainLoginCheckpointPage,
        "profile": MainProfilePage,
        "page": MainPage,
        "group": MainGroupPage,
        "notification": MainNotificationPage,
    },
    "mobile": {
        "login": MobileLoginPage
    },
    "mbasic": {
        "login": MBasicLoginPage,
        "login_checkpoint": MBasicLoginCheckpointPage,
        "profile": MBasicProfilePage,
        "page": MBasicPage,
        "group": MBasicGroupPage,
        "notification": MBasicNotificationPage
    }
}
