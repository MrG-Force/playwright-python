from abc import ABC, abstractmethod
from playwright.sync_api import Page, TimeoutError


class BaseFormTab(ABC):
    """Abstract base class for stepper tabs that contain forms. This class provides methods to fill out text inputs and select fields."""

    def __init__(self, page: Page):
        self.page = page

    @abstractmethod
    def fill_form(self, data: dict) -> None:
        pass

    def fill_text_input(self, formcontrolname: str, value: str) -> None:
        active_tab = self.page.locator("[role='tabpanel'][aria-expanded='true']")
        input_field = active_tab.locator(f"[formcontrolname='{formcontrolname}']")
        input_field.click()
        input_field.fill(value)

    def set_select(self, formcontrolname: str, value: str) -> None:
        active_tab = self.page.locator("[role='tabpanel'][aria-expanded='true']")
        select_field = active_tab.locator(f"[formcontrolname='{formcontrolname}']")
        select_field.click()
        listbox = self.page.locator("[role='listbox']")

        try:
            option = listbox.locator(f"[role='option'][value='{value}']")
            option.wait_for(timeout=1000)
            option.click()
        except TimeoutError:
            raise ValueError(
                f"Option '{value}' not found for form input '{formcontrolname}'"
            )
