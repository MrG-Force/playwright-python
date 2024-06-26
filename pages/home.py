from pages.base_page import BasePage
import allure


class HomePage(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.URL = f"{self.URL}/home"

    @allure.step("Load the home page")
    def load(self) -> "HomePage":
        self.page.goto(f"{self.URL}/home")
        return self
