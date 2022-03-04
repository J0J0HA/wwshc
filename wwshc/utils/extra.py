import random
import time
import selenium.common.exceptions
from .. import utils
from .. import references
from typing import *
from selenium.webdriver.common.by import By
import pyderman


def ensure_chromedriver():
    pyderman.install(pyderman.chrome, file_directory=".", filename="chromedriver.exe")


def void(*args, **kwargs):
    pass


def acting(*vargs: Tuple[Any], **vkwargs: Dict[Any, Any]) -> Callable:
    void(*vargs, **vkwargs)

    def worker(func: Callable) -> Callable:
        def wrapper(*args: Tuple[Any], **kwargs: Dict[str, Any]) -> Any:
            print("got request", func.__name__)
            if "__ACTING__" in kwargs and kwargs["__ACTING__"] == "__DISABLE__":
                kwargs.pop("__ACTING__")
                return func(*args, **kwargs)
            else:
                time.sleep(random.random())
                while args[0].parent.acting:
                    print(func.__name__, "is waiting!", repr((args, kwargs, )), args[0].parent.acting)
                    time.sleep(args[0].maw)
                args[0].parent.acting = True
                r = func(*args, **kwargs)
                args[0].parent.acting = False
            return r
        return wrapper
    return worker


def filter_userlist(self, only_online: bool, stop_name: str, stop_mail: str):
    res = []
    if not only_online:
        self.driver.find_element(by=By.LINK_TEXT, value="Alle Mitglieder anzeigen").click()
    for u in self.brother.driver.find_element(by=By.ID, value="table_users").find_element(by=By.TAG_NAME, value="tbody")\
            .find_elements(by=By.TAG_NAME, value="tr"):
        if not u.text == "":
            res.append(references.User(u.find_element(by=By.CLASS_NAME, value="c_fullname").text,
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
        raise utils.exceptions.NoSuchUser(f"No user with mail '{mail}' found.")
    return references.User(u.find_element(by=By.CLASS_NAME, value="c_fullname").text,
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
        raise utils.exceptions.NoSuchUser(f"No user with mail '{name}' found.")
    return references.User(u.find_element(by=By.CLASS_NAME, value="c_fullname").text,
                             u.find_element(by=By.CLASS_NAME, value="c_login").text, self, self.brother)


def use_popup(self, ignore: Optional[List[str]] = None):
    if not ignore:
        ignore = []

    handles = self.brother.driver.window_handles
    handles.remove(self.brother.mainwin)
    for i in ignore:
        try: handles.remove(i)
        except: pass
    for i in self.parent.genwins:
        try: handles.remove(i)
        except: pass
    for i in self.parent.foundwins:
        try: handles.remove(i)
        except: pass
    self.driver.switch_to.window(handles.pop())


def use_main(self):
    self.driver.switch_to.window(self.parent.mainwin)
