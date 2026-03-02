    import os

    class Config:
        SECRET_KEY = os.environ.get("SECRET_KEY", "fallback-secret-key")
    
        DATABASE_URL = os.environ.get("DATABASE_URL")
    
        if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
            DATABASE_URL = DATABASE_URL.replace(
                "postgres://", "postgresql://", 1
            )
    
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
        SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ================= CONNECTION POOL =================
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,      # Prevent stale connections
        "pool_recycle": 1800,       # Recycle every 30 mins
        "pool_size": 5,
        "max_overflow": 10,
        "pool_timeout": 30,
    }

    # ================= SESSION SETTINGS =================
    # Required for Render HTTPS
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
