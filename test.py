import wwshc

with open("user.txt") as usernm:
    with open("pass.txt") as passwd:
        wws = wwshc.Agent("https://wwschool.de", usernm.read(), passwd.read(), False)

def test(): pass
print(test.__class__)
print(wws.class_list())
