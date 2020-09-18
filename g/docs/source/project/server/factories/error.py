import re
import sys

from project.server.helpers import generic_errors


def get_instance(path):
    match = re.compile('/(v\d+)/.*').match(path)
    if match:
        try:
            module = 'project.server.controllers.' + match.group(1)

            __import__(module + '.errors', fromlist=[''])
            return getattr(sys.modules[module], 'errors')
        except (KeyError, AttributeError):
            return generic_errors
    return generic_errors
