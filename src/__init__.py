import logging
import os

import twitter_service
import twitter_auth

LOG_LEVEL = os.environ.get("LOG_LEVEL") or "DEBUG"

logging.root.setLevel(LOG_LEVEL)

if __name__ == '__main__':

    twitter_service.post_wednesday_tweet()
    print('do something here')
