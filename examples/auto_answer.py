import wwshc

wws = wwshc.Agent("https://wwschool.de", "username", "password")     # Creating the Agent

def answer(text, name, mail, send_time):
    if mail != wws.USER:                    # Ignore messages from yourself to prevent endless loops
        user = wws.users_getByMail(mail)    # Getting User-object of sender
        user.quick_send("This is an automated answer by wwshc (https://wwshc.jojojux.de/")     # Sending Quickmessage

if __name__ == "__main__":
    wws.eventloop()                                   # Runs threaded -> You can execute more code below
    wws.events.on_event("quick_received", answer)     # Setting the function as event listener
