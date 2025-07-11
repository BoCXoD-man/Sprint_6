from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

class OrderPage:
    def __init__(self, driver):
        self.driver = driver
        self.name = (By.XPATH, "//input[@placeholder='* Имя']")
        self.surname = (By.XPATH, "//input[@placeholder='* Фамилия']")
        self.address = (By.XPATH, "//input[@placeholder='* Адрес: куда привезти заказ']")
        self.metro = (By.CLASS_NAME, "select-search__input")
        self.phone = (By.XPATH, "//input[@placeholder='* Телефон: на него позвонит курьер']")
        self.next_button = (By.XPATH, "//button[text()='Далее']")
        self.date = (By.XPATH, "//input[@placeholder='* Когда привезти самокат']")
        self.rent_day = (By.CLASS_NAME, "Dropdown-control")
        self.option_1_day = (By.XPATH, "//div[text()='сутки']")
        self.black_color = (By.ID, "black")
        self.comment = (By.XPATH, "//input[@placeholder='Комментарий для курьера']")
        self.submit_button = (By.XPATH, "//button[text()='Заказать']")
        self.confirm_button = (By.XPATH, "//button[text()='Да']")
        self.success_modal = (By.CLASS_NAME, "Order_ModalHeader__3FDaJ")

    def fill_user_info(self, name, surname, address, metro, phone):
        """ 
        Заполняет информацию о пользователе в форме заказа.
        Args:
            name (str): Имя пользователя.
            surname (str): Фамилия пользователя.
            address (str): Адрес пользователя.
            metro (str): Станция метро пользователя.
            phone (str): Телефон пользователя.
        """
        self.driver.find_element(*self.name).send_keys(name)
        self.driver.find_element(*self.surname).send_keys(surname)
        self.driver.find_element(*self.address).send_keys(address)
        self.driver.find_element(*self.metro).send_keys(metro)
        self.driver.find_element(By.CLASS_NAME, "select-search__option").click() # клик по элементу станции метро в выпадающем списке после того, как пользователь начал ввод в поле.
        self.driver.find_element(*self.phone).send_keys(phone)
        self.driver.find_element(*self.next_button).click()

    def fill_rent_info(self, date, comment):
        """ Заполняет информацию о сроке аренды и комментарии в форме заказа.
        Args:
            date (str): Дата доставки.
            comment (str): Комментарии к заказу.
        """
        # Вводим дату доставки
        date_input = self.driver.find_element(*self.date)
        date_input.clear() # Очищаем поле ввода даты, если там что-то есть
        date_input.send_keys(date)
        date_input.send_keys(Keys.ENTER) # Подтверждаем ввод даты

        # Скроллим к дропдауну (выпадающему списку) срока аренды
        rent_dropdown = self.driver.find_element(*self.rent_day)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", rent_dropdown)

        # Явное ожидание, пока элемент не станет кликабельным
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.rent_day))

        # Наводим мышь
        ActionChains(self.driver).move_to_element(rent_dropdown).perform()

        # Кликаем по дропдауну и выбираем срок аренды
        rent_dropdown.click()
        self.driver.find_element(*self.option_1_day).click()

        # Выбираем цвет самоката
        self.driver.find_element(*self.black_color).click()

        # Вводим комментарий
        self.driver.find_element(*self.comment).send_keys(comment)
        # Ожидаем вторую кнопку "Заказать" в форме доставки
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='Order_Buttons__1xGrp']//button[text()='Заказать']"))
        )
        self.driver.find_element(By.XPATH, "//div[@class='Order_Buttons__1xGrp']//button[text()='Заказать']").click()
        
        # Подтверждаем заказ
        self.driver.find_element(*self.confirm_button).click()

    def is_order_successful(self):
        """ Проверяет, что заказ успешно оформлен.
        Returns:
            bool: True, если заказ успешно оформлен, False в противном случае.
        """
        return "Заказ оформлен" in self.driver.find_element(*self.success_modal).text