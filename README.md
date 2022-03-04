# WWSHC
This is an unofficial module to control WWS (https://wwschool.de; Also other Services using WebWeaver Software) via python code.

## PIP
*Install 0.0.11 via pip: `pip install wwshc==0.0.11`
* Or see at [PyPi.org](https://pypi.org/project/wwshc/0.0.11/)

## Changelog
### Incoming Changes in 0.0.12
* Adding Cache (`wwshc.wwsopt.Cache`; later `.utils.caching.Cache` or easily `.Cache`)
* Continued updating syntax of selenium find_element functions
* Implemented more annotations
* Changed namespace-structures
* Use `wwshc` or `wwshc.references` to get all interesting classes (`.Agent` is now at `._agent.Agent`)
* Changed settings-file format from pydatfile to json (use keys "url", "user", "pass", "wait" in your file and pass the path to "file"-argument)
* Updated selenium to 4.1.2
* Removed `.utils.extra.Filter` (earlier `.wwsopt.Filter`)
* Changed acting's `_ignore: bool` to `__ACTING__: str`
* Changed Caches's `__EXTRA__: str` to `__CACHE__: str`
* Use `**NOACT`, `**SKIP` and `**RESET` instead of `__ACTING__=="DISABLED"`, `__CACHE__="__SKIP__"` or `__CACHE__=="__RESET__"`
* _Other things I have not planned yet._

### Changes in 0.0.11:
* Added eventsystem (`wws.events`)
* Updated selenium to 4.1.0
* Started updating syntax of selenium find_element functions
* Corrected some IDs that have changed in WWS

## Code Examples
### Login
To login, just create a Agent-object
```
import wwshc

wws = wwshc.Agent("https://wwschool.de", "username", "password")
```
### Messaging
To send yourself a message, use `Agent.users_getByMail()` and then `User.quick_send()`.
```
you = wws.users_getByMail(wws.USER)   # Get User by your own mail adress (mathes wws.USER)
you.send_quick("Hello!")              # Sending a Quickmessage with the text "hi"
```
### Events
If you want to make automated answers, you can use this code:
```
import wwshc

wws = wwshc.Agent("https://wwschool.de", "username", "password")     # Creating the Agent

def answer(text, name, mail, send_time):
    if mail != wws.USER:                    # Ignore messages from yourself to prevent endless loops
        user = wws.users_getByMail(mail)    # Getting User-object of sender
        user.quick_send("This is an automated answer by wwshc (https://wwshc.jojojux.de/")     # Sending Quickmessage

if __name__ == "__main__":
    wws.eventloop()                                   # Runs threaded -> You can execute more code below
    wws.events.on_event("quick_received", answer)     # Setting the function as event listener
```
### More
To see more code examples, see [here](https://github.com/J0J0HA/wwshc/tree/master/examples).
