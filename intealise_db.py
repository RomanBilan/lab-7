import psycopg2

# Параметри підключення до бази даних
conn_params = {
    "dbname": "postgres",
    "user": "user",
    "password": "password",
    "host": "localhost",
    "port": 5432
}

# SQL-запити для створення таблиць
sql_create_tables = """
-- Таблиця Клієнти
CREATE TABLE IF NOT EXISTS Clients (
    client_id SERIAL PRIMARY KEY,
    company_name VARCHAR(100) NOT NULL,
    account_number VARCHAR(20) UNIQUE NOT NULL,
    phone_number VARCHAR(15) NOT NULL,
    contact_person VARCHAR(50),
    address VARCHAR(150)
);

-- Таблиця Автомобілі
CREATE TABLE IF NOT EXISTS Cars (
    car_id SERIAL PRIMARY KEY,
    car_brand VARCHAR(50) NOT NULL,
    car_price NUMERIC(10, 2) NOT NULL CHECK (car_price > 0),
    client_id INT NOT NULL REFERENCES Clients(client_id) ON DELETE CASCADE
);

-- Таблиця Ремонт
CREATE TABLE IF NOT EXISTS Repairs (
    repair_id SERIAL PRIMARY KEY,
    start_date DATE NOT NULL,
    car_id INT NOT NULL REFERENCES Cars(car_id) ON DELETE CASCADE,
    repair_type VARCHAR(20) NOT NULL CHECK (repair_type IN ('гарантійний', 'плановий', 'капітальний')),
    hourly_rate NUMERIC(8, 2) NOT NULL CHECK (hourly_rate > 0),
    discount NUMERIC(3, 1) NOT NULL CHECK (discount BETWEEN 0 AND 10),
    repair_hours INT NOT NULL CHECK (repair_hours > 0)
);
"""

# Функція для створення таблиць
def create_tables():
    try:
        # Підключення до бази даних
        with psycopg2.connect(**conn_params) as conn:
            with conn.cursor() as cursor:
                # Виконання SQL-запитів
                cursor.execute(sql_create_tables)
                conn.commit()
                print("Таблиці успішно створено.")
    except Exception as e:
        print(f"Помилка під час створення таблиць: {e}")

# Функція для вставки тестових даних
def insert_test_data():
    try:
        with psycopg2.connect(**conn_params) as conn:
            with conn.cursor() as cursor:
                # Вставка тестових даних у таблицю Clients
                clients = [
                    ("Компанія 1", "12345678901234567890", "123-456-7890", "Іван Іванов", "Київ, вул. Шевченка"),
                    ("Компанія 2", "09876543210987654321", "987-654-3210", "Петро Петренко", "Львів, вул. Франка")
                ]
                for client in clients:
                    # Перевіряємо, чи значення `account_number` не перевищує 20 символів
                    if len(client[1]) > 20:
                        print(f"Помилка: значення account_number занадто довге: {client[1]}")
                        continue
                    cursor.execute("""
                        INSERT INTO Clients (company_name, account_number, phone_number, contact_person, address)
                        VALUES (%s, %s, %s, %s, %s)
                    """, client)

                conn.commit()
                print("Тестові дані успішно додано.")
    except Exception as e:
        print(f"Помилка під час вставки даних: {e}")

# Виконання функцій
if __name__ == "__main__":
    create_tables()
    insert_test_data()
