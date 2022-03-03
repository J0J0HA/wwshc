import wwshc
from wwshc import cache

with open(r"user.txt", "r") as usernm:
    with open(r"pass.txt", "r") as passwd:
        wws = wwshc.Agent("https://wwschool.de", usernm.read(), passwd.read(), no_notification=True, hide=True)


print(str(repr(wws)))
wws.eventloop()
print(wws.class_list())
print(wws.class_get("08A").users_list())
print(wws.class_list())
print(wws.class_get("08A").users_list())
print("++++++++")
for c in cache.cache:
    print(c)
