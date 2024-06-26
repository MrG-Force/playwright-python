import re
from typing import Dict
from pages.base_page import BasePage
from pages.stepper_tabs.contact_tab import ContactDetailsTab
from playwright.sync_api import Locator, expect

from pages.stepper_tabs.delivery_tab import DeliveryDetailsTab
from pages.stepper_tabs.payment_tab import PaymentDetailsTab
from pages.stepper_tabs.confirm_order_tab import ConfirmOrderTab


class CheckoutPage(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.URL = f"{self.URL}/checkout"
        self.contact_details_tab: ContactDetailsTab = ContactDetailsTab(page)
        self.delivery_details_tab: DeliveryDetailsTab = None
        self.payment_details_tab: PaymentDetailsTab = None
        self.confirm_order_tab: ConfirmOrderTab = None

    def fill_out_contact_details_form(
        self, contact_details: dict[str, str]
    ) -> "CheckoutPage":
        """Fill out the contact details form"""
        self.delivery_details_tab = self.contact_details_tab.fill_form(
            contact_details
        ).click_next()
        return self

    def fill_out_delivery_details_form(
        self,
        delivery_details: dict[str, str] = None,
        same_as_contact: bool = False,
    ) -> "CheckoutPage":
        """
        Fill out the delivery details form, if same_as_contact is True, then the delivery details
        will be the same as the contact details and the form will be filled out automatically.
        """
        if self.delivery_details_tab is None:
            raise ValueError("DeliveryDetailsTab is not initialised")
        if delivery_details is None and not same_as_contact:
            raise ValueError("Delivery details not provided")
        if same_as_contact:
            self.payment_details_tab = self.delivery_details_tab.fill_form(
                same_as_contact
            ).click_next()
        else:
            self.payment_details_tab = self.delivery_details_tab.fill_form(
                same_as_contact=False, details=delivery_details
            ).click_next()
        return self

    def fill_out_payment_details_form(self, details: dict[str, str]) -> "CheckoutPage":
        if self.payment_details_tab is None:
            raise ValueError("PaymentDetailsTab is not initialised")
        self.confirm_order_tab = self.payment_details_tab.fill_form(
            details
        ).click_next()
        return self

    def get_order_total(self) -> Locator:
        return self.confirm_order_tab.get_order_total()

    def assert_order_total(self, expected_total: str) -> None:
        expect(self.get_order_total()).to_have_text(expected_total)

    def get_order_items(self) -> Dict[str, Dict[str, str]]:
        return self.confirm_order_tab.get_order_items()

    def order_contains_items(self, items: list[Dict[str, str]]) -> bool:
        return self.confirm_order_tab.order_contains_items(items)

    def get_contact_details(self) -> Dict[str, str]:
        return self.confirm_order_tab.get_contact_details()

    def get_delivery_details(self) -> Dict[str, str]:
        return self.confirm_order_tab.get_delivery_details()

    def get_payment_details(self) -> Dict[str, str]:
        return self.confirm_order_tab.get_payment_details()

    def click_submit_order(self) -> "CheckoutPage":
        self.confirm_order_tab.click_submit_order()
        self.page.wait_for_selector(".loader", state="hidden", timeout=30000)
        return self

    def get_order_status(self) -> str:
        # use regular expression to match any text
        order_status = self.page.locator(".alert strong").first
        expect(order_status).to_contain_text(re.compile(r".+"))
        return order_status.inner_text()

    def get_order_number(self) -> str:
        order_number = self.page.locator(".alert strong").nth(1)
        expect(order_number).to_contain_text(re.compile(r".+"))
        return order_number.inner_text()
