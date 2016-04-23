from replacement_algorithms.base import BaseReplacement
from heapq import heappush, heappop


class OptReplacement(BaseReplacement):

    name = 'Opt'

    def __init__(self, *args):
        BaseReplacement.__init__(self, *args)
        self.page_use_indecies = dict()
        self.current_index = 0

    def preprocess_memory_access(self, access):
        """
        Create table for storing page index access times

        Store a heap for each page index of the array into all of the memory
        accesses that it will be accessed at.  This should be a min heap,
        because we will use the first element in the heap to determine the
        "distance" from the current time that the page will be needed next,
        and will pop from this heap whenever that page is accessed
        """
        table = self.page_use_indecies
        page_index = access.page_index
        if page_index not in table:
            table[page_index] = []
        heappush(table[page_index], access.index)
        return access

    def process_memory_access(self, access):
        table = self.page_use_indecies
        page_index = access.page_index
        access_index = heappop(table[page_index])
        if access_index != access.index:
            raise RuntimeError('Page access index does not match expected')
        self.current_index = access_index
        return access

    def free_memory(self):
        index = self._get_index_to_free()
        if index is None:
            raise RuntimeError('Could not find a page to free')
        return self._free_memory_with_index(index)

    def _get_index_to_free(self):
        key_to_return = None
        max_distance = 0
        for page_index, v in self.page_table:
            d = self._get_distance_from_current(page_index)
            if d is None:
                return page_index
            if d > max_distance:
                max_distance = d
                key_to_return = page_index
        return key_to_return

    def _get_distance_from_current(self, page_index):
        """
        Get the distance to some index's next access

        Returns:
            int or None:
                int: distance to access
                None: no more accesses
        """
        table = self.page_use_indecies
        heap = table[page_index]
        if len(heap) == 0:
            return None
        else:
            return heap[0] - self.current_index
