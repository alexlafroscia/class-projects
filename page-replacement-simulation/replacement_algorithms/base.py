from abc import ABCMeta, abstractmethod


class BaseReplacement(object):

    __metaclass__ = ABCMeta
    name = 'Base'

    def __init__(self, page_table, refresh, tau):
        self.page_table = page_table
        self.tau = tau
        self.refresh_rate = refresh

    def preprocess_memory_access(self, access):
        """
        Preprocess a memory access before saving

        Allows a replacement algorithm to hook into the process of reading in
        the memory accesses from the file to pre-process or do any setup that
        might be necessary.  Subclasses do not have to implement this if there
        is no preprocessing that needs to be done.

        Args:
            access (MemoryAccess): The memory access object to process

        Returns:
            MemoryAccess: The access object that should be saved into the list
            accesses to process.  Can be the original object passed in.
        """
        return access

    def process_memory_access(self, access):
        """
        Process a memory access

        Allows the replacement algorithm to do something with the access before
        the simulation tries to place it into the table
        """
        return access

    def postprocess_memory_access(self, access):
        """
        Do something after memory access has been handled

        Allows the replacement algorithm to do something after the memory
        access has been handled and the page is in the page table.  This is
        useful for instances where we need to do something with the page value
        for some access before handling the next one.
        """
        pass

    @abstractmethod
    def free_memory(self):
        """
        Free some memory to make room to put something new into a frame

        Abstract method that must be implemented by all subclasses

        Returns:
            int: the number of pages "written to disk"
        """
        pass

    def _free_memory_with_index(self, index):
        """
        Used by subclasses to free memory and get the number of dirty pages
        """
        page_value = self.page_table[index]
        self.page_table.free_indecies(index)
        if page_value.dirty:
            return 1
        else:
            return 0
