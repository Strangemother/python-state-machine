# Python state machine


A node connected state machine designed to implement income outcome of tree
nodes though objects (driven states) to dispatch events.
Events will infere concurrent actions.

Actions will be performed from events through the node cloud.
The node cloud will imply further event dispatches.


The entire procedure is non blocking, event clear and scalable. With a reactive state machine performing computatuions based upon calculated events, can allow waterfall logic through many nodes,creating a network of reactions.

## Scenario

A Node 'Alpha' will react when a 'beta' node is added to the network.

We can imply a machine to accept the incoming node and implement an immediate reactive state for existing nodes and the newly implemented node 'alpha'

Beta:
	value = 1
	when 'alpha'.value == 1:
		beta.value = 2

	integrate(beta)
	integrate(alpha)
	alpha.value = 1
	beta.value == 2

This very simple concept should span aross nodes of any size, performing reative responses upon each change. In turn, an action will alter many values within the network.

