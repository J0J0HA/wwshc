## Changelog
### Update 0.0.12 (beta; usable; incomplete)
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

### Update 0.0.11 (beta; usable; incomplete)
* Added eventsystem (`wws.events`)
* Updated selenium to 4.1.0
* Started updating syntax of selenium find_element functions
* Corrected some IDs that have changed in WWS
