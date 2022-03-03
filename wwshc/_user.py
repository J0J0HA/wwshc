import time
from selenium.webdriver.common.by import By
from . import utils


class User:
    def __init__(self, name: str, mail: str, found_by, wws):
        """
        :param name: Name of the User
        :param mail: E-mail of the user
        :param found_by: The Element wich found the User (Agent, Group, Class)
        :param wws: The brother Agent
        """
        self.name = name
        self.mail = mail
        self.brother = found_by
        self.parent = wws
        self.driver = wws.driver
        self.maw = wws.maw

    def _navto(self):
        """
        Navigate to the web-page of this element
        """
        self.brother._navto()
        utils.extra.void(self.brother.users_list(_ignore=True))

    @utils.extra.acting()
    def quick_send(self, text):
        """
        Send a Quickmessage to the User

        :param text: Text of the Message to send
        """
        self._navto()
        time.sleep(self.maw)
        self.driver.find_element_by_xpath(f'//*[contains(concat(" ", normalize-space(@class), " "), " table_list '
                                          f'")]/tbody/tr/*[contains(text(),'
                                          f'"{self.mail}")]/..').find_element_by_css_selector(
            ".icons").find_element_by_css_selector(
            f"img.set0").click()
        time.sleep(self.maw)
        utils.extra.use_popup(self)
        self.driver.switch_to.frame(self.driver.find_element_by_class_name("wysiwyg"))
        self.driver.find_element_by_class_name("wysiwyg").send_keys(text)
        self.driver.switch_to.default_content()
        time.sleep(self.parent.maw)
        self.driver.find_element_by_class_name("submit").click()
        utils.extra.use_main(self)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"User(name={repr(self.name)}, mail={repr(self.mail)}, agent={repr(self.parent)})"

