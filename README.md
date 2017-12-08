# Piper CI web ui

## Requirements (non-pipy)

* Python >= 3.6

## Installation

1. Install requirements

2. Install project from github:

    `pip install git+https://github.com/francma/piper-ci-web.git`
    
3. That's it!

## Configuration

1. Copy example configuration:

    `cp config.example.yml config.yml`
    
2. Edit your config to fit your needs:
    
    `vim config.example.yml`

## Running

uwsgi (example):

`uwsgi --http-socket :[PORT] -w piper_web.run:app --pyargv [CONFIG_FILE]`

debug:

`piper-web [CONFIG_FILE]`

## Developer guide

Set `app.dummy` to `yes` in `[CONFIG_FILE]`