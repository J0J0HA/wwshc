import time
#import wwshc
from wwshc.wwsopt import Cache

#with open(r"user.txt", "r") as usernm:
#    with open(r"pass.txt", "r") as passwd:
#        wws = wwshc.Agent("https://wwschool.de", usernm.read(), passwd.read(), no_notification=True, hide=False)


#wws.eventloop()
#print(wws.class_list())
#print(wws.class_get("08A").users_list())

cache = Cache()


@cache.cached(True)
def test(tp="no"):
    time.sleep(1)
    return tp


print(test("hi"))
print(test("hi"))
print(test("bye"))
print(test("bye", __EXTRA__="__SKIP__"))
print(test())
print(test())
print(test("hi"))
print(test("hi"))
print(test("bye"))
print(test("bye", __EXTRA__="__RESET__"))
print(test())
print(test())
print(cache.funcs)
