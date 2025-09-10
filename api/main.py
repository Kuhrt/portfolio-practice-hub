from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from middleware.exception_handlers import custom_http_exception_handler
from routers import (
    health_router,
    practice_goal_router,
    practice_session_router,
    user_router,
)
from services import close_redis, config, init_db, init_redis
from services.common.migration_service import run_migrations
from utils import get_keycloak_public_keys


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    print("🎵 Starting Practice Hub API...")

    # Initialize database
    try:
        init_db()
        print("✅ Database engine initialized")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        raise e

    # Run database migrations
    try:
        run_migrations()
        print("✅ Database migrations completed")
    except Exception as e:
        print(f"❌ Database migrations failed: {e}")
        raise e

    # Initialize Redis
    try:
        init_redis()
        print("✅ Redis initialized")
    except Exception as e:
        print(f"❌ Redis initialization failed: {e}")
        raise e

    # Verify Keycloak connection
    try:
        get_keycloak_public_keys.cache_clear()
        get_keycloak_public_keys()  # Test connection
        print("✅ Keycloak connection verified")
    except Exception as e:
        print(f"❌ Keycloak connection failed: {e}")

    yield

    # Shutdown
    print("🎵 Shutting down Practice Hub API...")
    close_redis()
    print("✅ Redis connection closed")


app = FastAPI(
    title="Practice Hub API",
    description="API for tracking music practice sessions",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[config.WEB_APP_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add exception handlers
app.add_exception_handler(HTTPException, custom_http_exception_handler)
app.add_exception_handler(RequestValidationError, custom_http_exception_handler)
app.add_exception_handler(Exception, custom_http_exception_handler)

# Include routers
api_prefix = "/api"
app.include_router(health_router, prefix=api_prefix)
app.include_router(practice_goal_router, prefix=api_prefix)
app.include_router(practice_session_router, prefix=api_prefix)
app.include_router(user_router, prefix=api_prefix)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(config.PORT if config.PORT else 8000),
        reload=True if config.ENVIRONMENT == "development" else False,
    )
