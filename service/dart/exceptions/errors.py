# -*- coding: utf-8 -*-
class APIKeyError(ValueError):
    def __init__(self, msg='Unregistered API Key'):
        super().__init__(msg)


class TemporaryLocked(RuntimeError):
    def __init__(self, msg='Temporarily locked'):
        super().__init__(msg)


class NoDataReceived(ValueError):
    def __init__(self, msg='No data received'):
        super().__init__(msg)


class OverQueryLimit(RuntimeError):
    def __init__(self, msg='Over query limit'):
        super().__init__(msg)


class InvalidField(ValueError):
    def __init__(self, msg='Invalid field'):
        super().__init__(msg)


class ServiceClose(RuntimeError):
    def __init__(self, msg='Open API was closed for web service'):
        super().__init__(msg)


class UnknownError(RuntimeError):
    def __init__(self, msg='Unknown error'):
        super().__init__(msg)


class NotFoundConsolidated(ValueError):
    def __init__(self, err_msg='Could not find consolidated financial statements'):
        super().__init__(err_msg)
