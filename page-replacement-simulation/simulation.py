# -*- coding: utf-8 -*-

from io import open
from Queue import Queue
from textwrap import dedent
from access import MemoryAccess
from replacement_algorithms import get_replacement_algorithm
from page_table import PageTable, PageFaultException, PageTableFullException


class Simulation(object):
    """
    Virtual Memory Simulation

    The actual simulation to run that models virtual memory accesses in a
    system.

    Args:
        filename (string): the file to read the memory accesses from
        alg_name (string): the name of the algorithm to use for choosing
            the memory page to free
    """

    def __init__(self, filename, alg_name, num_fames, refresh, tau):
        self.page_table = PageTable(num_fames)
        self.page_fault_counter = 0
        self.memory_access_counter = 0
        self.disk_write_counter = 0
        self._load_replacement_algorithm(alg_name, refresh, tau)
        self._load_memory_accesses_from_file(filename)

    def _load_memory_accesses_from_file(self, filename):
        self.accesses = Queue()
        with open(filename) as f:
            for index, line in enumerate(f):
                self._parse_memory_access(line.strip(), index)

    def _load_replacement_algorithm(self, alg_name, r, t):
        self.alg = get_replacement_algorithm(alg_name, self.page_table, r, t)

    def _parse_memory_access(self, line, index):
        [address, access_type] = line.split(' ', 1)
        access = MemoryAccess(address, access_type, index)
        access = self.alg.preprocess_memory_access(access)
        self.accesses.put(access)

    def run(self):
        """
        Run the simulation
        """
        [self._handle_memory_access(access) for access in self]

    def _handle_memory_access(self, access):
        """
        Handle a given memory access
        """
        self.memory_access_counter += 1
        access = self.alg.process_memory_access(access)
        self._insert_into_table(access)
        # Set the page to dirty if the access is a write
        page_value = self.page_table[access]
        page_value.referenced = True
        if access.write:
            page_value.dirty = True
        self.alg.postprocess_memory_access(access)

    def _insert_into_table(self, access):
        """
        Load some required memory into RAM

        Attempts an insert into RAM for some given access.  If needed, calls
        the right methods to free space in the page table
        """
        try:
            self.page_table.insert(access)
        except PageFaultException as e:
            self._handle_page_fault(e, access)

    def _handle_page_fault(self, exception, access):
        """
        Handle a page fault
        """
        self.page_fault_counter += 1
        if isinstance(exception, PageTableFullException):
            self._free_table_space()
            self.page_table.insert_no_check(access)

    def _free_table_space(self):
        num_freed_pages = self.alg.free_memory()
        self.disk_write_counter += num_freed_pages

    def __iter__(self):
        """
        Iterate over each memory access in the simulation
        """
        while not self.accesses.empty():
            yield self.accesses.get()

    def __str__(self):
        return dedent('''\
                      {}
                      Number of frames:       {}
                      Total memory accesses:  {}
                      Total page faults:      {}
                      Total writes to disk:   {}'''
                      ).format(self.alg.name,
                               self.page_table.size,
                               self.memory_access_counter,
                               self.page_fault_counter,
                               self.disk_write_counter)
