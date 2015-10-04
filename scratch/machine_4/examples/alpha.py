from machine import Machine
from node import Node
from conditions import Condition


class AlphaNode(Node):
    alpha = 'A'
    bravo = 'B'
    charlie = 'C'
    delta = 'D'
    echo = 'E'
    foxtrot = 'F'
    golf = 'G'
    hotel = 'H'
    india = 'I'
    juliett = 'J'
    kilo = 'K'
    lima = 'L'
    mike = 'M'
    november = 'N'
    oscar = 'O'
    papa = 'P'
    quebec = 'Q'
    romeo = 'R'
    sierra = 'S'
    tango = 'T'
    uniform = 'U'
    victor = 'V'
    whiskey = 'W'
    xray = 'X'
    yankee = 'Y'
    zulu = 'Z'


class GreekNode(Node):
    alpha = 1
    beta = 2
    gamma = 3
    delta = 4
    epsilon = 5
    zeta = 6
    eta = 7
    theta = 8
    iota = 9
    kappa = 0
    mu = 1
    nu = 2
    xi = 3
    omicron = 4
    pi = 5
    rho = 6
    sigma = 7
    tau = 8
    upsilon = 9
    phi = 0
    chi = 1
    psi = 2
    omega = 3


def run():
    ma = Machine('example')
    n = AlphaNode()
    ma.add(n)
    return ma


def main():
    return run()


if __name__ == '__main__':
    main()
