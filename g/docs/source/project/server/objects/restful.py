import collections

from project.server.objects.pagination import Pagination


class Restful:
    def __init__(self):
        self.fields = []
        self.filters = {}
        self.order_by = collections.OrderedDict()
        self.pagination = Pagination()
        self.q = None
