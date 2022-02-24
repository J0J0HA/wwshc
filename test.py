import wwshc
from wwshc.wwsopt import Cache

with open(r"user.txt", "r") as usernm:
    with open(r"pass.txt", "r") as passwd:
        wws = wwshc.Agent("https://wwschool.de", usernm.read(), passwd.read(), no_notification=True, hide=False)


wws.eventloop()
print(wws.class_list())
print(wws.class_get("08A").users_list())
print(wws.class_list())
print(wws.class_get("08A").users_list())
