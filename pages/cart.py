from pages.base_page import BasePage
from pages.checkout import CheckoutPage


class CartPage(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.URL = f"{self.URL}/cart"

    def click_checkout(self) -> "CheckoutPage":
        self.page.get_by_role("link", name="Check Out").click()
        return CheckoutPage(self.page)
