from playwright.sync_api import Page
from pages.checkout import CheckoutPage
import pytest
from pages.home import HomePage


@pytest.mark.skip(reason="")
def test_shop_page_buy_toys(
    page: Page, home_page: HomePage, details: dict[str, dict[str, str]]
) -> None:
    contact_details = details["contact"]
    delivery_details = details["delivery"]
    payment_details = details["payment"]
    home_page.load().go_to_shop().buy_toy_by_title("test_toy").buy_toy_by_title(
        "Rubik's Cube"
    ).go_to_cart().click_checkout().fill_out_contact_details_form(
        contact_details
    ).fill_out_delivery_details_form(
        same_as_contact=False, delivery_details=delivery_details
    ).fill_out_payment_details_form(
        payment_details
    )

    page.pause()
