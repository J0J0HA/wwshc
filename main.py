import wwshc

with open("pass.txt", "r") as passwd:
    with open("user.txt", "r") as user:
        wws = wwshc.Agent("https://wwschool.de", user.readline(), passwd.readline(), hide=False)


@wws.events.on("new_window")
def new_win(**kwargs):
    print("new_window", kwargs)


@wws.events.on("status_changed")
def status_changed(**kwargs):
    print("status_changed", kwargs)


@wws.events.on("quick_received")
def quick_received(**kwargs):
    print("quick_received", kwargs)
    print(wws.USER.split("@")[0])
    if kwargs["name"] == wws.USER.split("@")[0]:
        wws.users_getByName(kwargs["name"]).quick_send("+++ Automatische Antwort +++<br>Test für Automatische Antworten!<br>Diese Nachricht wurde von wwshc gesendet. (pypi.org/project/wwshc)<br>+++Automatische Antwort +++")


if __name__ == '__main__':
    wws.eventloop()
    wws.events.on_event("new_window", new_win)
    wws.events.on_event("status_changed", status_changed)
    wws.events.on_event("quick_received", quick_received)
    wws.users_getByName("johannes.hartel").quick_send("Test")
    wws.hold()
