from html import entities
from ssl import create_default_context
from tracemalloc import start
from unicodedata import name

from sqlalchemy import (BigInteger, Boolean, Column, DateTime, Float,
                        ForeignKey, Integer, String, null)

from models.base import Base


class Source(Base):
    __tablename__ = 'sources'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

    def __init__(self, id, name) -> None:
        super().__init__()
        self.id = id
        self.name = name


class User(Base):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True)
    name = Column(String(255))
    username = Column(String(255))
    created_at = Column(DateTime, nullable=False)
    location = Column(String(255))
    profile_image_url = Column(String(1000))

    def __init__(self, id, name, username, created_at, location, profile_image_url) -> None:
        super().__init__()
        self.id = id
        self.name = name
        self.username = username
        self.created_at = created_at
        self.location = location
        self.profile_image_url = profile_image_url


class Tweet(Base):
    """Monthly Posting database model mapping the `monthly_postings` table."""
    __tablename__ = 'tweets'
    id = Column(BigInteger, primary_key=True)
    text = Column(String(1000), nullable=False)
    author_id = Column(BigInteger, ForeignKey(
        User.id, ondelete="RESTRICT"), nullable=False)
    created_at = Column(DateTime, nullable=False)
    conversation_id = Column(BigInteger)
    in_reply_to_user_id = Column(BigInteger)
    language = Column(String(2))
    source_id = Column(Integer, ForeignKey(Source.id, ondelete="RESTRICT"))
    # geo

    def __init__(self, id, text, author_id, created_at, conversation_id, in_reply_to_user_id, language, source_id) -> None:
        super().__init__()
        self.id = id
        self.text = text
        self.author_id = author_id
        self.created_at = created_at
        self.conversation_id = conversation_id
        self.in_reply_to_user_id = in_reply_to_user_id
        self.language = language
        self.source_id = source_id

    def __repr__(self):
        return '<Tweet %r>' % self.text


class ReferencedTweet(Base):
    __tablename__ = 'referenced_tweets'
    id = Column(BigInteger, nullable=False, primary_key=True)
    source_id = Column(BigInteger, nullable=False)
    target_id = Column(BigInteger, nullable=False)
    reference_type = Column(String(255), nullable=False)

    def __init__(self, id, source_id, target_id, reference_type) -> None:
        super().__init__()
        self.id = id
        self.source_id = source_id
        self.target_id = target_id
        self.reference_type = reference_type


class Hashtag(Base):
    __tablename__ = 'hashtags'
    id = Column(BigInteger, nullable=False, primary_key=True)
    tag = Column(String(255), nullable=False)

    def __init__(self, id, tag) -> None:
        super().__init__()
        self.id = id
        self.tag = tag


class ReferencedHashtag(Base):
    __tablename__ = 'referenced_hashtags'
    id = Column(BigInteger, nullable=False, primary_key=True)
    tweet_id = Column(BigInteger, nullable=False)
    tag_id = Column(BigInteger, nullable=False)
    start = Column(Integer, nullable=False)
    end = Column(Integer, nullable=False)

    def __init__(self, id, tweet_id, tag_id, start, end) -> None:
        super().__init__()
        self.id = id
        self.tweet_id = tweet_id
        self.tag_id = tag_id
        self.start = start
        self.end = end


class Cashtag(Base):
    __tablename__ = 'cashtags'
    id = Column(BigInteger, nullable=False, primary_key=True)
    tag = Column(String(255), nullable=False)

    def __init__(self, id, tag) -> None:
        super().__init__()
        self.id = id
        self.tag = tag


class ReferencedCashtag(Base):
    __tablename__ = 'referenced_cashtags'
    id = Column(BigInteger, nullable=False, primary_key=True)
    tweet_id = Column(BigInteger, nullable=False)
    tag_id = Column(BigInteger, nullable=False)
    start = Column(Integer, nullable=False)
    end = Column(Integer, nullable=False)

    def __init__(self, id, tweet_id, tag_id, start, end) -> None:
        super().__init__()
        self.id = id
        self.tweet_id = tweet_id
        self.tag_id = tag_id
        self.start = start
        self.end = end


class ReferencedUser(Base):
    __tablename__ = 'referenced_users'
    id = Column(BigInteger, nullable=False, primary_key=True)
    tweet_id = Column(BigInteger, nullable=False)
    user_id = Column(BigInteger, nullable=False)

    def __init__(self, id, tweet_id, user_id) -> None:
        super().__init__()
        self.id = id
        self.tweet_id = tweet_id
        self.user_id = user_id
