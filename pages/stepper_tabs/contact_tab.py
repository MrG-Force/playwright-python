from pages.stepper_tabs.base_form_tab import BaseFormTab
from pages.stepper_tabs.delivery_tab import DeliveryDetailsTab


class ContactDetailsTab(BaseFormTab):
    """Contact details form tab"""

    def fill_form(self, details: dict[str, str]) -> "ContactDetailsTab":
        """Fill out the contact details form"""
        return (
            self.fill_first_name(details["first_name"])
            .fill_last_name(details["last_name"])
            .fill_email(details["email"])
            .fill_phone_number(details["phone_number"])
            .fill_address_1(details["address_1"])
            .fill_address_2(details["address_2"])
            .fill_suburb(details["suburb"])
            .select_state(details["state"])
            .fill_postcode(details["postcode"])
        )

    def fill_first_name(self, f_name: str) -> "ContactDetailsTab":
        self.fill_text_input("firstName", f_name)
        return self

    def fill_last_name(self, l_name: str) -> "ContactDetailsTab":
        self.fill_text_input("lastName", l_name)
        return self

    def fill_email(self, email: str) -> "ContactDetailsTab":
        self.fill_text_input("email", email)
        return self

    def fill_phone_number(self, phone: str) -> "ContactDetailsTab":
        self.fill_text_input("phonenumber", phone)
        return self

    def fill_address_1(self, address: str) -> "ContactDetailsTab":
        self.fill_text_input("addressline1", address)
        return self

    def fill_address_2(self, address: str) -> "ContactDetailsTab":
        self.fill_text_input("addressline2", address)
        return self

    def fill_suburb(self, suburb: str) -> "ContactDetailsTab":
        self.fill_text_input("suburb", suburb)
        return self

    def select_state(self, state: str) -> "ContactDetailsTab":
        self.set_select("state", state)
        return self

    def fill_postcode(self, postcode: str) -> "ContactDetailsTab":
        self.fill_text_input("postcode", postcode)
        return self

    def click_next(self) -> "DeliveryDetailsTab":
        self.page.get_by_role("button", name="Next").click()
        return DeliveryDetailsTab(self.page)
