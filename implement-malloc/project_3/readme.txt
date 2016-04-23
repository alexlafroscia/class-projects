My Malloc and Free
Author: Alex LaFroscia
Date: Nov 3, 2014


# Problems with My Solution

I wasn't able to get a properly working version of `free` going with the way
that I set up the program.  I understand what the problem is, but ran out of
time to be able to fix it.

The way that I kept track of the free nodes of each order was to create an array
of structs, where each struct pointed to the first free node, and the index of
the array represented the order.  This worked great for allocation, but when it
came time to deallocate, it didn't work as well.  What I realized was that
the first free node for each order didn't have a pointer to the object in the
array that was referencing it, so it wasn't easy to remove the node from the
linked list.  Because of this, during coallescing, nodes got left in the linked
list for a particular order instead of propetly being removed.  Obviously, this
coallescing to fail.

To fix this problem, I would have needed to make a better way to reference each
linked list of free nodes, so that I could always remove them from the list
for each order.  I tried doing this using a void pointer in the `FreeHeader`
structs but this led to issues that I didn't have enough time to fix.  If I
were to start over, I would design the array so that the nodes that represent
free chunks of memory always have a reference to both the previous and next
nodes.  If this was done correctly, the rest of the `my_free` algorithm should
work.
