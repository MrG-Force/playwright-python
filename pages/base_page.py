from __future__ import annotations
from abc import ABC
import os
from typing import TYPE_CHECKING
from playwright.sync_api import Page
import allure

if TYPE_CHECKING:
    from pages.home import HomePage
    from pages.shop import ShopPage
    from pages.cart import CartPage


class BasePage(ABC):
    """Abstract base page class"""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.URL = os.getenv("SUT_URL")

    @allure.step("Go to the home page")
    def go_to_home(self) -> HomePage:
        from pages.home import HomePage

        self.page.get_by_role("button", name="Home").click()
        return HomePage(self.page)

    @allure.step("Go to the shop page")
    def go_to_shop(self) -> ShopPage:
        from pages.shop import ShopPage

        self.page.get_by_role("button", name="Shop").click()
        return ShopPage(self.page)

    @allure.step("Go to the cart page")
    def go_to_cart(self) -> CartPage:
        from pages.cart import CartPage

        # Wait for the "has been added" message to disappear
        self.page.wait_for_selector("snack-bar-container", state="hidden")
        self.page.get_by_role("button", name="Cart").click()
        return CartPage(self.page)
