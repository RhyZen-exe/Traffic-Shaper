from core.storage import get_connection, create_tables

conn = get_connection("data/test_storage.db")
create_tables(conn)
print("Таблицы созданы")
conn.close()