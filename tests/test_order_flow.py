# coding=utf-8

import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from page_objects.main_page import MainPage
from page_objects.order_page import OrderPage


@allure.epic("Заказ самоката")
@allure.feature("Позитивный сценарий заказа")
class TestScooterOrderFlow:
    def _fill_order_and_check_success(self, driver, user_data):
        """
        Заполняет форму заказа и проверяет успешность оформления заказа.
        Args:
            driver: WebDriver
            user_data (tuple): Кортеж с данными пользователя (имя, фамилия, адрес, станция метро, телефон, дата доставки, комментарий).
        """
        name, surname, address, metro, phone, date, comment = user_data

        order_page = OrderPage(driver)
        order_page.fill_user_info(name, surname, address, metro, phone)
        order_page.fill_rent_info(date, comment)

        # Проверяем, что заказ успешно оформлен
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located(order_page.success_modal)
        )
        assert order_page.is_order_successful()

    @allure.story("Заказ через верхнюю кнопку с набором 1")
    def test_order_flow_with_button_top(self, driver, today_date):
        """
        Заказ через верхнюю кнопку с набором 1. 
        Args:
            driver: WebDriver
            today_date: Текущая дата
        """
        main_page = MainPage(driver)
        main_page.open()
        main_page.click_order_button(position='top')

        user_data = (
            "Алекс", "Кош", "ул. Пушкина, Дом Колотушки",
            "Черкизовская", "89990000000", today_date, "Позвонить за час"
        )
        self._fill_order_and_check_success(driver, user_data)

    # !!! ЕСЛИ ХОЧЕТСЯ СТАТИЧНЫЕ ТЕСТОВЫЕ ДАННЫЕ, РАСКОММЕНТИРУЙТЕ СЛЕДУЮЩИЙ КОД !!!
    # @allure.story("Заказ через нижнюю кнопку с набором 2")
    # def test_order_flow_with_button_bottom(self, driver, today_date):
    #     main_page = MainPage(driver)
    #     main_page.open()
    #     main_page.click_order_button(position='bottom')

    #     user_data = (
    #         "Владислав", "Крапивин", "пр. Мира, 5",
    #         "Сокольники", "89991112233", today_date, "Попросить оставить у двери"
    #     )
    #     self._fill_order_and_check_success(driver, user_data)

    # !!! А тут немного творчества и импровизации
    @allure.story("Заказ через нижнюю кнопку с набором 2")
    def test_order_flow_with_button_bottom(self, driver, fake_user):
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
        self._fill_order_and_check_success(driver, fake_user)