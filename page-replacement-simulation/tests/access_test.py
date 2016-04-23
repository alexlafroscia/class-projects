from access import MemoryAccess


class TestMemoryAccess:

    def test_read_property(self):
        r = MemoryAccess('00000000', 'R', 0)
        assert r.read
        assert not r.write

    def test_write_property(self):
        w = MemoryAccess('00000000', 'W', 0)
        assert not w.read
        assert w.write

    def test_page_index(self):
        r = MemoryAccess('00001000', 'R', 0)
        w = MemoryAccess('00002000', 'W', 0)
        p = MemoryAccess('00001001', 'R', 0)
        assert r.page_index == 1
        assert w.page_index == 2
        assert r.page_index == p.page_index

    def test_save_access_index(self):
        r = MemoryAccess('00000000', 'R', 1)
        assert r.index == 1
