import oracledb
import os
from dotenv import load_dotenv

load_dotenv()

un = "scott"
cs = "localhost/orclpdb"
pw = os.getenv("ORACLE_PASSWORD")

with oracledb.connect(user=un, password=pw, dsn=cs) as connection:
    with connection.cursor() as cursor:
        sql = "select sysdate from dual"
        for r in cursor.execute(sql):
            print(r)