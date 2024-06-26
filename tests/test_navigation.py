import pytest
from pages.home import HomePage
from playwright.sync_api import expect, Page


@pytest.mark.skip(reason="")
def test_navigation_bar(page: Page, home_page: HomePage) -> None:

    shop_page = home_page.load().go_to_shop()
    expect(page).to_have_url(shop_page.URL)
    cart_page = shop_page.go_to_cart()
    expect(page).to_have_url(cart_page.URL)
    home_page = cart_page.go_to_home()
    expect(page).to_have_url(home_page.URL)
