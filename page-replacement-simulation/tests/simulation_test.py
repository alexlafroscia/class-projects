from simulation import Simulation
from page_table import PageFaultException, PageTableFullException
from access import MemoryAccess


def stub_empty_method(self, *args, **kwargs):
    pass


class TestSimulation:

    def test_it_initializes_page_table_correctly(self):
        Simulation._load_memory_accesses_from_file = stub_empty_method
        Simulation._load_replacement_algorithm = stub_empty_method
        s = Simulation('dummy path', 'dummy alg', 4, 4, 4)
        assert s.page_table.size == 4

    def test_handling_page_fault(self):
        Simulation._load_memory_accesses_from_file = stub_empty_method
        Simulation._load_replacement_algorithm = stub_empty_method
        s = Simulation('dummy path', 'dummy alg', 4, 4, 4)
        a = MemoryAccess('00000000', 'R', 0)
        e = PageFaultException()
        s._handle_page_fault(e, a)
        assert s.page_fault_counter == 1

    def skip_test_handling_page_table_full(self):
        Simulation._load_memory_accesses_from_file = stub_empty_method
        Simulation._load_replacement_algorithm = stub_empty_method
        s = Simulation('dummy path', 'dummy alg', 4)
        a = MemoryAccess('00000000', 'R', 0)
        e = PageTableFullException()
        s._handle_page_fault(e, a)
        assert s.page_fault_counter == 1
