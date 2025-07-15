
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure

class BasePage:
    """
    Базовый класс для всех страниц, содержащий общие методы и локаторы.
    """
    def __init__(self, driver, timeout=5):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    @allure.step("Поиск одного элемента: {locator}")
    def find_element(self, locator):
        """
        Ищет один элемент по локатору.
        Args:
            locator (tuple): Локатор элемента.
        Returns:
            WebElement: Найденный элемент.
        """
        return self.driver.find_element(*locator)

    @allure.step("Поиск нескольких элементов: {locator}")
    def find_elements(self, locator):
        """
        Ищет несколько элементов по локатору.
        Args:
            locator (tuple): Локатор элемента.
        Returns:
            list: Список найденных элементов.
        """
        return self.driver.find_elements(*locator)

    @allure.step("Клик по элементу: {locator}")
    def click(self, locator):
        """
        Кликает по элементу, ожидая его кликабельности.
        Args:
            locator (tuple): Локатор элемента.
        """
        self.wait_for_clickable(locator)
        self.find_element(locator).click()

    @allure.step("Ввод текста '{text}' в элемент: {locator}")
    def send_keys(self, locator, text):
        """
        Вводит текст в элемент.
        Args:
            locator (tuple): Локатор элемента.
            text (str): Текст для ввода.
        """
        self.find_element(locator).send_keys(text)

    @allure.step("Очистка текста в элементе: {locator}")
    def clear(self, locator):
        """
        Очищает текст в элементе.
        Args:
            locator (tuple): Локатор элемента.
        """
        self.find_element(locator).clear()

    @allure.step("Очистка и ввод текста '{text}' в элемент: {locator}")
    def send_keys_with_clear(self, locator, text):
        """
        Очищает текст в элементе и вводит новый текст.
        Args:
            locator (tuple): Локатор элемента.
            text (str): Текст для ввода.
        """
        el = self.find_element(locator)
        el.clear()
        el.send_keys(text)

    @allure.step("Ожидание кликабельности элемента: {locator}")
    def wait_for_clickable(self, locator):
        """
        Ожидает, что элемент станет кликабельным.
        Args:
            locator (tuple): Локатор элемента.
        """
        self.wait.until(EC.element_to_be_clickable(locator))

    @allure.step("Получение текста элемента: {locator}")
    def get_text(self, locator):
        """
        Получает текст элемента по локатору.
        Args:
            locator (tuple): Локатор элемента.
        Returns:
            str: Текст элемента.
        """
        return self.find_element(locator).text

    @allure.step("Скролл до элемента: {locator}")
    def scroll_to(self, locator):
        """
        Скроллит страницу до указанного элемента.
        Args:
            locator (tuple): Локатор элемента, до которого нужно скроллить.
        """
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)

    @allure.step("Проверка, что текущий URL содержит подстроку: {substring}")
    def current_url_contains(self, substring: str) -> bool:
        """ Проверяет, что текущий URL содержит указанную подстроку.
        Args:
            substring (str): Подстрока, которую нужно найти в URL.
        Returns:
            bool: True, если подстрока найдена, иначе False.
        """
        return substring in self.driver.current_url

    @allure.step("Ожидание появления нового окна (всего ожидается {count})")
    def wait_for_new_window(self, count: int = 2):
        """
        Ожидает появления нового окна.
        Args:
            count (int): Ожидаемое количество окон. По умолчанию 2.
        """
        self.wait.until(EC.number_of_windows_to_be(count))

    @allure.step("Переключение на новое окно (не {original_handle})")
    def switch_to_new_window(self, original_handle: str) -> str:
        """Переключение на новое окно.
        Args:
            original_handle (str): Хэндл оригинального окна, чтобы не переключаться обратно на него.
        Returns:
            str: Хэндл нового окна.
        """   
        new_window = [w for w in self.driver.window_handles if w != original_handle][0]
        self.driver.switch_to.window(new_window)
        return new_window

    @allure.step("Ожидание смены URL от {from_url}")
    def wait_for_url_change(self, from_url: str):
        """
        Ожидает, что текущий URL изменится от указанного.
        Args:
            from_url (str): URL, от которого ожидается изменение.
        """
        self.wait.until(lambda d: d.current_url != from_url)

    @allure.step("Получение текущего URL")
    def get_current_url(self) -> str:
        """Возвращает текущий URL страницы."""
        return self.driver.current_url

    @allure.step("Ожидание видимости элемента: {locator}")
    def wait_for_visible(self, locator):
        """
        Ожидает, что элемент станет видимым.
        Args:
            locator (tuple): Локатор элемента.
        """
        self.wait.until(EC.visibility_of_element_located(locator))

    @allure.step("Ожидание непустого текста в элементе: {locator}")
    def wait_until_text_not_empty(self, locator, timeout=5):
        """
        Ожидает, что текст в элементе не будет пустым.
        Args:   
            locator (tuple): Локатор элемента.
            timeout (int): Максимальное время ожидания в секундах.
        """
        WebDriverWait(self.driver, timeout).until(
            lambda d: self.find_element(locator).text.strip() != ""
        )
