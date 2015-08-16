# Reactive network concept

The theory; solve the rudimentary issue of agnostic logical components connected via a homogeneous network of secure events.

Consider the scenario of connecting many agnostic tools to an event driven interface. Our concept can be the automated home. A simple rule 'hall lights on when the front door is unlocked' can be applied with many valid implementations.
However growing the network of devices and implementing more conditions will create a bloated core of (hopefully) compatible devices.

The win is to spread the required logical analysis of this scenario across many devices, maintaining personal logic specific to purpose. Consider the lighting cared for by a cheap shelf product and the security system governed by another.

Connecting the two API's requires an intermediate and processors on each device connected.

---

The goal of this project to provide a solution for this problem by developing a framework for a reactive action to state driven events.

When developing a component for the state machine, we only consider the requirements for the 'Node' connecting to the network. A Node will monitor conditions of other named nodes within the network, performing computational logic when a change in a monitored node occurs.

We can connect nodes across a homogeneous network naturally secure, bridged across hops and scalable using cheap software and hardware tools. 

---

In the scenario of the 'light bulb' - we wait for a condition 'on' set True and conditional actions will perform application logic.

In turn, other Nodes such as 'door lock' on the network can cheaply monitor the change of a 'light bulb' 'on' set True - applying independent derived from the action watched.

This simple case can be based upon a small network of nodes, or many - all inter-dependently monitoring Node changes and react when required.

---

The API provided will aim to be a clean python interface for developing a node using off-the-shelf python modules. With the ability to install the platform on many cheap hardware devices. 

This will allow the communication of many devices throughout a scalable network without requiring a central point of failure.


## API

A basic node can have values of which exist on the network. No reaction need to occur. This could be a simple state Node

    
    class LightBulb(Node):
        on = False
        color = 'red'
        value = 20


These values can be read and altered by the other nodes on the network.

Watching a network node change can be explicit or agnostic.

    class House(Node):

        def lightbulb_on(self, node, state):
            if state == True:
                self.set('tv', 'on', true)

        def reactions(self):
            return (
                Condition('lightbulb', 'on', self.lightbulb_on)
            )

By listening to and sending basic states, the objects defined are mapped internally to react in a modular way. In this example API, the 'house' sets the value 'tv.on' when the lights are on. 

Because there is no event handling or API structure to communicate through, implementing this to any device or platform is extremely decoupled.

---

Each component applied through the API is modular by it's design. The underlying API should be considered as a secure component to monitor changes through you decoupled applications.

The goal of this project will provide a layer to communicate state changes through a homogeneous network of bridged applications.

+ Allows for a scalable architecture natively
+ Object secure by default
+ Cheap API using tested code

API considerations and platforms will leverage:

+ python core and pip packages
+ websockets
+ multithread libs
+ object-storage

---

# Extended API

## Node

+ component of the network
+ Can be connected explicitly or implicitly
+ Can be extended for API use

## Manager

+ Maintains a connection of network nodes
+ Should be peer connected
+ Can bridge connections
+ Pass messages 

## Framework

+ Messages are naturally secure 
+ Automatically thread
+ Automatically event change and reactions
+ Distribute process pools

## Plugin Architecture

+ a Node can implement plugins
+ a reactive plugin assigns