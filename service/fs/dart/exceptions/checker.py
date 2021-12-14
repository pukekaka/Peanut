# -*- coding: utf-8 -*-
from service.fs.dart.exceptions.errors import (APIKeyError, TemporaryLocked, NoDataReceived, OverQueryLimit, InvalidField, ServiceClose, UnknownError)


def check_error(status):
    errors = {
        '000': None,
        '010': APIKeyError,
        '011': TemporaryLocked,
        '013': NoDataReceived,
        '020': OverQueryLimit,
        '100': InvalidField,
        '800': ServiceClose,
        '900': UnknownError,
    }
    return errors.get(status, UnknownError)


def check_status(**kwargs):
    status = kwargs.get('status')
    err = check_error(status)
    if err is not None:
        msg = kwargs.get('message')
        raise err(msg)
