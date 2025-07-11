# coding=utf-8

import allure
import pytest
from selenium import webdriver
from page_objects.main_page import MainPage


@allure.epic("Главная страница")
@allure.feature("Блок 'Вопросы о важном'")
class TestImportantQuestions:
    """
    Тесты для проверки ответов на вопросы в блоке "Вопросы о важном" на главной странице.
    """

    expected_answers = {
        0: "Сутки — 400 рублей. Оплата курьеру — наличными или картой.",
        1: "Пока что у нас так: один заказ — один самокат. Если хотите покататься с друзьями, можете просто сделать несколько заказов — один за другим.",
        2: "Допустим, вы оформляете заказ на 8 мая. Мы привозим самокат 8 мая в течение дня. Отсчёт времени аренды начинается с момента, когда вы оплатите заказ курьеру. Если мы привезли самокат 8 мая в 20:30, суточная аренда закончится 9 мая в 20:30.",
        3: "Только начиная с завтрашнего дня. Но скоро станем расторопнее.",
        4: "Пока что нет! Но если что-то срочное — всегда можно позвонить в поддержку по красивому номеру 1010.",
        5: "Самокат приезжает к вам с полной зарядкой. Этого хватает на восемь суток — даже если будете кататься без передышек и во сне. Зарядка не понадобится.",
        6: "Да, пока самокат не привезли. Штрафа не будет, объяснительной записки тоже не попросим. Все же свои.",
        7: "Да, обязательно. Всем самокатов! И Москве, и Московской области.",
    }

    @classmethod
    def setup_class(cls):
        """Инициализация драйвера и открытие страницы перед всеми тестами."""
        cls.driver = webdriver.Firefox()
        cls.page = MainPage(cls.driver)
        cls.page.open()

    def _check_exact_answer(self, index, expected_text):
        """
        Вспомогательный метод для проверки точного ответа на вопрос.
        Args:
            index (int): Индекс вопроса в блоке "Вопросы о важном".
            expected_text (str): Ожидаемый текст ответа на вопрос.
        """
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        question_element = self.driver.find_elements(By.CLASS_NAME, "accordion__button")[index]
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", question_element)
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, "accordion__button")))
        question_element.click()
        WebDriverWait(self.driver, 5).until(
            lambda d: self.page.get_answer_text(index).strip() != ""
        )
        actual_text = self.page.get_answer_text(index).strip()
        assert actual_text == expected_text

    @pytest.mark.parametrize("index", list(expected_answers.keys()))
    def test_faq_answers(self, index):
        """
        Параметризованный тест: проверяет, что ответ по индексу совпадает с ожидаемым.
        Args:
            index (int): Индекс вопроса в блоке "Вопросы о важном".
        """
        allure.dynamic.story(f"Проверка вопроса {index + 1}")

        with allure.step(f"Проверка точного текста ответа на вопрос {index + 1}"):
            self._check_exact_answer(index, self.expected_answers[index])
    
    @classmethod
    def teardown_class(cls):
        """Закрытие браузера после завершения всех тестов."""
        cls.driver.quit()

