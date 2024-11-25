import psycopg2

# Параметри підключення до бази даних
conn_params = {
    "dbname": "postgres",
    "user": "user",
    "password": "password",
    "host": "localhost",
    "port": 5432
}

# Функція для виводу даних таблиці
def fetch_and_display_data():
    try:
        # Підключення до бази даних
        with psycopg2.connect(**conn_params) as conn:
            with conn.cursor() as cursor:
                # Отримання списку таблиць
                cursor.execute("""
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = 'public'
                """)
                tables = cursor.fetchall()

                for table in tables:
                    table_name = table[0]
                    print(f"\nДані з таблиці '{table_name}':")

                    # Отримання даних з таблиці
                    cursor.execute(f"SELECT * FROM {table_name}")
                    rows = cursor.fetchall()

                    # Отримання назв стовпців
                    col_names = [desc[0] for desc in cursor.description]

                    # Форматований вивід даних
                    if rows:
                        print(" | ".join(col_names))
                        print("-" * 50)
                        for row in rows:
                            print(" | ".join(map(str, row)))
                    else:
                        print("Таблиця порожня.")
    except Exception as e:
        print(f"Помилка під час отримання даних: {e}")

# Виконання функції
if __name__ == "__main__":
    fetch_and_display_data()
