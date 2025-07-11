import pytest
from selenium import webdriver
from datetime import datetime
import pytest
from faker import Faker
import random

fake = Faker('ru_RU')  # Русскоязычные данные

@pytest.fixture
def driver():
    """
    Фикстура для инициализации драйвера браузера.
    Открывает браузер перед тестом и закрывает после выполнения.
    
    Returns:
        WebDriver: экземпляр браузера
    """
    browser = webdriver.Firefox()
    browser.set_window_size(1920, 1080)
    yield browser  # после yield управление вернётся в тест, а когда тест завершится — выполнится код после yield
    browser.quit()  # закрытие браузера

@pytest.fixture
def today_date():
    """
    Возвращает сегодняшнюю дату в формате ДД.ММ.ГГГГ.
    
    Returns:
        str: строка текущей даты
    """
    return datetime.today().strftime("%d.%m.%Y")

@pytest.fixture
def fake_user():
    """
    Генерирует фейкового пользователя для формы заказа самоката.
    Returns:
        tuple: (имя, фамилия, адрес, метро, телефон, дату доставки, комментарий)
    """
    name = fake.first_name()
    surname = fake.last_name()
    address = f"г. Москва, {fake.street_name()}, д. {random.randint(1, 100)}"
    phone = f'89{random.randint(0, 999999999)}'
    comment = fake.sentence(nb_words=5)
    date = datetime.today().strftime("%d.%m.%Y")
    # Выбор из реальных станций, которые поддерживает сервис
    metro_choices = [
        "Черкизовская", "Сокольники", "Лубянка", "Курская", "Комсомольская",
        "Бульвар Рокоссовского", "Таганская", "Тверская", "Пушкинская"
    ]
    metro = random.choice(metro_choices)

    return name, surname, address, metro, phone, date, comment