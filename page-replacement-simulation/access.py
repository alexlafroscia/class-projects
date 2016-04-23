class MemoryAccess(object):
    """
    Memory Access Representation

    Models an access of virtual memory that will take place in the simulation.

    Args:
        address (int): the address that the access took place at
        access_type (string): the type of access that otook place.  Should
            either be 'R' or 'W' to represent Read or Write
    """

    def __init__(self, address, access_type, index):
        self.address = int(address, base=16)
        self.access_type = access_type
        self.index = index

    @property
    def read(self):
        """
        If the page access is a Read

        Returns:
            boolean: if the page access is a read
        """
        return self.access_type == 'R'

    @property
    def write(self):
        """
        If the page access is a Write

        Returns:
            boolean: if the page access is a Write
        """
        return self.access_type == 'W'

    @property
    def page_index(self):
        """
        The index of the page that needs to be accessed

        Since the page index is the 20 most significant bits of the address
        we are accessing, we can calculate the page index by shifting the
        address until those 20 bits are isolated.
        """
        return self.address >> 12

    def __str__(self):
        return "Address: {}, {}".format(self.address, self.access_type)
