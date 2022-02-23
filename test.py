import wwshc
from typing import *

with open(r"user.txt", "r") as usernm:
    with open(r"pass.txt", "r") as passwd:
        wws = wwshc.Agent("https://wwschool.de", usernm.read(), passwd.read(), no_notification=True)


wws.eventloop()
print(wws.class_list())
