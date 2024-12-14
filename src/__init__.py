from flask import Flask
from src.config.config import Config

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from src.utils import generate_random_string

Base = declarative_base()

DATABASE_URL = "postgresql://root:root@host.docker.internal/my-box"

engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine)
session = Session()

app = Flask(__name__)

app.secret_key = generate_random_string(16)

config = Config()