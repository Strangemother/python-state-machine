from machine import Machine
from node import Node, ProxyNode
from conditions import Condition

peer = 'PYRO:obj_71a5a950caf0450b95b0d4b3b4b20044@localhost:41213'

def run():
    print 'machine echo side a'
    ma = Machine('proxy_runner')
    ma.add_peer(peer)
    n = ProxyNode('node.example.TestNode')
    ma.add(n)

    return ma

def main():
    return run()


if __name__ == '__main__':
    main()
