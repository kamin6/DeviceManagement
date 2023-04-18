import os
from sqlalchemy import create_engine, text

db_connection = os.environ['DB_CONNECTION_STRING']

engine = create_engine(
  db_connection, 
  connect_args={
    "ssl": {
      "ssl_ca": "/etc/ssl/cert.pem"
    }
  }
)
    