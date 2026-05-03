# @ISITWEDNESDAY Bot

https://x.com/isitwednesday

1. Tweets when it's Wednesday, and when it's not. 
2. Listens to `#isitwednesday` `#isitwednesdayyet` `#whenisitwednesday` https://x.com/isitwednesday
and responds to the tweet to the let person know which timezones it is Wednesday for. 


# Dev
Prereqs:
- Python >=3.13
- [uv](https://docs.astral.sh/uv/)


## Install
`$ make install`

UV will make a .venv directory with the pyproject.toml required python version and dependencies.

## Package
`$ make package`

## Deploy
`$ make deploy-post-service`

`$ make deploy-reply-service`
