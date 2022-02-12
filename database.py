from dotenv import load_dotenv
import mariadb
import os
import sys

#load envs
load_dotenv()
db_user = os.getenv("DB_USER")
db_passwd = os.getenv("DB_PASSWD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_db = os.getenv("DB_DB")
token = os.getenv("DISCORD_TOKEN")
ipc_secret_key = os.getenv("IPC_SECRET_KEY")
dc_client_id = os.getenv("DISCORD_CLIENT_ID")
dc_client_secret = os.getenv("DISCORD_CLIENT_SECRET")
dc_callback_uri = os.getenv("DISCORD_CALLBACK_URI")


try:
    db = mariadb.connect(
        user=db_user,
        password=db_passwd,
        host=db_host,
        port=int(db_port),
        database=db_db
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

cur = db.cursor()

#database functions
def create_table(table):
    sql = "CREATE TABLE IF NOT EXISTS %s (setting VARCHAR(255), value VARCHAR(255))" % table
    cur.execute(sql)

def insert(table, setting, value):
  sql = "INSERT INTO %s.%s (setting, value) VALUES ('%s', '%s')"
  val = (os.getenv("DB_DB"), table, setting, value)
  sql = sql % val
  cur.execute(sql)
  db.commit()


def read_all(table):
  cur.execute("SELECT * FROM %s.%s" % os.getenv("DB_DB") % table)
  result = cur.fetchall()
  for x in result:
    return x

def read_one(table, setting):
  cur.execute("SELECT value FROM %s.%s WHERE setting=%s" % os.getenv("DB_DB") % table % setting)
  result = cur.fetchone()
  return result

def update(table, setting, value):
    sql = "UPDATE s%.%s SET value=%s WHERE setting=%s"
    val = (os.getenv("DB_DB"), table, value, setting)
    cur.execute(sql, val)
    db.commit()

def delete(table, setting):
    sql = "DELETE FROM %s.%s WHERE setting=%s"
    val = (os.getenv("DB_DB"), table, setting)
    cur.execute(sql, val)
    cur.commit()