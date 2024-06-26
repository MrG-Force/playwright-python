"""Page Object for the Shop Page"""

from pages.base_page import BasePage


class ShopPage(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.wait_for_products_to_load()
        self.URL = f"{self.URL}/toy-list"

    def wait_for_products_to_load(self):
        """Wait for the products to load on the page"""
        self.page.wait_for_selector(".product")

    def buy_toy_by_title(self, title: str, quantity: int = 1) -> "ShopPage":
        """Buy a given quantity of a toy by its title."""
        for _ in range(quantity):
            product_tile = self.page.locator(
                f'xpath=//li[.//div[h4[text()="{title}"]]]'
            ).first
            product_tile.get_by_role("button", name="Buy").click()

        return self

    def buy_these_toys(
        self, toys: list[dict[str, str]], quantity: int = None
    ) -> "ShopPage":
        """
        Buy a list of toys with optional quantity.

        Iterates over the list of toys and buys each toy by title. If a quantity is provided,
        it uses that quantity for each toy. Otherwise, it defaults to an incremental quantity
        starting from 1; i.e., buy one of the first one, two of the second one, and so on.

        Parameters:
        toys (list[dict[str, str]]): A list of toy dictionaries with a "title" key.
        quantity (int, optional): The quantity to buy for each toy. Defaults to None for incremental quantities.

        Returns:
        ShopPage: The instance of the ShopPage for method chaining.

        Example:
        shop_page.buy_these_toys([{"title": "Toy 1"}, {"title": "Toy 2"}])
        shop_page.buy_these_toys([{"title": "Toy 1"}, {"title": "Toy 2"}], quantity=5)
        """
        for i, toy in enumerate(toys):
            qty = quantity if quantity is not None else i + 1
            self.buy_toy_by_title(toy["title"], qty)

        return self
