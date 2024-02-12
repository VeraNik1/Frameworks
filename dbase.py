from databases import Database
from sqlalchemy import MetaData, Table, Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy import create_engine
from models import Status

DATABASE_URL = "sqlite:///store_db.db"

database = Database(DATABASE_URL)
metadata = MetaData()


users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(32)),
    Column("surname", String(32)),
    Column("email", String(128)),
    Column("password", String(64)),
)

products = Table(
    "products",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(48)),
    Column("description", String(150)),
    Column("cost", Float),
)

orders = Table(
    "orders",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey('users.id')),
    Column("product_id", Integer, ForeignKey('products.id')),
    Column("date", DateTime),
    Column("status", String(16)),
)


engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata.create_all(engine)