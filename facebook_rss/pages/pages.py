from .main.login import LoginPage as MainLoginPage
from .mbasic.login import LoginPage as MBasicLoginPage
from .mobile.login import LoginPage as MobileLoginPage

pages = {
    "main": {
        "login": MainLoginPage
    },
    "mobile": {
        "login": MobileLoginPage
    },
    "mbasic": {
        "login": MBasicLoginPage
    }
}
