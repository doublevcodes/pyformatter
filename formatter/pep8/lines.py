from typing import Optional


class LineChecker:

    def __init__(self, line: str) -> None:
        self.line = line.strip()

    def _check_line(self) -> tuple[bool, Optional[int]]:
        if line_length := len(self.line) >= 88:
            return (False, line_length)
        else:
            return (True, None)

    @classmethod
    def check(cls, line: str) -> tuple[bool, Optional[int]]:
        checker = cls(line)
        status, length = checker._check_line()
        if status:
            return status
        else:
            return (status, length)


