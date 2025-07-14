# coding=utf-8

import allure
import pytest
from page_objects.main_page import MainPage
from test_data import expected_answers


@allure.epic("Главная страница")
@allure.feature("Блок 'Вопросы о важном'")
class TestImportantQuestions:
    """
    Тесты для проверки ответов на вопросы в блоке "Вопросы о важном" на главной странице.
    """
    @pytest.mark.parametrize("index", list(expected_answers.keys()))
    def test_faq_answers(self, driver, index):
        page = MainPage(driver)
        page.open()
        """
        Параметризованный тест: проверяет, что ответ по индексу совпадает с ожидаемым.
        Args:
            index (int): Индекс вопроса в блоке "Вопросы о важном".
        """
        allure.dynamic.story(f"Проверка вопроса {index + 1}")

        with allure.step(f"Проверка точного текста ответа на вопрос {index + 1}"):
            page.check_exact_answer(index, expected_answers[index])
