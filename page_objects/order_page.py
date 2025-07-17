from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import allure
from page_objects.base_page import BasePage

class OrderPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.name = (By.XPATH, "//input[@placeholder='* Имя']")
        self.surname = (By.XPATH, "//input[@placeholder='* Фамилия']")
        self.address = (By.XPATH, "//input[@placeholder='* Адрес: куда привезти заказ']")
        self.metro = (By.CLASS_NAME, "select-search__input")
        self.metro_option = (By.CLASS_NAME, "select-search__option")
        self.phone = (By.XPATH, "//input[@placeholder='* Телефон: на него позвонит курьер']")
        self.next_button = (By.XPATH, "//button[text()='Далее']")
        self.date = (By.XPATH, "//input[@placeholder='* Когда привезти самокат']")
        self.rent_day = (By.CLASS_NAME, "Dropdown-control")
        self.option_1_day = (By.XPATH, "//div[text()='сутки']")
        self.black_color = (By.ID, "black")
        self.comment = (By.XPATH, "//input[@placeholder='Комментарий для курьера']")
        self.submit_button_modal = (By.XPATH, "//div[@class='Order_Buttons__1xGrp']//button[text()='Заказать']")
        self.confirm_button = (By.XPATH, "//button[text()='Да']")
        self.success_modal = (By.CLASS_NAME, "Order_ModalHeader__3FDaJ")

    @allure.step("Заполнение формы заказа пользовательскими данными")
    def fill_user_info(self, name, surname, address, metro, phone):
        """
        Заполняет форму заказа пользовательскими данными.
        Args:
            name (str): Имя пользователя.
            surname (str): Фамилия пользователя.
            address (str): Адрес пользователя.
            metro (str): Станция метро пользователя.
            phone (str): Телефон пользователя.
        """
        self.send_keys(self.name, name)
        self.send_keys(self.surname, surname)
        self.send_keys(self.address, address)
        self.send_keys(self.metro, metro)
        self.click(self.metro_option)
        self.send_keys(self.phone, phone)
        self.click(self.next_button)

    @allure.step("Заполнение информации о сроке аренды и комментарии")
    def fill_rent_info(self, date, comment):
        """
        Заполняет информацию о сроке аренды и комментарии.
        Args:
            date (str): Дата доставки в формате ДД.ММ.ГГГГ.
            comment (str): Комментарий для курьера.
        """
        self.wait_for_visible(self.date)
        date_input = self.find_element(self.date)
        date_input.clear()
        date_input.send_keys(date)
        date_input.send_keys(Keys.ENTER)

        self.scroll_to(self.rent_day)
        self.wait_for_clickable(self.rent_day)
        ActionChains(self.driver).move_to_element(self.find_element(self.rent_day)).perform()
        self.click(self.rent_day)
        self.click(self.option_1_day)

        self.click(self.black_color)
        self.send_keys(self.comment, comment)

        self.wait_for_clickable(self.submit_button_modal)
        self.click(self.submit_button_modal)
        self.click(self.confirm_button)
    

    @allure.step("Проверка успешности оформления заказа")
    def is_order_successful(self):
        return "Заказ оформлен" in self.get_text(self.success_modal)
