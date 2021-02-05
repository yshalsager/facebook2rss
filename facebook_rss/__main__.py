"""entry point"""
import argparse
import asyncio
from sys import exit as exit_

from facebook_rss import local_cookies
from facebook_rss.main import run_api
from facebook_rss.tasks.login import login_and_get_cookies

parser = argparse.ArgumentParser(prog='python3 -m facebook_rss')
# group = parser.add_mutually_exclusive_group(required=True)
parser.add_argument("--login", help="Login to facebook", action="store_true")
parser.add_argument("-u", "--email", help="Email address", type=str)
parser.add_argument("-p", "--password", help="Facebook password", type=str)
parser.add_argument("-d", "--development", help="Run in development mode", action="store_true")

args = parser.parse_args()

if __name__ == '__main__':
    if args.login:
        if not args.email:
            print("You must provide an email address!")
            exit_(1)
        if not args.password:
            print("You must provide a password!")
            exit_(1)
        asyncio.run(login_and_get_cookies(args.email, args.password))
    else:
        if not local_cookies.exists():
            print("Either you have not logged in yet or the provided cookies file doesn't exists!")
            exit_(1)
        asyncio.run(run_api(development_mode=args.development))
