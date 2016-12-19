def singleton(cls):
    def wrapper(*args, **kwargs):
        if not hasattr(cls, '__instance'):
            cls.__instance = cls(*args, **kwargs)
        return cls.__instance

    return wrapper