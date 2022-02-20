import json
import threading
from typing import *
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import win10toast
import time
import wwshc.wwsels
import wwshc.wwsopt
import wwshc.wwsevent
from wwshc.wwsopt import _acting
import pyderman
import wwshc.wwserr
from selenium.webdriver.common.by import By


def ensure_chromedriver():
    pyderman.install(pyderman.chrome, file_directory=".", filename="chromedriver.exe")


class Agent:
    def __init__(self: ClassVar, url: str = "", user: str = "", passwd: str = "", hide: bool = True, wait: [float, int] = 0.5, no_notification: bool = False, file = None):
        """
        THIS PROJECT WAS CREATED BY A STUDENT. THERE ARE MANY FUNCTIONS THAT ONLY ADMINS HAVE OR THAT HAVE NOT BEEN RELEASED TO ME. THESE ARE NOT INCLUDED.
        :param url: URL of your wws-System.
        :param user: E-Mail of your WebWeaverSchool-Account (Normally name@schoolname.wwsurl.topleveldomain)
        :param passwd: Password of your WebWeaverSchool-Account
        :param hide: True if you don't want
        :param wait: Time the System waits for API-Requests/Page-Builings before starting to act after page-load.
        :param no_notification: Set true if you don't want do see a success notification
        :param file: If set all other params are ignored. Sets the settings in a file
        """
        ensure_chromedriver()   # Ensure the newest chromedriver is installed.
        if file is not None:
            f = json.load(file)
            self.URL = f["url"]
            self.USER = f["user"]
            self.PASS = f["passwd"]
            self.maw = f["wait"]
        else:
            self.URL = url
            self.USER = user
            self.PASS = passwd
            self.maw = wait
        self.holdOn = False
        self.genwins = []
        self.parent = self
        self.foundwins = []
        self.quicks = []
        self.acting = True
        opts = webdriver.ChromeOptions()
        opts.headless = hide
        self.driver = webdriver.Chrome('./chromedriver.exe', options=opts)
        self.driver.set_window_size(1500, 1000)
        self._nav("/wws/100001.php")
        self.driver.find_element(by=By.CSS_SELECTOR, value="a.language_selection_current_link").click()
        for lang in self.driver.find_elements(by=By.CSS_SELECTOR, value="a.language_selection_option_link"):
            if lang.text == "Deutsch":
                lang.click()
                break
        self.mainwin = self.driver.current_window_handle
        time.sleep(self.maw)
        self.events = wwsevent.Events()
        if not no_notification:
            win10toast.ToastNotifier().show_toast("WWSHC", "WebWeaverSchoolHackClient-Agent erfolgreich gestartet.", threaded=True)
        self.acting = False

    def hold(self: ClassVar, autostop: bool = True):
        """
        Hold the window opened (useless if headless)
        :param autostop: Atomatticcally stop holding if the window is closed.
        """
        self.holdOn = True
        while self.holdOn:
            time.sleep(self.maw)
            if autostop:
                try:
                    if len(self.driver.window_handles) == 0:
                       break
                    else:
                        pass
                except selenium.common.exceptions.InvalidSessionIdException:
                    break
                except selenium.common.exceptions.WebDriverException:
                    break

    @_acting()
    def quit(self: ClassVar) -> bool:
        """
        Close the Window
        :return: Success
        """
        try:
            self.driver.quit()
            return True
        except selenium.common.exceptions.InvalidSessionIdException:
            return False
        except selenium.common.exceptions.WebDriverException:
            return False

    def _navto(self: ClassVar):
        """
        Navigate to the web-page of this element
        """
        self.check()
        self.driver.find_element(by=By.ID, value="top_chapter_first").click()

    def _nav(self, suburl: str):
        """
        Navigate to the given url.
        :param suburl: URL to navigate to.
        """
        self.driver.get(self.URL+suburl)
        self.check()

    def check(self: ClassVar):
        """
        Checks if a login is needed and logs in.
        """
        try:
            time.sleep(self.maw)
            self.driver.find_element(by=By.CSS_SELECTOR, value='[html_title="Einloggen"').click()
            self.driver.find_element(by=By.ID, value="login_login").send_keys(self.USER)
            self.driver.find_element(by=By.ID, value="login_password").send_keys(self.PASS)
            self.driver.find_element(by=By.NAME, value="login_submit").click()
        except selenium.common.exceptions.NoSuchElementException:
            pass

    @_acting()
    def class_list(self: ClassVar) -> List[wwshc.wwsels.Class]:
        """
        Use this to list all Classes are available for you
        :return: List
        """
        self.check()
        clss = []
        for c in Select(self.driver.find_element(by=By.CSS_SELECTOR, value='[html_title="Meine Klassen"]')).options:
            if c.text != "Meine Klassen" and c.text != "--------------------------------------":
                clss.append(wwshc.wwsels.Class(c.text, self))
        return clss

    @_acting()
    def class_get(self, name: str) -> wwshc.wwsels.Class:
        """
        Use this to get a Class available for you
        :raise wwshc.err.NoSuchClass: If the Class is not available for you or is not existing
        :param name: Name of the Class you want to have
        :return: The Class you requested
        """
        self.check()
        for c in self.class_list():
            if c.name == name:
                self.parent.acting = False
                return c
        raise wwshc.wwserr.NoSuchClass(f"No class with name '{name}' found.")

    @_acting()
    def groups_list(self: ClassVar) -> List[wwshc.wwsels.Group]:
        """
        Use this to list all Groups are available for you
        :return: List of all Groups
        """
        self.check()
        grps = []
        for g in Select(self.driver.find_element(by=By.CSS_SELECTOR, value='[html_title="Meine Gruppen"')).options:
            if g.text != "Meine Gruppen" and g.text != "Gruppenübersicht" and g.text != "--------------------------------------":
                grps.append(wwshc.wwsels.Group(g.text, self))
        return grps

    @_acting()
    def groups_get(self, name: str):
        """
        Use this to get a Group avalible for you
        :raise wwshc.err.NoSuchGroup: If the Group is not avalible for you or is not existing

        :param name: Name of the Group you want to have
        :return: The Group you requested
        """
        self.check()
        for g in self.groups_list():
            if g.name == name:
                self.parent.acting = False
                return g
        raise wwshc.wwserr.NoSuchGroup(f"No group with name '{name}' found.")

    def users_list(self, only_online=False, stop_name="", stop_mail=""):
        """
        Use this to list all Users in Contacts

        :param only_online: If you want to list ony people are online.
        :return: List of all Users in Contacts
        """
        self._navto()
        self.driver.find_element(by=By.ID, value="menu_105492").find_element(by=By.TAG_NAME, value="a").click()
        res = []
        if not only_online:
            self.driver.find_element(by=By.LINK_TEXT, value="Alle Mitglieder anzeigen").click()
        for u in self.driver.find_element(by=By.CLASS_NAME, value="table_list").find_element(
                by=By.TAG_NAME, value="tbody").find_elements(by=By.TAG_NAME, value="tr"):
            if not u.text == "":
                res.append(wwshc.wwsels.User(u.find_elements(by=By.TAG_NAME, value="td")[3].text,
                                             u.find_elements(by=By.TAG_NAME, value="td")[4].text, self, self))
            if u.text == stop_name:
                return res
        return res

    @_acting()
    def users_add(self, name_or_mail):
        try:
            self._navto()
            self.driver.find_element(by=By.ID, value="menu_105492").find_element(by=By.TAG_NAME, value="a").click()
            self.driver.find_element(by=By.LINK_TEXT, value="Mitglied aufnehmen").click()
            time.sleep(self.maw)
            wwshc.wwsopt.use_popup(self)
            self.driver.find_element(by=By.NAME, value="add_member").send_keys(name_or_mail)
            try:
                self.driver.find_element(by=By.CLASS_NAME, value="submit").click()
                self.driver.find_element(by=By.CLASS_NAME, value="submit").click()
            except selenium.common.exceptions.NoSuchElementException:
                raise wwshc.wwserr.AlreadyInContacts("This User is already in your contact list")
            time.sleep(self.maw)
            wwshc.wwsopt.use_main(self)
        except selenium.common.exceptions.UnexpectedAlertPresentException as e:
            if e.alert_text == "Kein gültiger Nutzer":
                raise wwshc.wwserr.NoSuchUser(f"The User {name_or_mail} is not existing.")
            else:
                print(e.alert_text)

    @_acting()
    def users_remove(self, name_or_mail):
        self._navto()
        self.driver.find_element(by=By.ID, value="menu_105492").find_element(by=By.TAG_NAME, value="a").click()
        print(self.driver.find_element(by=By.CLASS_NAME, value="jail_table").find_element(by=By.TAG_NAME, value="tbody")
              .find_element(by=By.XPATH, value=f"//*[contains(text(),'{name_or_mail}')]"))
        self.driver.find_element(by=By.CLASS_NAME, value="jail_table").find_element(by=By.TAG_NAME, value="tbody")\
            .find_element(by=By.XPATH, value=f"//*[contains(text(),'{name_or_mail}')]")\
            .find_element(by=By.XPATH, value="..").find_element(by=By.CSS_SELECTOR, value=".icons")\
            .find_element(by=By.CSS_SELECTOR, value='[html_title="Weitere Funktionen"]').click()
        time.sleep(self.maw)
        self.driver.find_element(by=By.CLASS_NAME, value="jail_table").find_element(by=By.TAG_NAME, value="tbody")\
            .find_element(by=By.XPATH, value=f"//*[contains(text(),'{name_or_mail}')]")\
            .find_element(by=By.XPATH, value="..").find_element(by=By.CSS_SELECTOR, value=".icons")\
            .find_element(by=By.XPATH, value=f"//*[contains(text(),'Löschen')]").click()
        self.driver.switch_to.alert()
        self.driver.close()
        self.driver.switch_to.active_element()

    def users_getByName(self, name: str):
        """
        Use this to get a User in Contacts by his Name
        :raise wwshc.err.NoSuchUser: If the User cannot be found by your search arguments

        :param name: Name of the User you are requesting.
        :return: The User you Requested
        """
        for u in self.users_list(stop_name=name):
            if u.name == name:
                return u
        raise wwshc.wwserr.NoSuchUser(f"No user with name '{name}' found.")

    def users_getByMail(self, mail: str):
        """
        Use this to get a User in Contacts by his E-Mail
        :raise wwshc.err.NoSuchUser: If the User cannot be found by your search arguments

        :param mail: E-Mail of the User you are requesting.
        :return: The User you Requested
        """
        for u in self.users_list(stop_mail=mail):
            if u.mail == mail:
                return u
        raise wwshc.wwserr.NoSuchUser(f"No user with mail '{mail}' found.")

    @_acting()
    def files_uploadFile(self, filepath):
        self.driver.find_element(by=By.ID, value="menu_121332").find_element(by=By.TAG_NAME, value="a").click()
        self.driver.find_element(by=By.LINK_TEXT, value="Neue Datei ablegen").click()
        time.sleep(self.maw)
        wwshc.wwsopt.use_popup(self)
        self.driver.find_element(by=By.NAME, value="file[]").send_keys(filepath)
        self.driver.find_element(by=By.CLASS_NAME, value="submit").click()
        wwshc.wwsopt.use_main(self)

    def files_addFile(self, filepath):
        raise NotImplementedError("Cannot add a file.")

    def files_removeFile(self, path):
        raise NotImplementedError("Cannot remove a file.")

    @_acting()
    def files_addFolder(self, name, description=""):
        self.driver.find_element(by=By.ID, value="menu_121332").find_element(by=By.TAG_NAME, value="a").click()
        self.driver.find_element(by=By.LINK_TEXT, value="Ordner anlegen").click()
        time.sleep(self.maw)
        wwshc.wwsopt.use_popup(self)
        self.driver.find_element(by=By.NAME, value="folder").send_keys(name)
        self.driver.find_element(by=By.NAME, value="description").send_keys(description)
        self.driver.find_element(by=By.CLASS_NAME, value="submit").click()
        wwshc.wwsopt.use_main(self)

    def files_removeFolder(self, path):
        """
        *** UNDOCUMENTATED ***
        """
        raise NotImplementedError("Cannot remove a folder.")

    @_acting()
    def tasks_list(self):
        self._navto()
        res = []
        self.driver.find_element(by=By.ID, value="menu_105500").find_element(by=By.TAG_NAME, value="a").click()
        for element in self.driver.find_element(by=By.CLASS_NAME, value="jail_table")\
                .find_element(by=By.TAG_NAME, value="tbody").find_elements(by=By.TAG_NAME, value="tr"):
            res.append(wwshc.wwsels.Task(element.find_element(by=By.CLASS_NAME, value="c_title").text,
                       element.find_element(by=By.CLASS_NAME, value="c_source").text, element.get_property("sort") == "2", self, self))
        return res

    def tasks_get(self, filter: wwshc.wwsopt.Filter):
        return filter.filter(self.tasks_list())[0]

    def eventloop(self) -> None:
        return threading.Thread(target=self._eventloop, daemon=True).start()

    def _eventloop(self):
        self.events.on_event("new_window", self._handler_new_window)
        last_window = self.driver.current_window_handle
        last_url = self.driver.current_url
        last_title = self.driver.title
        while True:
            time.sleep(self.maw)
            # Window Changed
            if (self.driver.current_window_handle, self.driver.title, self.driver.current_url,) != (last_window, last_title, last_url,):
                last_window = self.driver.current_window_handle
                last_url = self.driver.current_url
                last_title = self.driver.title
                self.events.cause("status_changed", status={"window": self.driver.current_window_handle, "title": self.driver.title, "url": self.driver.current_url})

            # New Windows
            all = self.parent.driver.window_handles
            all.remove(self.parent.mainwin)
            for i in self.parent.genwins:
                try: all.remove(i)
                except: pass
            for i in self.parent.foundwins:
                try: all.remove(i)
                except: pass
            if len(all) > 0 and not self.acting:
                self.acting = True
                new = all.pop()
                self.foundwins.append(new)
                self.driver.switch_to.window(new)
                time.sleep(self.maw)
                self.events.cause("new_window", window=self.driver.current_window_handle, title=self.driver.title, url=self.driver.current_url)
                wwshc.wwsopt.use_main(self)
                self.acting = False

            # Quicks
            if not self.acting and len(self.quicks) > 0:
                self.acting = True
                quick = self.quicks.pop()
                self.driver.switch_to.window(quick["window"])
                time.sleep(self.maw)
                text = self.driver.find_element(by=By.XPATH, value='//*[@id="main_content"]/p').text
                name = self.driver.find_element(by=By.XPATH,
                                                value='//*[@id="main_content"]/table/tbody/tr[1]/td[2]/span').text
                mail = self.driver.find_element(by=By.XPATH,
                                                value='//*[@id="main_content"]/table/tbody/tr[1]/td[2]/span')\
                    .get_attribute("html_title")
                send_time = self.driver.find_element(by=By.XPATH,
                                                     value='//*[@id="main_content"]/table/tbody/tr[2]/td[2]').text
                self.events.cause("quick_received", text=text, name=name, mail=mail, send_time=send_time)
                self.driver.close()
                wwshc.wwsopt.use_main(self)
                self.acting = False

    def _handler_new_window(self, window, title, url):
        if "Quickmessage lesen" in title:
            self.quicks.append({"window": window, "title": title, "url": url})

    def __exit__(self):
        return self.__del__()

    def __del__(self):
        try:
            if len(self.driver.window_handles) != 0:
               self.driver.close()
        except selenium.common.exceptions.InvalidSessionIdException:
            return False
        except selenium.common.exceptions.WebDriverException:
            return False
        return True
