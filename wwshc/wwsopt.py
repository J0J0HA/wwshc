import time
import selenium.common.exceptions
import wwshc.wwserr
import wwshc.wwsels
import warnings
from selenium.webdriver.common.by import By


def void(*args, **kwargs):
    pass


def filter_userlist(self, only_online: bool, stop_name: str, stop_mail: str):
    res = []
    if not only_online:
        self.driver.find_element(by=By.LINK_TEXT, value="Alle Mitglieder anzeigen").click()
    for u in self.brother.driver.find_element(by=By.ID, value="table_users").find_element(by=By.TAG_NAME, value="tbody")\
            .find_elements(by=By.TAG_NAME, value="tr"):
        if not u.text == "":
            res.append(wwshc.wwsels.User(u.find_element(by=By.CLASS_NAME, value="c_fullname").text,
                                         u.find_element(by=By.CLASS_NAME, value="c_login").text, self, self.brother))
        if u.text == stop_name:
            return res
    return res


def filter_userlist_mail(self, mail: str, only_online: bool):
    if not only_online:
        self.driver.find_element(by=By.LINK_TEXT, value="Alle Mitglieder anzeigen").click()
    time.sleep(self.maw)
    try:
        u = self.brother.driver.find_element(by=By.XPATH, value=f'//*[contains(concat(" ", normalize-space(@class), '
                                                                f'" "), " table_list ")]/tbody/tr/*[contains(text(),'
                                                                f'"{mail}")]/..')
    except selenium.common.exceptions.NoSuchElementException:
        raise wwshc.wwserr.NoSuchUser(f"No user with mail '{mail}' found.")
    return wwshc.wwsels.User(u.find_element(by=By.CLASS_NAME, value="c_fullname").text,
                             u.find_element(by=By.CLASS_NAME, value="c_login").text, self, self.brother)


def filter_userlist_name(self, name: str, only_online: bool):
    if not only_online:
        self.parent.driver.find_element(by=By.LINK_TEXT, value="Alle Mitglieder anzeigen").click()
    time.sleep(self.maw)
    try:
        u = self.parent.driver.find_element(by=By.XPATH, value='//*[contains(concat(" ", normalize-space(@class), '
                                                               '" "), " table_list ")]/tbody/tr/*[contains(text(),'
                                                               '"{name}")]/..')
        print(u.screenshot_as_base64)
    except selenium.common.exceptions.NoSuchElementException:
        raise wwshc.wwserr.NoSuchUser(f"No user with mail '{name}' found.")
    return wwshc.wwsels.User(u.find_element(by=By.CLASS_NAME, value="c_fullname").text,
                             u.find_element(by=By.CLASS_NAME, value="c_login").text, self, self.brother)


def use_popup(self, ignore=[]):
    all = self.brother.driver.window_handles
    all.remove(self.brother.mainwin)
    for i in ignore:
        try: all.remove(i)
        except: pass
    for i in self.parent.genwins:
        try: all.remove(i)
        except: pass
    for i in self.parent.foundwins:
        try: all.remove(i)
        except: pass
    self.driver.switch_to.window(all.pop())


def use_alert(self):
    warnings.warn("Use wws.driver.switch_to.alert() instead.")


def use_main(self):
    self.driver.switch_to.window(self.parent.mainwin)


class Filter:
    def __init__(self, **kwargs):
        self.allowed = kwargs.keys()
        for k in kwargs.keys():
            self.__setattr__(k, kwargs[k])

    def filter(self, list):
        """
        *** UNDOCUMENTATED ***
        """
        filtered_list = list
        for a in self.allowed:
            for e in list:
                if self.__getattribute__(a) == e.__getattribute__(a):
                    filtered_list.remove(e)
        return filtered_list
