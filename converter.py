import re
import file
from file=php.php import *

php_flags_dict = {
    "i": re.IGNORECASE,
    "u": re.UNICODE,
    "m": re.MULTILINE,
    "s": re.DOTALL,
    "x": re.VERBOSE
}


def php_regex_parser(r, return_compiled=False):
    def parse_flags(php_flags):
        ret = 0
        for c in php_flags:
            if c in php_flags_dict:
                ret |= php_flags_dict[c]
        return ret

    reg = r[1:r.rfind(r[0])]
    f = r[r.rfind(r[0])+1:]
    if 'U' in f:
        reg = re.sub(r'([^\\(])([\?\*\+])', r'\1\2?', reg)
    if 'A' in f and not reg.startswith('^'):
        reg = '^' + reg
    flags = parse_flags(f)
    if return_compiled:
        return re.compile(reg, flags)
    return reg, flags
