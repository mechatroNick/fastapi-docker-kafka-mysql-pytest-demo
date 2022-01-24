from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

if os.getenv("AWS_RDS_URL"):
    SQLALCHEMY_DATABASE_URI = "mysql://{}:{}@{}?ssl_ca={}".format(
        os.getenv("AWS_RDS_CHANNEL_DATABASE_USER", "user"),
        os.getenv("AWS_RDS_CHANNEL_DATABASE_PWD", "password"),
        os.getenv("AWS_RDS_URL", "mysql:3306/db"),
        os.getenv("AWS_RDS_SSL_CERT_PATH", "/certs/rds-ca-2019-root.pem"),
    )
    engine = create_engine(
        SQLALCHEMY_DATABASE_URI,
        convert_unicode=True,
        pool_size=5,
        max_overflow=10,
    )
elif os.getenv("USE_LOCAL_MYSQL"):
    SQLALCHEMY_DATABASE_URI = "mysql://{}:{}@{}/{}".format(
        os.getenv("DB_USER", "user"),
        os.getenv("DB_PASSWORD", "password"),
        os.getenv("DB_HOST", "mysql:3306"),
        os.getenv("DB_NAME", "db"),
    )
    engine = create_engine(
        SQLALCHEMY_DATABASE_URI,
        convert_unicode=True,
        pool_size=5,
        max_overflow=10,
    )
else:
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    engine = create_engine(SQLALCHEMY_DATABASE_URI)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
