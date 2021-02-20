#!/bin/bash
python3 -m  facebook_rss --login -u $EMAIL -p $PASSWORD
uvicorn facebook_rss.main:api --host 0.0.0.0 --port 8000
