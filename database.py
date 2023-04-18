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

# Method for fetching all the members from the database
def load_members_from_db():
  with engine.connect() as conn:
    members_data = conn.execute(text("select * from members"))
    members = {}
    for row in members_data.all():
      members[row[0]] = row[1]
    return members

# Method for fetching all the devices associated with the given memberId
def load_devices_from_db(memberId):
  with engine.connect() as conn:
    devices_data = conn.execute(
      text(f"""select * from devices where OWNER='{memberId}'"""))
    devicesOfMember = list(devices_data)
    return devicesOfMember
    