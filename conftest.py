import pytest
from selenium import webdriver
from datetime import datetime
import pytest


@pytest.fixture(scope="class")
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
