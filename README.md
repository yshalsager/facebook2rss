# Facebook to RSS API [WIP]

A small API for accessing Facebook profile, pages and groups posts as RSS feeds.

## Disclaimer

1- This tool is provided with no warranty of any kind. I am not responsible for anything that might happen to your
Facebook account that will be automated by this tool.

2- This tool is still experimental. It has been tested heavily and has a lot of features that are not implemented yet. I
built it for personal use but decided to release it as a public open source project.

## Installation

The tool requires Python 3.7 with pip v19+ installed or poetry if you use it.

Clone the repository and run any of the following commands:

**Using poetry**

```bash
poetry install
```

**Using Pip**

```bash
pip install .
```

## Usage

- First, login to Facebook using the following command that will save your session in order to be used later:

```bash
python3 -m facebook_rss --login -u email -p password
```

- Next, run the following command to start serving the API:

```bash
python3 -m facebook_rss
```

## Features

TODO

## Limitations

TODO

## Current status

- Only profile and pages posts can be accessed using /profile/[profile_name] API route.
- Data is being scraped from mbasic Facebook website that doesn't use Javascript and cached for 30 minutes.