from access import MemoryAccess


class PageFaultException(Exception):

    """
    Page Fault Exception

    Exception to raise when the page table doesn't already have the page it
    needs in memory, requiring that it is loaded from disk
    """
    pass


class PageTableFullException(PageFaultException):

    """
    Page Table Full Exception

    Exception to raise when the page table is full, requiring the invokation
    of some replacement algorithm to determine which page should be evicted
    from memory
    """
    pass


class Page(object):

    def __init__(self, referenced=False):
        self.dirty = False
        self.referenced = referenced
        self.timestamp = 0

    def get_age(self, current_time):
        return current_time - self.timestamp

    def __repr__(self):
        string = '<Page'
        if self.referenced:
            string += ' Referenced'
        if self.dirty:
            string += ' Dirty'
        return string + ' Timestamp: {} >'.format(self.timestamp)


class PageTable(object):

    """
    Page Table

    Represents the mapping of page frames to virtual memory pages

    Args:
        size (int): the max number of pages the table can hold, representing
            the number of page frames we have available
    """

    def __init__(self, size):
        self.size = size
        self.table = dict()

    @property
    def is_full(self):
        """
        Whether or not the table can hold another page without needing to
        evict something from memory
        """
        return len(self.table.keys()) == self.size

    def insert(self, access):
        """
        Insert a page into memory

        Given some memory access, determine what needs to happen to allow that
        memory to be accessed.

        If the page that is required is already in memory, we can essentially
        do nothing at all.

        If the page is not in memory but there is room in the table, we can
        insert the page but need to let the Simulation know that there was a
        "Page Fault" that occured.

        If the table is full, then we need to let the simulation know that a
        replacement algorithm needs to run and free some space for us to insert
        some of our virtual memory into a frame.

        One of these three conditions should always be met; anything else
        would be a real error.

        Args:
            access (MemoryAccess): the memory access to insert into the table

        Raises:
            PageFaultException: If a page fault occured
            PageTableFullException: If the page table is full, requiring the
                Simulation to invoke a replacement algorithm to free some space
                to make room for the new insertion
            RuntimeError: If the given insertion somehow did not fall into one
                of the three anticipated actions that should be valid on
                insertion
        """
        index = access.page_index
        if index in self.table:
            return True
        if not self.is_full:
            self.insert_no_check(access)
            raise PageFaultException()
        if self.is_full:
            raise PageTableFullException()
        raise RuntimeError('You shouldn\'t have gotten here...')

    def insert_no_check(self, access):
        self.table[access.page_index] = Page()

    def free_indecies(self, indecies):
        """
        Free some indecies in the page table

        Creates free spaces to place pages into by freeing indecies.  Counts
        the number of dirty pages that will be freed, and returns the number.

        Args:
            indecies (index or list of indecies): list of page indecies to free

        Returns:
            int: the number of page frames written to disk
        """
        written = 0
        if indecies is None:
            raise KeyError('Cannot free page without a valid index')
        if not isinstance(indecies, list):
            indecies = [indecies]
        for key in indecies:
            if self.table[key].dirty:
                written += 1
            del self.table[key]
        return written

    def get(self, access):
        """
        Get the value for some index
        """
        index = access
        if isinstance(access, MemoryAccess):
            index = access.page_index
        return self.table[index]

    def __getitem__(self, access):
        return self.get(access)

    def __iter__(self):
        return self.table.iteritems()

    def __len__(self):
        """
        Length of the page table is the number of frames filled
        """
        return len(self.table.keys())
