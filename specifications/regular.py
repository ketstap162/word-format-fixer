import re
from typing import Iterable

from settrings import RG_TARGETS


def is_valid_regex(regex_string):
    try:
        re.compile(regex_string)
        return True
    except re.error:
        return False


class RegexChecker:
    def __init__(self, target: str | Iterable, pattern: str, fault_text: str):
        if type(target) is "str":
            if target not in RG_TARGETS:
                raise ValueError(f"Target {target} is not supported")
        else:
            for trg in target:
                if trg not in RG_TARGETS:
                    raise ValueError(f"Target {target} is not supported")

        if not is_valid_regex(pattern):
            raise ValueError(f"The pattern {pattern} is not regular string")

        self.target = target
        self.pattern = pattern
        self.fault_text = fault_text

    def check(self, target, text) -> bool:
        if self.target != target:
            return True

        if re.match(self.pattern, text, re.MULTILINE):
            return True

        return False

    def catch(self, target, text) -> str | None:
        if not self.check(target, text):
            return self.fault_text
