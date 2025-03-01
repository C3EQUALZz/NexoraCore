from sqlalchemy import TypeDecorator, String

# TODO: WRITE ALL TYPED DECORATORS FOR ALCHEMY
class PhoneDecorator(TypeDecorator):
    impl = String
    cache_ok = True

