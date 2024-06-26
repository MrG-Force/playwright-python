from pages.stepper_tabs.base_form_tab import BaseFormTab
from pages.stepper_tabs.payment_tab import PaymentDetailsTab


class DeliveryDetailsTab(BaseFormTab):
    """Delivery details form tab"""

    def fill_form(
        self, same_as_contact: bool = False, details: dict[str, str] = None
    ) -> "DeliveryDetailsTab":

        if same_as_contact:
            self.page.get_by_text("Yes").click()
            return self
        else:
            return (
                self.fill_name(details["full_name"])
                .fill_address_1(details["address_1"])
                .fill_address_2(details["address_2"])
                .fill_suburb(details["suburb"])
                .select_state(details["state"])
                .fill_postcode(details["postcode"])
            )

    def fill_name(self, name: str) -> "DeliveryDetailsTab":
        self.fill_text_input("name", name)
        return self

    def fill_address_1(self, address: str) -> "DeliveryDetailsTab":
        self.fill_text_input("addressline1", address)
        return self

    def fill_address_2(self, address: str) -> "DeliveryDetailsTab":
        self.fill_text_input("addressline2", address)
        return self

    def fill_suburb(self, suburb: str) -> "DeliveryDetailsTab":
        self.fill_text_input("suburb", suburb)
        return self

    def select_state(self, state: str) -> "DeliveryDetailsTab":
        self.set_select("state", state)
        return self

    def fill_postcode(self, postcode: str) -> "DeliveryDetailsTab":
        self.fill_text_input("postcode", postcode)
        return self

    def click_next(self) -> "PaymentDetailsTab":
        self.page.get_by_role("button", name="Next").click()
        return PaymentDetailsTab(self.page)
