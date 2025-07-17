from datetime import datetime
from faker import Faker
import random

fake = Faker('ru_RU')  # Русскоязычные данные


def get_today_date():
    """
    Возвращает сегодняшнюю дату в формате ДД.ММ.ГГГГ.
    
    Returns:
        str: строка текущей даты
    """
    return datetime.today().strftime("%d.%m.%Y")


def get_fake_user():
    """
    Генерирует фейкового пользователя для формы заказа самоката.
    Returns:
        tuple: (имя, фамилия, адрес, метро, телефон, дату доставки, комментарий)
    """
    name = fake.first_name()
    surname = fake.last_name()
    address = f"г. Москва, {fake.street_name()}, д. {random.randint(1, 100)}"
    phone = f'89{random.randint(100000000, 999999999)}'
    comment = fake.sentence(nb_words=5)
    date = datetime.today().strftime("%d.%m.%Y")
    # Выбор из реальных станций, которые поддерживает сервис
    metro_choices = [
        "Черкизовская", "Сокольники", "Лубянка", "Курская", "Комсомольская",
        "Бульвар Рокоссовского", "Таганская", "Тверская", "Пушкинская"
    ]
    metro = random.choice(metro_choices)

    return name, surname, address, metro, phone, date, comment
