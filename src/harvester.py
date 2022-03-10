import logging
import traceback

import tweepy

from database.sql_session import session_scope
from models.tweet import (Cashtag, Hashtag, ReferencedCashtag,
                          ReferencedHashtag, ReferencedTweet, ReferencedUser,
                          Source, Tweet, User)


class Harvester(tweepy.StreamingClient):
    def __init__(self, bearer_token, *, return_type=..., wait_on_rate_limit=False, **kwargs):
        super().__init__(bearer_token, return_type=return_type,
                         wait_on_rate_limit=wait_on_rate_limit, **kwargs)
        self.logger = logging.getLogger(__name__)

    def on_response(self, response):
        # check for errors
        if response.errors:
            self.logger.error(response.errors)
            return super().on_response(response)
        if response.data.lang == 'de' or response.data.lang == 'en':
            try:
                with session_scope() as session:
                    id = response.data.id

                    source = session.query(Source)\
                        .filter(Source.name == response.data.source)\
                        .first()

                    if not source:
                        source = Source(
                            id=None,
                            name=response.data.source
                        )
                        session.add(source)
                        session.flush()

                    for user_data in response.includes.get('users'):
                        test = session.query(User)\
                            .filter(User.id == user_data.id)\
                            .first()

                        if not test:
                            user = User(
                                id=user_data.id,
                                name=user_data.name,
                                username=user_data.username,
                                created_at=user_data.created_at,
                                location=user_data.location,
                                profile_image_url=user_data.profile_image_url
                            )
                            session.add(user)

                    session.flush()
                    tw = Tweet(
                        id=id,
                        text=response.data.text,
                        author_id=response.data.author_id,
                        created_at=response.data.created_at,
                        conversation_id=response.data.conversation_id,
                        in_reply_to_user_id=response.data.in_reply_to_user_id,
                        language=response.data.lang,
                        source_id=source.id
                    )
                    session.add(tw)

                    if response.data.referenced_tweets:
                        for ref_tweet_data in response.data.referenced_tweets:
                            ref_tweet = ReferencedTweet(
                                id=None,
                                source_id=id,
                                target_id=ref_tweet_data.id,
                                reference_type=ref_tweet_data.type
                            )
                            session.add(ref_tweet)
                    if response.data.entities.get('mentions'):
                        for mention in response.data.entities.get('mentions'):
                            ref_user = ReferencedUser(
                                id=None,
                                tweet_id=id,
                                user_id=mention.get('id')
                            )
                            session.add(ref_user)
                    if response.data.entities.get('hashtags'):
                        for hashtag_data in response.data.entities.get('hashtags'):
                            tag = hashtag_data.get('tag')
                            hashtag = session.query(Hashtag)\
                                .filter(Hashtag.tag == tag)\
                                .first()

                            if not hashtag:
                                hashtag = Hashtag(
                                    id=None,
                                    tag=hashtag_data.get('tag')
                                )
                                session.add(hashtag)
                                session.flush()

                            ref_hashtag = ReferencedHashtag(
                                id=None,
                                tweet_id=id,
                                tag_id=hashtag.id,
                                start=hashtag_data.get('start'),
                                end=hashtag_data.get('end')
                            )
                            session.add(ref_hashtag)
                    if response.data.entities.get('cashtags'):
                        for cashtag_data in response.data.entities.get('cashtags'):
                            tag = cashtag_data.get('tag')
                            cashtag = session.query(Cashtag)\
                                .filter(Cashtag.tag == tag)\
                                .first()

                            if not cashtag:
                                cashtag = Cashtag(
                                    id=None,
                                    tag=cashtag_data.get('tag')
                                )
                                session.add(cashtag)
                                session.flush()

                            ref_cashtag = ReferencedCashtag(
                                id=None,
                                tweet_id=id,
                                tag_id=cashtag.id,
                                start=cashtag_data.get('start'),
                                end=cashtag_data.get('end')
                            )
                            session.add(ref_cashtag)

                    session.commit()

            except Exception:
                traceback.print_exc()

        return super().on_response(response)
