class config:
    SECRET_KEY='HHSjbuf44'


class develomentconf(config):
    DEBUG = True


config = {'develoment': develomentconf()}
