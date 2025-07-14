import allure
from selenium.webdriver.common.by import By
from page_objects.base_page import BasePage
from page_objects.order_page import OrderPage

class MainPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://qa-scooter.praktikum-services.ru/"
        self.order_button_top = (By.XPATH, "//button[text()='Заказать'][1]")
        self.order_button_bottom = (By.XPATH, "//button[text()='Заказать'][last()]")
        self.logo_scooter = (By.CLASS_NAME, "Header_LogoScooter__3lsAR")
        self.logo_yandex = (By.CLASS_NAME, "Header_LogoYandex__3TSOI")
        self.questions = (By.CLASS_NAME, "accordion__button")
        self.answers = (By.CLASS_NAME, "accordion__panel")

    @allure.step("Открытие главной страницы")
    def open(self):
        self.driver.get(self.url)

    @allure.step("Клик по кнопке 'Заказать' в позиции: {position}")
    def click_order_button(self, position='top'):
        if position == 'top':
            self.click(self.order_button_top)
        else:
            self.click(self.order_button_bottom)

    @allure.step("Клик по вопросу под номером {index}")
    def click_question(self, index):
        self.scroll_to(self.questions)  # Скроллим к блоку вопросов
        self.wait_for_clickable(self.questions)  # Ждём кликабельность любого из них
        self.find_elements(self.questions)[index].click()

    @allure.step("Получение текста ответа на вопрос {index}")
    def get_answer_text(self, index):
        return self.find_elements(self.answers)[index].text

    @allure.step("Клик по логотипу Самоката")
    def click_scooter_logo(self):
        self.click(self.logo_scooter)

    @allure.step("Клик по логотипу Яндекса")
    def click_yandex_logo(self):
        self.click(self.logo_yandex)

    @allure.step("Проверка, что URL содержит '{substring}'")
    def url_should_contain(self, substring):
        assert substring in self.get_current_url(), f"URL не содержит '{substring}'"

    @allure.step("Ожидание появления новой вкладки")
    def wait_for_tab_count(self, expected: int = 2):
        self.wait_for_new_window(expected)

    @allure.step("Переключение на новую вкладку (не {original_handle})")
    def switch_to_new_tab(self, original_handle: str):
        return self.switch_to_new_window(original_handle)

    @allure.step("Проверка, что URL изменился от {from_url}")
    def wait_for_url_change_from(self, from_url: str):
        self.wait_for_url_change(from_url)

    def get_answer_locator(self, index):
        """
        Вспомогательный метод для получения локатора ответа на вопрос.
        Формирует локатор для ответа на вопрос по индексу.
        Args:
            index (int): Индекс вопроса (0-based).
        Returns:
            tuple: Кортеж из стратегии поиска и значения локатора.
        """
        return (By.XPATH, f"(//div[contains(@class, 'accordion__panel')])[{index + 1}]")
    

    def get_question_locator(self, index):
        """
        Вспомогательный метод для получения локатора вопроса.
        Формирует локатор для вопроса по индексу.
        Args:
            index (int): Индекс вопроса (0-based).
        Returns:
            tuple: Кортеж из стратегии поиска и значения локатора.
        """
        return (By.XPATH, f"(//div[contains(@class, 'accordion__button')])[{index + 1}]")

    
    @allure.step("Проверка точного ответа на вопрос {index}")
    def check_exact_answer(self, index, expected_text):
        question_locator = self.get_question_locator(index)
        answer_locator = self.get_answer_locator(index)

        self.scroll_to(question_locator)
        self.click(question_locator)

        self.wait_until_text_not_empty(answer_locator)
        actual = self.get_text(answer_locator).strip()
        assert actual == expected_text, f"Ожидалось: {expected_text}, получено: {actual}"

    def fill_order_and_check_success(self, driver, user_data):
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

        # Ожидаем отображение модального окна с подтверждением
        order_page.wait_for_visible(order_page.success_modal)

        assert order_page.is_order_successful()
