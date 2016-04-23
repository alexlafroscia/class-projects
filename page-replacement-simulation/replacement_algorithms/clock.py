from replacement_algorithms.base import BaseReplacement
from collections import deque


class CircularQueue(deque):

    """
    A more friendly circular queue

    Extends the default `deque` data structure with some helper methods that
    make it more suitable for the operations that we need to perform, namely
    retrieving the item that is currently being pointed to and clearing a space
    for a new item.

    Instead of actually keeping a pointer to the front of the queue, we instead
    assume that the element in the first index is the one that the "hand" is
    pointing to.  This allows us to use the built-in `rotate` method to move
    through the queue in a circular way, instead of moving the pointer to
    different indecies.
    """

    def head(self):
        """
        Get the item that the "hand" is pointing to
        """
        return self[0]

    def enqueue(self, value):
        """
        Wrap the append method to ensure duplicates aren't added
        """
        (key, v) = value
        if key not in [item[0] for item in self]:
            self.append(value)

    def clear_space(self):
        """
        Clear a space for a new item to be added to the queue

        Iterate through the values in the queue until we can find one to
        remove.  Page values that are referenced are spared, having their
        reference bits set back to `False`.  If we come across a value that
        hasn't been referenced, that is the item that should be removed from
        the queue.

        Returns:
            int: The key for the page to free
        """
        key_to_free = None
        while key_to_free is None:
            key, page_value = self.head()
            if page_value.referenced:
                page_value.referenced = False
                self.rotate(-1)
            else:
                self.popleft()
                key_to_free = key
        return key_to_free


class ClockReplacement(BaseReplacement):

    name = 'Clock'

    def __init__(self, *args):
        BaseReplacement.__init__(self, *args)
        queue_size = self.page_table.size
        self.queue = CircularQueue(maxlen=queue_size)

    def postprocess_memory_access(self, access):
        """
        Items to the queue
        """
        page_value = self.page_table[access]
        key = access.page_index
        self.queue.enqueue((key, page_value))

    def free_memory(self):
        """
        Free memory using the circular queue

        If we need to free memory, invoke the appropriate method on the
        underlying CircularQueue object to determine which index should be
        removed.  Then, free the page with that index.
        """
        index = self.queue.clear_space()
        return self._free_memory_with_index(index)
