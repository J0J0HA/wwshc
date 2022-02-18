class WWSHCError(BaseException): pass
class WWSHCNotExistingError(WWSHCError): pass
class NoSuchGroup(WWSHCNotExistingError): pass
class NoSuchClass(WWSHCNotExistingError): pass
class NoSuchUser(WWSHCNotExistingError): pass
class AlreadyInContacts(WWSHCError): pass
