open states.

A node connected state machine designed to implement income outcome of tree
nodes though objects (driven states) to dispatch events.
Events will infere concurrent actions.

Actions will be performed from events through the node cloud.
The node cloud will imply further event dispatches.

A and B and C and D
then C

A.state == 1 and B.state == 1 and C.state == 2

A Node:

An object of reference with keys of state values.

+ node values will change
+ A change dispatches a change event


Senario:

automated vehicles:

Objects representing dictionarys to changed based on network alteration. In this
case, hardware outside the network alters a network node(s) - actions will infer

Car auto stop:

	P = Promxity
    C = Car
    H = Hardware

Input:

	P.distance = 20
	P.their_speed = 15

Logic:

	if P.distance < 30 and P.their_speed < 20:
		# coming up close
        P.status = 'warning'

    if P.status == 'warning' and C.speed < P.their_speed:
        # Slow down
        dispatch('slow-down')


    On C.back_light == True:
        H.backlight = 'on'

The event 'begin-braking' and the back_light is on. change the HUD

    On 'begin-braking' and C.back_light = True:
        C.hud.status = 'Braking has begun'

The event 'slow-down' actions the car.

    On 'slow-down':
        C.slow_down()

The event turn-off will deactive much of the hardware

    On 'turn-off':
        C.stop()
        H.back_light = False
        H.indicators = False
        H.front_light = False
        H.hud = False
        H.radio = False
        H.air_con = False
        H.heating = False
        H.ignition = False

    On 'lock':
        H.windows = 'Close'
        H.ignition = False
        H.brakes = True
        H.sensors = True
        H.anti_theft = True
        H.doors = 'Lock'
        H.boot = 'Lock'

A dispatched event has data. The data should be accessible as part of the event
state to react to.
A remote send a 'lock' command, the network node H could send events

    On 'Remote' and Remote.lock == True:
        off = dispatch(turn-off)
        locked = dispatch('lock')
        if off and locked:
            dispatch('secure')

A action dispatches and changes state

    C.slow_down():
        dispatch('begin-braking', {})
        C.back_light = True


### A Node:

An object of reference with keys of state values.

+ A node is a dictionary of anything to state upon
+ node values will change
+ A change to a value dispatches a change event

### An Event

+ sends messages of state change within the network
+ can carry state data in and out of the network

## An Action

+ requires all conditions to be met before performing.
+ can dispatch an event
+ can change the state of another node
+ call other actions

## Reaction

+ can monitor changes to a node state
+ can call a method or action during reaction
+ can check is a state is true

Card states:

if cards are 5C 6C 7C 8C 9C this is a straight flush - the best hand. Lets
state machine this.

U = User
C = Card
D = Deck
T = Table

    U.ask(s):
        if s == 'small':
            if U.money >= T.small_blind.value:
                dispatch('answer', 'small')
        if s == 'big':
            if U.money >= T.big_blind.value:
                dispatch('answer', 'big')


    On 'hole-cards':
        U.give_card( e[0] ) # 5H
        U.give_card( e[1] ) # 6H

    On 'add-small-blind':
        T.small_blind = True

    On 'add-big-blind':
        T.big_blind = True

    On T.big_blind == True
        and T.small_blind == True:
        T.button_position = T.dealer<U>.position + 2

On change of a single value:

    On T.button_position:
        T.users[T.button_position].ask()

    # U.ask() has an answer.
    On 'answer':
        if e.value == 'call':
            if e.call_value >= U.min_call:
                T.round_pot += e.call_value
                T.user_turn += 1
            else:
                U.status = 'Must match previous raise'
        if e.value == 'raise':
            T.round_pot += e.call_value
            T.users[T.user_turn+1].min_call = e.call_value
            T.user_turn += 1
        if e.value == 'fold':
            U.fold_cards()
            T.user_turn += 1
        if e.value == 'small':
            dispatch('add-small-blind')
        if e.value == 'big':
            dispatch('add-big-blind')

    On T.user_turn == T.users.length:
        T.user_turn = 0
        dispatch('round')

    On 'move-dealer':
        if T.dealer.position == T.players.length:
            T.dealer.position = 0
        else:
            T.dealer.position += 1
            dispatch('deal-cards')


    On 'deal-cards':
        for U in T.players:
            U.hold_cards( D.new_card(), D.newCard() )
        if T.status = ''
        dipatch('start-round')

    On 'start-round':
        print 'start round'
        dispatch('receive-bets')

    On 'receive-blinds':
        T.players[T.user_turn + 1].ask('small')
        T.players[T.user_turn + 2].ask('big')
        dispatch('receive blinds')

    On 'receive-bet':
        T.round_pot += e.value
        T.user_turn += 1

    On 'table-card'
        and D.table_cards().length == 3
        and T.state = 'delt':
        T.state = 'the flop'
        T.betting_round = 1
        T.ask_bets()


    On 'deal-flop':
        # three community cards
        D.table_card( D.new_card() ).face_up()
        D.table_card( D.new_card() ).face_up()
        D.table_card( D.new_card() ).face_up()


    On 'receive-bets':
        for U in T.players:
            U.ask()


Game flow

    + move dealer
        U
    + receive blinds
    + U deal cards
    + start round
    + U deal flop
    + receive bets
    + deal turn
    + receive bets
    + deal river
    + receive bets
    + award best hand

