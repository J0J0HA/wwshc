from . import utils
from typing import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

class Group:
    def __init__(self, name: str, wws):
        """
        :param name: Of the Group
        :param wws: The brother Agent
        """
        self.name = name
        self.parent = wws
        self.maw = wws.maw
        self.driver = wws.driver

    def _navto(self):
        """
        Navigate to the web-page of this element
        """
        self.parent._navto()
        Select(self.driver.find_element_by_id("top_select_18")).select_by_visible_text(self.name)

    @utils.extra.acting()
    @utils.extra.cache.cached()
    def users_list(self, only_online=False, stop_name="", stop_mail=""):
        """
        Use this to list all Users of this Group

        :param only_online: If you want to list ony people are online.
        :return: List of all Users of this Group
        """
        self._navto()
        self.driver.find_element_by_id("menu_109756").find_element_by_tag_name("a").click()
        res = utils.extra.filter_userlist(self, only_online, stop_name, stop_mail)
        return res

    @utils.extra.acting()
    @utils.extra.cache.cached()
    def users_getByName(self, name: str, only_online=False):
        """
        Use this to get a User of this Group by his Name
        :raise wwshc.err.NoSuchUser: If the User cannot be found by your search arguments

        :param name: Name of the User you are requesting.
        :return: The User you Requested
        """
        self._navto()
        self.driver.find_element_by_id("menu_109756").find_element_by_tag_name("a").click()
        res = utils.extra.filter_userlist_name(self, name, only_online)
        return res

    @utils.extra.acting()
    @utils.extra.cache.cached()
    def users_getByMail(self, mail: str, only_online=False):
        """
        Use this to get a User of this Group by his E-Mail
        :raise wwshc.err.NoSuchUser: If the User cannot be found by your search arguments

        :param mail: E-Mail of the User you are requesting.
        :return: The User you Requested
        """
        self._navto()
        self.driver.find_element_by_id("menu_109756").find_element_by_tag_name("a").click()
        res = utils.extra.filter_userlist_mail(self, mail, only_online)
        return res

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"Group(name={repr(self.name)}, parent={repr(self.parent)})"

