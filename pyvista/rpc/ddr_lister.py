# coding=utf-8
__author__ = 'Joe'

from .rpc import Rpc, RpcParameter
from .utils import *


class DdrLister(object):

    def __init__(self):
        self.file = None
        self._iens = None
        self._fields = '@'
        self._flags = 'IP'
        self.number = None
        self.frum = None
        self.part = None
        self._index = '#'
        self.screen = None
        self.identifier = None
        self.rpc = None
        self.response = None
        self.fieldnames = None

    @property
    def iens(self):
        return self._iens

    @iens.setter
    def iens(self, value):
        if not value:
            return
        if value[0] != ',':
            value = ',' + value
        if value[-1] != ',':
            value += ','
        parts = value[1:-1].split(',', -1)
        for part in parts:
            if not part.isdigit():
                raise RpcException('Invalid IENS')
        self._iens = value

    @property
    def fields(self):
        return self._fields

    @fields.setter
    def fields(self, value):
        if len(value):
            self._fields = value if value.find('@') != -1 else '@;' + value

    @property
    def flags(self):
        return self._flags

    @flags.setter
    def flags(self, value):
        if not value:
            value = 'IP'
        if value.find('P') == -1:
            raise RpcException('Current version does packed queries only')
        self._flags = value

    def find(self, cxn):
        self._prepare()
        if type(cxn) is str:
            self.records = self.load_from_file(cxn)
        else:
            self.response = cxn.execute(self.rpc)
            self._load(self.response)
        return self.records

    def _prepare(self):
        self._prepare_param_list()
        params = RpcParameter(RpcParameter.LIST, self.param_list)
        self.rpc = Rpc.create('DDR LISTER', [params])

    def _prepare_param_list(self):
        if not getattr(self, 'file', None):
            raise RpcException('VistaSelect must specify a file')
        self.param_list = [('"FILE"', self.file)]

        if getattr(self, 'iens', None):
            self.param_list += [('"IENS"', self.iens)]

        self.param_list += [('"FIELDS"', getattr(self, 'fields', '@'))]

        self.param_list += [('"FLAGS"', getattr(self, 'flags', 'IP'))]

        if getattr(self, 'number', None):
            self.param_list += [('"MAX"', str(self.number))]

        if getattr(self, 'frum', None):
            self.param_list += [('"FROM"', adjust_for_search(self.frum))]

        if getattr(self, 'part', None):
            self.param_list += [('"PART"', self.part)]

        self.param_list += [('"XREF"', getattr(self, 'index', '#'))]

        if getattr(self, 'screen', None):
            self.param_list += [('"SCREEN"', self.screen)]

        if getattr(self, 'identifier', None):
            self.param_list += [('"ID"', self.identifier)]

        return self.param_list

    def _load(self, response):
        lines = response.split("\r\n")
        numlines = len(lines)

        # Find starting line...
        linenum = 0
        while linenum < numlines and lines[linenum] != '[BEGIN_diDATA]':
            linenum += 1
        if linenum == numlines:
            raise RpcException('Empty response')
        linenum += 1

        self.records = []

        # Might need to check that last line is '[END_diDATA]' but assume it
        # for now...
        while linenum < numlines - 1 and not lines[linenum].startswith('[END_diDATA]'):
            self.records.append(lines[linenum].split('^'))
            linenum += 1

        if self.fieldnames:
            named_records = []
            for rec in self.records:
                named_records.append(dict(list(zip(self.fieldnames, rec))))
            self.records = named_records
        return self.records

    def load_from_file(self, filename):
        f = open(filename, 'rb')
        response = f.read()
        f.close()
        return self._load(response.decode())
