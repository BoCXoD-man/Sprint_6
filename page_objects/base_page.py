from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    """
    Базовый класс для всех страниц, содержащий общие методы и локаторы."""
    def __init__(self, driver, timeout=5):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def find_element(self, locator):
        """
        Находит элемент по локатору.
        Args:
            locator (tuple): Кортеж из стратегии поиска и значения локатора.
        Returns:
            WebElement: найденный элемент.
        """
        return self.driver.find_element(*locator)

    def find_elements(self, locator):
        """
        Находит элементы по локатору.
        Args:
            locator (tuple): Кортеж из стратегии поиска и значения локатора.
        Returns:
            list: Список найденных элементов.
        """
        return self.driver.find_elements(*locator)

    def click(self, locator):
        """
        Кликает по элементу, найденному по локатору.
        Args:
            locator (tuple): Кортеж из стратегии поиска и значения локатора.
        """
        self.wait_for_clickable(locator)
        self.find_element(locator).click()

    def send_keys(self, locator, text):
        """
        Отправляет текст в элемент, найденный по локатору.
        Args:
            locator (tuple): Кортеж из стратегии поиска и значения локатора.
            text (str): Текст для отправки.
        """
        self.find_element(locator).send_keys(text)

    def clear(self, locator):
        """
        Очищает текст в элементе, найденном по локатору.
        Args:
            locator (tuple): Кортеж из стратегии поиска и значения локатора.
        """
        self.find_element(locator).clear()

    def send_keys_with_clear(self, locator, text):
        """
        Очищает поле и отправляет текст.
        Args:
            locator (tuple): Кортеж из стратегии поиска и значения локатора.
            text (str): Текст для отправки.
        """
        el = self.find_element(locator)
        el.clear()
        el.send_keys(text)

    def wait_for_clickable(self, locator):
        """
        Ожидает, что элемент станет кликабельным.
        Args:
            locator (tuple): Кортеж из стратегии поиска и значения локатора.
        """
        self.wait.until(EC.element_to_be_clickable(locator))

    def get_text(self, locator):
        """
        Получает текст из элемента.
        Args:
            locator (tuple): Кортеж из стратегии поиска и значения локатора.
        Returns:
            str: Текст элемента.
        """
        return self.find_element(locator).text

    def scroll_to(self, locator):
        """
        Скроллит страницу до элемента, найденного по локатору.
        Args:
            locator (tuple): Кортеж из стратегии поиска и значения локатора.
        """
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)

    def current_url_contains(self, substring: str) -> bool:
        """Проверяет, что текущий URL содержит подстроку.
        Args:
            substring (str): Подстрока для проверки в URL."""
        return substring in self.driver.current_url

    def wait_for_new_window(self, count: int = 2):
        """Ожидает, что появится новое окно.
        Args:
            count (int): Ожидаемое количество окон. По умолчанию 2.
        """
        self.wait.until(EC.number_of_windows_to_be(count))

    def switch_to_new_window(self, original_handle: str) -> str:
        """Переключается на новое окно, отличное от оригинального.
        Args:
            original_handle (str): Хэндл оригинального окна.
        Returns:
            str: Хэндл нового окна.
        """
        new_window = [w for w in self.driver.window_handles if w != original_handle][0]
        self.driver.switch_to.window(new_window)
        return new_window

    def wait_for_url_change(self, from_url: str):
        """Ожидает, что URL изменится от указанного.
        Args:
            from_url (str): URL, от которого ожидается изменение.
        """
        self.wait.until(lambda d: d.current_url != from_url)

    def get_current_url(self) -> str:
        """Получает текущий URL страницы.
        Returns:
            str: Текущий URL страницы.
        """
        return self.driver.current_url

    def wait_for_visible(self, locator):
        """
        Ожидает, что элемент станет видимым.
        Args:
            locator (tuple): Кортеж из стратегии поиска и значения локатора.
        """
        self.wait.until(EC.visibility_of_element_located(locator))

    def wait_until_text_not_empty(self, locator, timeout=5):
        """
        Ожидает, что текст элемента по локатору станет непустым.
        """
        WebDriverWait(self.driver, timeout).until(
            lambda d: self.find_element(locator).text.strip() != ""
        )
