# coding=utf-8

import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from page_objects.main_page import MainPage


@allure.epic("Главная страница")
@allure.feature("Редиректы")
class TestRedirects:
    """
    Тесты на проверку корректности редиректов с логотипов на главной странице:
    - Логотип Самоката ведет на главную страницу сервиса.
    - Логотип Яндекса открывает новую вкладку с Дзен/Яндекс.
    """

    @allure.story("Клик по логотипу Самоката ведет на главную")
    def test_click_scooter_logo_redirects_to_main(self, driver):
        """
        Проверяет, что при клике на логотип 'Самокат' происходит переход на главную страницу (url содержит 'qa-scooter').
        """
        page = MainPage(driver)
        page.open()
        page.click_scooter_logo()
        assert "qa-scooter" in driver.current_url, "Ожидался редирект на главную страницу Самоката"

    @allure.story("Клик по логотипу Яндекса открывает Дзен/Яндекс")
    def test_click_yandex_logo_opens_dzen(self, driver):
        """
        Проверяет, что при клике на логотип Яндекса открывается новая вкладка с Дзен/Яндекс.
        """
        page = MainPage(driver)
        page.open()
        original_window = driver.current_window_handle
        page.click_yandex_logo()

        # Ожидание открытия новой вкладки
        WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))

        # Получаем дескриптор новой вкладки (которая открылась после клика)
        # Генерируем список всех вкладок и выбираем ту, которая не является оригинальной
        new_window = [w for w in driver.window_handles if w != original_window][0]  # Их должно быть только две до этого шага

        # Переключаемся на новую вкладку для продолжения работы
        driver.switch_to.window(new_window)

        # Ожидание загрузки URL
        WebDriverWait(driver, 10).until(lambda d: d.current_url != "about:blank")
        current_url = driver.current_url

        assert (
            "dzen.ru" in current_url
            or "yandex.ru" in current_url
            or "ya.ru" in current_url
        ), f"Непредвиденный URL: {current_url}"