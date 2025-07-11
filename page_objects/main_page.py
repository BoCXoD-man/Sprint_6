from selenium.webdriver.common.by import By

class MainPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://qa-scooter.praktikum-services.ru/"
        self.order_button_top = (By.XPATH, "//button[text()='Заказать'][1]")
        self.order_button_bottom = (By.XPATH, "//button[text()='Заказать'][last()]")
        self.logo_scooter = (By.CLASS_NAME, "Header_LogoScooter__3lsAR")
        self.logo_yandex = (By.CLASS_NAME, "Header_LogoYandex__3TSOI")
        self.questions = (By.CLASS_NAME, "accordion__button")
        self.answers = (By.CLASS_NAME, "accordion__panel")

    def open(self):
        """Открывает главную страницу."""
        self.driver.get(self.url)

    def click_order_button(self, position='top'):
        """
        Кликает по кнопке "Заказать" в зависимости от позиции.
        Args:
            position (str): 'top' для верхней кнопки, 'bottom' для нижней.
        """
        if position == 'top':
            self.driver.find_element(*self.order_button_top).click()
        else:
            self.driver.find_element(*self.order_button_bottom).click()

    def click_question(self, index):
        """
        Кликает по вопросу в блоке "Вопросы о важном" по индексу.
        Args:
            index (int): Индекс вопроса в списке вопросов.
        """
        self.driver.find_elements(*self.questions)[index].click()

    def get_answer_text(self, index):
        """
        Получает текст ответа на вопрос по индексу.
        Args:
            index (int): Индекс вопроса в списке вопросов.
        """
        return self.driver.find_elements(*self.answers)[index].text

    def click_scooter_logo(self):
        """Кликает по логотипу Самоката, чтобы вернуться на главную страницу."""
        self.driver.find_element(*self.logo_scooter).click()

    def click_yandex_logo(self):
        """Кликает по логотипу Яндекса, чтобы вернуться на главную страницу."""
        self.driver.find_element(*self.logo_yandex).click()