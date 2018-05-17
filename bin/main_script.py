import os
import click
import yaml
import logging
import logging.config
from build_data import get_word_dependencies, generate_network


def setup_logging(default_path='logging.yaml', default_level=logging.INFO, env_key='LOG_CFG'):
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


@click.group()
def cli():
    pass


@click.command(name='fetch-wordnet-data')
@click.option('--word', default='music_genre')
def fetch_wordnet_data(word):
    get_word_dependencies(word)
    generate_network(word)


cli.add_command(fetch_wordnet_data)

if __name__ == '__main__':
    setup_logging()
    cli()
