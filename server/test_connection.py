import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="uudex",
    user="uudex_user",
    password="uudex")

cur = conn.cursor()

cur.execute("select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';")            

print(cur.fetchall())