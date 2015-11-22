# Network resolutions

Networking machines involves the remote connection to a dispatch layer. A machine hears an event from a node. Dependant upon implementation the machine should propograte this event and its values to a list of connected machines or proxy machines.

The connections should be adhoc. By providing an address string to a machine should result in a transparent connection and an event chain reaction.

Pre-configuring a machine should also be extremely simple. A machine should only need a connection pattern `HOST:PORT` or a resolvable address object.

The machine will resolve a connection as a peer - expecting an equaivilent machine type to be the address resolver. Peering machines allows agnostic dispatch across a flat layer of connected objects.

Peered connections should resolve chains of peers; allowing the event to propogate through sub-networks of a peers connection. The peers of peers may not be a-symetrical therefore circular referencing or chained dependencies must be watched.

---

An easy resolution to replica events is an ID match or event a vector clock monitoring the nodes events through the chain.

The machine should handle resolution of duplicate events during a translation phase.

If an event with the same reference as a previously assigned event is captured through the chain, the handling of the events destination should be based upon the machines conditions or default conditions.

Pointers to large data objects should be resolved at this stage. Addition resolution points for security and proxies

