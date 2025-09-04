import logging
from typing import Generator

import redis
from sqlmodel import Session, create_engine

from services import config

logger = logging.getLogger(__name__)

# Global instances - will be initialized in lifespan
engine = None
redis_client = None


def init_db():
    """Initialize database engine and create tables"""
    global engine
    logger.info("Initializing database: %s", config.DATABASE_URL)
    try:
        engine = create_engine(config.DATABASE_URL)

        # Note: Schema and table creation is now handled by Alembic migrations
        # Run 'uv run alembic upgrade head' to apply migrations
        logger.info(
            "Database engine initialized. Run migrations with: uv run alembic upgrade head"
        )
    except Exception as e:
        logger.error("Failed to initialize database: %s", e)
        raise e


def init_redis():
    """Initialize Redis client"""
    global redis_client
    logger.info("Initializing Redis client: %s", config.REDIS_URL)
    try:
        redis_client = redis.from_url(config.REDIS_URL, decode_responses=True)
        # Test connection
        redis_client.ping()
        logger.info("Redis client initialized successfully")
    except Exception as e:
        logger.error("Failed to initialize Redis client: %s", e)
        raise e


def close_redis():
    """Close Redis connection"""
    global redis_client
    if redis_client:
        logger.info("Closing Redis connection")
        redis_client.close()
        redis_client = None


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency to get database session"""
    if engine is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")

    session = Session(engine)
    try:
        yield session
    finally:
        session.close()


def get_redis() -> redis.Redis:
    """FastAPI dependency to get Redis client"""
    if redis_client is None:
        raise RuntimeError("Redis not initialized. Call init_redis() first.")
    return redis_client
