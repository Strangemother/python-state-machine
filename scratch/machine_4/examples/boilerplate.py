from machine import Machine
from node import Node
from conditions import Condition


class TestNode(Node):
    color = 'red'

def run():
    ma = Machine('example')
    n = TestNode()
    ma.add(n)
    return ma

def main():
    return run()


if __name__ == '__main__':
    main()
