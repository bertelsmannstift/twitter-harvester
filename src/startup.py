#!/usr/bin/env python3
import argparse
import logging
import logging.config

from database.sql_session import init_db
from harvester import Harvester
from utils.settings import get_settings


def init_argpase() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [Option] [FILE]...",
        description="This is my template for python programs.\nIt includes a main function, argument parsing and a logger."
    )
    parser.add_argument(
        '-v', '--version', action='version',
        version=f'{parser.prog} version 1.0.0'
    )
    parser.add_argument('files', nargs='*')
    return parser


def main() -> None:
    parser = init_argpase()
    args = parser.parse_args()

    logging.config.fileConfig('logging.conf')
    logger = logging.getLogger(__name__)

    logger.info(args)

    init_db()

    harvester = Harvester(bearer_token=get_settings().TWITTER_BEARERTOKEN)
    harvester.sample(
        expansions=['author_id', 'geo.place_id'],
        user_fields=['created_at', 'description', 'entities', 'id', 'location', 'name', 'pinned_tweet_id',
                     'profile_image_url', 'protected', 'public_metrics', 'url', 'username', 'verified', 'withheld'],
        place_fields=['contained_within', 'country', 'country_code',
                      'full_name', 'geo', 'id', 'name', 'place_type'],
        tweet_fields=['attachments', 'author_id', 'context_annotations', 'conversation_id', 'created_at', 'entities',
                      'geo', 'in_reply_to_user_id', 'lang', 'referenced_tweets', 'source']
    )

# TODO: Build Docker Compose File consisting of harvester and database
# TODO: Put Tweets into Database


if __name__ == '__main__':
    main()
