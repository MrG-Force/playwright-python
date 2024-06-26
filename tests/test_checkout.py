import pytest
import allure
from playwright.sync_api import Page
from pages.checkout import CheckoutPage
from pages.home import HomePage


@allure.title("Test e2e checkout journey with contact details same as delivery")
# @pytest.mark.usefixtures("setup_teardown_toys")
def test_e2e_checkout_journey_with_contact_details_same_as_delivery(
    home_page: HomePage,
    toys: list[dict[str, str]],
    details: dict[str, dict[str, str]],
) -> None:
    """Test the end-to-end checkout journey with same contact and delivery details"""
    contact_details = details["contact"]
    payment_details = details["payment"]

    checkout_page: CheckoutPage = (
        home_page.load()
        .go_to_shop()
        .buy_these_toys(toys, 1)
        .go_to_cart()
        .click_checkout()
        .fill_out_contact_details_form(contact_details)
        .fill_out_delivery_details_form(same_as_contact=True)
        .fill_out_payment_details_form(payment_details)
    )

    with allure.step("Assert the order total"):
        expected_total = f"Total {sum([float(toy['price']) for toy in toys])}"
        checkout_page.assert_order_total(expected_total)

    order_items = checkout_page.get_order_items()
    actual_contact_details = checkout_page.get_contact_details()
    actual_delivery_details = checkout_page.get_delivery_details()
    actual_payment_details = checkout_page.get_payment_details()

    with allure.step(
        "Assert the order items and contact, delivery, and payment details"
    ):
        assert len(order_items) == len(toys)
        assert checkout_page.order_contains_items(toys)

        assert actual_contact_details["full_name"] == contact_details["full_name"]
        assert actual_contact_details["full_address"] == contact_details["full_address"]
        assert actual_contact_details["email"] == contact_details["email"]
        assert actual_contact_details["phone_number"] == contact_details["phone_number"]

        assert actual_delivery_details["full_name"] == contact_details["full_name"]
        assert (
            actual_delivery_details["full_address"] == contact_details["full_address"]
        )  # delivery address is the same as contact address

        assert actual_payment_details["name_on_card"] == payment_details["name_on_card"]
        assert actual_payment_details["card_number"] == payment_details["card_number"]
        assert actual_payment_details["card_type"] == payment_details["card_type"]
        assert actual_payment_details["expiry_date"] == payment_details["expiry_date"]
        assert actual_payment_details["cvv"] == payment_details["cvv"]

    # page.pause() # Just for debugging purposes on headed mode
    with allure.step("Submit the order"):
        checkout_page.click_submit_order()

    order_status = checkout_page.get_order_status()
    order_number = checkout_page.get_order_number()

    with allure.step("Assert the order was successfully submitted"):
        assert order_number != ""

    print(f"Order status: {order_status}")
    print(f"Order number: {order_number}")


@allure.title("Test e2e checkout journey with contact details not same as delivery")
# @pytest.mark.usefixtures("setup_teardown_toys")
def test_e2e_checkout_journey_with_contact_details_not_same_as_delivery(
    page: Page,
    home_page: HomePage,
    toys: list[dict[str, str]],
    details: dict[str, dict[str, str]],
) -> None:
    """Test the end-to-end checkout journey with same contact and delivery details"""
    contact_details = details["contact"]
    delivery_details = details["delivery"]
    payment_details = details["payment"]

    checkout_page: CheckoutPage = (
        home_page.load()
        .go_to_shop()
        .buy_these_toys(toys, 1)
        .go_to_cart()
        .click_checkout()
        .fill_out_contact_details_form(contact_details)
        .fill_out_delivery_details_form(delivery_details, False)
        .fill_out_payment_details_form(payment_details)
    )

    expected_total = f"Total {sum([float(toy['price']) for toy in toys])}"
    checkout_page.assert_order_total(expected_total)

    order_items = checkout_page.get_order_items()
    actual_contact_details = checkout_page.get_contact_details()
    actual_delivery_details = checkout_page.get_delivery_details()
    actual_payment_details = checkout_page.get_payment_details()

    assert len(order_items) == len(toys)
    assert checkout_page.order_contains_items(toys)

    assert actual_contact_details["full_name"] == contact_details["full_name"]
    assert actual_contact_details["full_address"] == contact_details["full_address"]
    assert actual_contact_details["email"] == contact_details["email"]
    assert actual_contact_details["phone_number"] == contact_details["phone_number"]

    assert actual_delivery_details["full_name"] == delivery_details["full_name"]
    assert actual_delivery_details["full_address"] == delivery_details["full_address"]

    assert actual_payment_details["name_on_card"] == payment_details["name_on_card"]
    assert actual_payment_details["card_number"] == payment_details["card_number"]
    assert actual_payment_details["card_type"] == payment_details["card_type"]
    assert actual_payment_details["expiry_date"] == payment_details["expiry_date"]
    assert actual_payment_details["cvv"] == payment_details["cvv"]

    # page.pause() # Just for debugging purposes on headed mode
    checkout_page.click_submit_order()
    order_status = checkout_page.get_order_status()
    order_number = checkout_page.get_order_number()
    # assert that order number is not empty
    assert order_number != ""
    print(f"Order status: {order_status}")
    print(f"Order number: {order_number}")
