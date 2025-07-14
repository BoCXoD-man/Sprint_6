# coding=utf-8

import allure
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
        Клик по логотипу Самоката должен перенаправлять на главную страницу.
        Args:
            driver: WebDriver
        """
        page = MainPage(driver)
        page.open()
        page.click_scooter_logo()
        page.url_should_contain("qa-scooter")

    @allure.story("Клик по логотипу Яндекса открывает Дзен/Яндекс")
    def test_click_yandex_logo_opens_dzen(self, driver):
        """
        Клик по логотипу Яндекса должен открывать новую вкладку с Дзен/Яндекс.
        Args:
            driver: WebDriver
        """
        page = MainPage(driver)
        page.open()
        original_window = driver.current_window_handle
        page.click_yandex_logo()

        page.wait_for_tab_count(2)
        page.switch_to_new_tab(original_window)
        page.wait_for_url_change_from("about:blank")

        current_url = page.get_current_url()
        assert (
            "dzen.ru" in current_url
            or "yandex.ru" in current_url
            or "ya.ru" in current_url
        ), f"Непредвиденный URL: {current_url}"