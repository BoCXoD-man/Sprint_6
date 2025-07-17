# coding=utf-8

import allure
from page_objects.main_page import MainPage
from test_data import user_data
from utils import get_fake_user


@allure.epic("Заказ самоката")
@allure.feature("Позитивный сценарий заказа")
class TestScooterOrderFlow:

    @allure.story("Заказ через верхнюю кнопку с набором 1")
    def test_order_flow_with_button_top(self, driver, user_data=user_data):
        """
        Заказ через верхнюю кнопку с набором 1. 
        Args:
            driver: WebDriver
            today_date: Текущая дата
        """
        main_page = MainPage(driver)
        main_page.open()
        main_page.click_order_button(position='top')

        main_page.fill_order_and_check_success(driver, user_data)

    @allure.story("Заказ через нижнюю кнопку с набором 2")
    def test_order_flow_with_button_bottom(self, driver):
        """
        Заказ через нижнюю кнопку с набором 2.
        Args:
            driver: WebDriver
            today_date: Текущая дата
            fake_user: Фейковые данные пользователя
        """
        main_page = MainPage(driver)
        main_page.open()
        main_page.click_order_button(position='bottom')
        fake_user = get_fake_user()
        main_page.fill_order_and_check_success(driver, fake_user)
