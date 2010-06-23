#!/usr/bin/env python

class CodeTalkerException(Exception):
    pass

class ParseError(CodeTalkerException):
    pass

class TokenError(CodeTalkerException):
    pass


# vim: et sw=4 sts=4
