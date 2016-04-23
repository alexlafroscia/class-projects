from random import random
from math import floor
from collections import deque
from replacement_algorithms.base import BaseReplacement


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

    @property
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

    def clear_space(self, tau, current_time):
        """
        Clear a space for a new item to be added to the queue

        Iteration looks a bit weird because of the fact that we need to rotate
        the queue each time through.

        Note: might be able to clean up that interface by overwriting the
        __iter__ method

        Arguments:
            tau (int): the age to check when determining whether the page
                       should be removed from memory
            current_time (int): the current time

        Returns:
            tuple:
                int: The key for the page to free
                int: The number of pages written to disk
        """
        counter = len(self)
        key_to_free = None
        written_pages = 0
        oldest_key = None
        oldest_timestamp = 0
        while True:
            if counter == 0:
                break;
            key, page = self.head

            # Keep track of the oldest page, just in case we need this info
            if page.timestamp >= oldest_timestamp:
                oldest_timestamp = page.timestamp
                oldest_key = key

            # If the page is not referenced and clean, we can stop
            if not page.referenced and not page.dirty:
                key_to_free = key
                break

            # If the page is not referenced, dirty and older than tau, we can
            # write it to disk and clean it
            if not page.referenced and page.dirty and page.get_age(current_time) > tau:
                written_pages += 1
                page.dirty = False
            # Finish loop
            self.rotate(-1)
            counter -= 1

        if key_to_free is not None:
            self._remove_page_with_key(key_to_free)
            if page.dirty:
                return (key_to_free, written_pages + 1)
            else:
                return (key_to_free, written_pages)
        else:
            page = self._remove_page_with_key(oldest_key)
            # make sure to count this page as written out
            if page.dirty and not page.get_age(current_time) > tau:
                written_pages += 1
            return (oldest_key, written_pages)

    def _remove_page_with_key(self, key):
        """
        Removes the page with the given key from the queue
        """
        for index, item in enumerate(self):
            k, v = item
            if key == k:
                del self[index]
                break
        return v

    def __str__(self):
        string = ''
        for key, value in self:
            string += "{}: {}\n".format(key, repr(value))
        return string


class WSCReplacement(BaseReplacement):

    name = 'Working Set Clock'

    def __init__(self, *args):
        BaseReplacement.__init__(self, *args)
        queue_size = self.page_table.size
        self.queue = CircularQueue(maxlen=queue_size)
        self.current_time = 0
        self.time_since_refresh = 0

    def process_memory_access(self, access):
        self.current_time = access.index
        if self.time_since_refresh == self.refresh_rate:
            self._clear_memory_references()
        self.time_since_refresh += 1
        return access

    def postprocess_memory_access(self, access):
        """
        Items to the queue
        """
        page_value = self.page_table[access]
        key = access.page_index
        self.queue.enqueue((key, page_value))

    def _clear_memory_references(self):
        for k, page in self.page_table:
            if page.referenced:
                page.referenced = False
                page.timestamp = self.current_time
        self.time_since_refresh = 0

    def free_memory(self):
        index, written = self.queue.clear_space(self.tau, self.current_time)
        self.page_table.free_indecies(index)
        return written
