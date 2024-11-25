import psycopg2
from faker import Faker
import random

# Параметри підключення до бази даних
conn_params = {
    "dbname": "postgres",
    "user": "user",
    "password": "password",
    "port": 5432
}

# Ініціалізація Faker
faker = Faker()

# Функція для вставки випадкових даних
def insert_random_data():
    try:
        with psycopg2.connect(**conn_params) as conn:
            with conn.cursor() as cursor:
                # Вставка даних у таблицю Clients
                for _ in range(6):  # Додаємо 6 клієнтів
                    account_number = faker.iban()[:20]  # Обрізаємо значення до 20 символів
                    phone_number = faker.phone_number()[:15]
                    cursor.execute("""
                        INSERT INTO Clients (company_name, account_number, phone_number, contact_person, address)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (
                        faker.company(),
                        account_number,
                        phone_number,
                        faker.name(),
                        faker.address()
                    ))

                # Отримання всіх client_id для прив'язки автомобілів
                cursor.execute("SELECT client_id FROM Clients")
                client_ids = [row[0] for row in cursor.fetchall()]

                # Вставка даних у таблицю Cars
                car_brands = ["Fiesta", "Focus", "Fusion", "Mondeo"]
                for _ in range(10):  # Додаємо 10 автомобілів
                    cursor.execute("""
                        INSERT INTO Cars (car_brand, car_price, client_id)
                        VALUES (%s, %s, %s)
                    """, (
                        random.choice(car_brands),
                        round(random.uniform(15000, 50000), 2),  # Випадкова ціна від 15,000 до 50,000
                        random.choice(client_ids)
                    ))

                # Отримання всіх car_id для прив'язки ремонтів
                cursor.execute("SELECT car_id FROM Cars")
                car_ids = [row[0] for row in cursor.fetchall()]

                # Вставка даних у таблицю Repairs
                repair_types = ["гарантійний", "плановий", "капітальний"]
                for _ in range(15):  # Додаємо 15 ремонтів
                    cursor.execute("""
                        INSERT INTO Repairs (start_date, car_id, repair_type, hourly_rate, discount, repair_hours)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (
                        faker.date_this_year(),
                        random.choice(car_ids),
                        random.choice(repair_types),
                        round(random.uniform(20, 100), 2),  # Випадкова ціна за годину від 20 до 100
                        round(random.uniform(0, 10), 1),    # Випадкова знижка від 0 до 10%
                        random.randint(1, 8)                # Випадкова кількість годин (1-8)
                    ))

                conn.commit()
                print("Дані успішно додано.")
    except Exception as e:
        print(f"Помилка під час додавання даних: {e}")

# Виконання функції
if __name__ == "__main__":
    insert_random_data()
