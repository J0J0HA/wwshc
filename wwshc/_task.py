import time
from selenium.webdriver.common.by import By
from . import utils


class Task:
    def __init__(self, title: str, source: str, done: bool, found_by, wws):
        self.parent = wws
        self.driver = wws.driver
        self.brother = found_by
        self.done = not done
        self.made_by = source
        self.title = title

    def reload(self):
        self.brother._navto()
        utils.extra.void(self.brother.tasks_list())

    def toggle_done(self):
        time.sleep(self.parent.maw)
        while self.parent.acting:
            time.sleep(self.parent.maw)
        self.parent.acting = True
        self.reload()
        for element in self.driver.find_element_by_class_name("jail_table").find_element_by_tag_name(
                "tbody").find_elements_by_tag_name("tr"):
            if self.title == element.find_element_by_class_name("c_title").text:
                element.find_element_by_class_name("c_state").find_element_by_tag_name("img").click()
                time.sleep(self.parent.maw)
                utils.extra.use_popup(self)
                self.driver.find_element_by_id("id_419089_1").click()
                utils.extra.use_main(self)
                time.sleep(self.parent.maw)
                break
        self.parent.acting = False

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"Task(title={repr(self.title)}, author={repr(self.made_by)}, done={repr(self.done)}, parent={repr(self.parent)})"
