from pages.stepper_tabs.base_form_tab import BaseFormTab
from pages.stepper_tabs.confirm_order_tab import ConfirmOrderTab


class PaymentDetailsTab(BaseFormTab):
    """Payment details form tab"""

    def fill_form(self, payment_details: dict[str, str]) -> "PaymentDetailsTab":
        """Fill out the payment details form"""
        return (
            self.fill_card_number(payment_details["card_number"])
            .select_card_type(payment_details["card_type"])
            .fill_name_on_card(payment_details["name_on_card"])
            .fill_expiry_date(payment_details["expiry_date"])
            .fill_cvv(payment_details["cvv"])
        )

    def fill_card_number(self, card_number: str) -> "PaymentDetailsTab":
        self.fill_text_input("creditcardno", card_number)
        return self

    def select_card_type(self, card_type: str) -> "PaymentDetailsTab":
        self.set_select("creditcardtype", card_type)
        return self

    def fill_name_on_card(self, name_on_card: str) -> "PaymentDetailsTab":
        self.fill_text_input("creditcardname", name_on_card)
        return self

    def fill_expiry_date(self, expiry_date: str) -> "PaymentDetailsTab":
        self.fill_text_input("creditcardexpiry", expiry_date)
        return self

    def fill_cvv(self, cvv: str) -> "PaymentDetailsTab":
        self.fill_text_input("creditcardcvv", cvv)
        return self

    def click_next(self) -> "ConfirmOrderTab":
        self.page.get_by_role("button", name="Next").click()
        return ConfirmOrderTab(self.page)
