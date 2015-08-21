#!/usr/bin/env python
"""
The registry server listens to broadcasts on UDP port 18812, answering to
discovery queries by clients and registering keepalives from all running
servers. In order for clients to use discovery, a registry service must
be running somewhere on their local network.
"""
from plumbum import cli
from rpyc.utils.registry import REGISTRY_PORT, DEFAULT_PRUNING_TIMEOUT
from rpyc.utils.registry import UDPRegistryServer, TCPRegistryServer
from rpyc.lib import setup_logger


class UDPRegistry(UDPRegistryServer):

    def on_service_added(self, name, addrinfo):
        ''' called when a new service joins the registry (but not on keepalives). override this to add custom logic'''
        print 'on_service_added'
        super(UDPRegistry, self).on_service_added(name, addrinfo)

    def on_service_removed(self, name, addrinfo):
        ''' called when a service unregisters or is pruned. override this to add custom logic'''
        print 'on_service_removed'
        super(UDPRegistry, self).on_service_removed(name, addrinfo)

    def cmd_query(self, host, name):
        ''' implementation of the query command'''
        print 'cmd_query'
        super(UDPRegistry, self).cmd_query(host, name)

    def cmd_register(self, host, names, port):
        ''' implementation of the register command'''
        print 'cmd_register'
        super(UDPRegistry, self).cmd_register(host, names, port)

    def cmd_unregister(self, host, port):
        ''' implementation of the unregister command'''
        print 'cmd_unregister'
        super(UDPRegistry, self).cmd_unregister(host, port)

    def start(self, ):
        ''' Starts the registry server (blocks)'''
        print 'start'
        super(UDPRegistry, self).start()

    def close(self, ):
        ''' Closes (terminates) the registry server'''
        print 'close'
        super(UDPRegistry, self).close()


class RegistryServer(cli.Application):
    mode = cli.SwitchAttr(["-m", "--mode"], cli.Set("UDP", "TCP"), default = "UDP",
        help = "Serving mode")

    ipv6 = cli.Flag(["-6", "--ipv6"], help="use ipv6 instead of ipv4")

    port = cli.SwitchAttr(["-p", "--port"], cli.Range(0, 65535), default = REGISTRY_PORT,
        help = "The UDP/TCP listener port")

    logfile = cli.SwitchAttr(["--logfile"], str, default = None,
        help = "The log file to use; the default is stderr")

    quiet = cli.SwitchAttr(["-q", "--quiet"], help = "Quiet mode (only errors are logged)")

    pruning_timeout = cli.SwitchAttr(["-t", "--timeout"], int,
        default = DEFAULT_PRUNING_TIMEOUT, help = "Set a custom pruning timeout (in seconds)")

    def main(self):
        if self.mode == "UDP":
            server = UDPRegistry(host = '::' if self.ipv6 else '0.0.0.0', port = self.port,
                pruning_timeout = self.pruning_timeout)
        elif self.mode == "TCP":
            server = TCPRegistryServer(port = self.port, pruning_timeout = self.pruning_timeout)
        setup_logger(self.quiet, self.logfile)
        server.start()


if __name__ == "__main__":
    RegistryServer.run()
