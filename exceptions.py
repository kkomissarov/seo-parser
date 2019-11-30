class MissingRequiredArgumentError(Exception):
    def __init__(self, msg="Вы не указали обязательный аргумент (адрес сайта)"):
        super().__init__(msg)


class TooManyArgumentsError(Exception):
    def __init__(self, msg="Вы передали слишком много аргументов"):
        super().__init__(msg)


class SiteNameError(Exception):
    def __init__(self, msg="Указанное значение не является адресом сайта"):
        super().__init__(msg)
