# Machine

A machine drives a number of nodes on the network. A node must exist within a container to capture its changes and dispatch those values across the network.

A machine will provide a storage point for the nodes. When a nodes value is changed, the name of the attribute and the value are dipatched through an event propogator.

The machine has applied an event listener to the node upon implementation. This value is sent through the network distribution layer. Other machines are waiting for maessages on the network.

When a machine hears an event, the local nodes are compared against a the events id. If a matching local node is found the associated attribute is updated.

The event is dispatched through the machines peers. This doe snot include the original peer. Other machines on the chain will react and perform the same routine.

## Event chain

The event propogated should be light. containing addressing information and the key value of the attribute changed. Any more and the network may become bloated.

For expensive objects a pointer should be provided the handler of the expensive event should resolve the pointer after a match. The value stored to a local node should not be a pointer, but the result object.

This should be performed transparently by the machine layer. When an event is heard a machine should both react and propograte the event.


