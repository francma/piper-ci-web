import argparse
from pathlib import Path

import yaml

from piper_web.container import Container

parser = argparse.ArgumentParser()
parser.add_argument(
    'config',
    help='Configuration file',
    type=Path
)

parsed = vars(parser.parse_args())
config_path = parsed['config'].expanduser()
config = yaml.load(config_path.open())

container = Container(config)
app = container.get_app()


def main():
    app.run()


if __name__ == 'main':
    main()
