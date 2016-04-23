import pytest
from page_table import PageTable, Page
from page_table import PageFaultException, PageTableFullException
from access import MemoryAccess


def read_memory_access_factory(address='00000000'):
    return MemoryAccess(address, 'R', 0)


def write_memory_access_factory(address='00000000'):
    return MemoryAccess(address, 'W', 0)


class TestPageTable:

    def test_is_full(self):
        p = PageTable(1)
        assert not p.is_full
        p.table[0] = True
        assert p.is_full

    def test_length(self):
        p = PageTable(1)
        p.table[0] = True
        assert len(p) == 1
        p.table[1] = True
        assert len(p) == 2

    def test_insert_with_no_checks(self):
        p = PageTable(1)
        a = read_memory_access_factory()
        p.insert_no_check(a)
        assert len(p) == 1

    def test_insert_when_already_available(self):
        p = PageTable(2)
        a = read_memory_access_factory()
        p.insert_no_check(a)
        result = p.insert(a)
        assert result
        assert len(p) == 1

    def test_insert_when_not_full(self):
        p = PageTable(2)
        a = read_memory_access_factory()
        p.insert_no_check(a)
        b = read_memory_access_factory('00001000')
        with pytest.raises(PageFaultException) as e:
            p.insert(b)
        assert not isinstance(e, PageTableFullException)
        assert len(p) == 2

    def test_insert_when_full(self):
        p = PageTable(1)
        a = read_memory_access_factory()
        p.insert_no_check(a)
        b = read_memory_access_factory('00001000')
        with pytest.raises(PageTableFullException):
            p.insert(b)
        assert len(p) == 1

    def test_get(self):
        p = PageTable(1)
        a = read_memory_access_factory()
        p.insert_no_check(a)
        val = p.table[0]
        assert p.get(a) is val
        assert p.get(a.page_index) is val

    def skip_free_clean_indecies(self):
        p = PageTable(1)
        a = read_memory_access_factory()
        p.insert_no_check(a)
        assert p.free_indecies(0) == 0
        assert len(p) == 0

    def skip_free_dirty_indecies(self):
        p = PageTable(1)
        a = write_memory_access_factory()
        p.insert_no_check(a)
        assert p.free_indecies(0) == 1
        assert len(p) == 0

    def test_iterable(self):
        p = PageTable(3)
        p.insert_no_check(read_memory_access_factory())
        p.insert_no_check(read_memory_access_factory('00001000'))
        for key, value in p:
            assert isinstance(key, int)
            assert isinstance(value, Page)
