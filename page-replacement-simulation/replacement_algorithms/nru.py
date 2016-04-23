import random
from replacement_algorithms.base import BaseReplacement


class PageClassifier:

    def __init__(self):
        self.page_classes = {
            '0': [],
            '1': [],
            '2': [],
            '3': []
        }

    def classify_page(self, key, v):
        category = self._get_category_from_properties(v.referenced, v.dirty)
        self.page_classes[category].append(key)

    def get_page_to_free(self):
        """
        Gets the key for the best page to free

        Checks each category in order of preference (0 -> 3) to see if there
        are any pages that have been assigned to that category.  If there are,
        pick one randomly to free.

        Returns:
            int: the key to free, or None if there is nothing to free
        """
        for value in ['0', '1', '2', '3']:
            if len(self.page_classes[value]) > 0:
                return self._get_item_from_category(value)
        return None

    def _get_category_from_properties(self, referenced, dirty):
        """
        Get classification based on page value

        Exchange a combination of `referenced` and `dirty` for a classification

        Args:
            referenced (boolean): whether the page was referenced
            dirty (boolean): whether the page has been written to

        Returns:
            string: the classification that the page belongs in
        """
        if referenced and dirty:
            return '3'
        elif referenced and not dirty:
            return '2'
        elif not referenced and dirty:
            return '1'
        elif not referenced and not dirty:
            return '0'

    def _get_item_from_category(self, value):
        page_values = self.page_classes[value]
        max_index = len(page_values) - 1
        index = random.randint(0, max_index)
        return page_values[index]


class NRUReplacement(BaseReplacement):

    name = 'NRU'

    def __init__(self, *args):
        BaseReplacement.__init__(self, *args)
        self.time_since_refresh = 0

    def process_memory_access(self, access):
        if self.time_since_refresh == self.refresh_rate:
            self._clear_memory_references()
        self.time_since_refresh += 1
        return access

    def free_memory(self):
        index = self._get_index_to_free()
        return self._free_memory_with_index(index)

    def _get_index_to_free(self):
        page_classes = PageClassifier()
        for key, value in self.page_table:
            page_classes.classify_page(key, value)
        return page_classes.get_page_to_free()

    def _clear_memory_references(self):
        for k, value in self.page_table:
            value.referenced = False
        self.time_since_refresh = 0
