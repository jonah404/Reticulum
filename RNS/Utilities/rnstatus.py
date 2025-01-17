#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2016-2022 Mark Qvist / unsigned.io
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import RNS
import argparse

from RNS._version import __version__

def size_str(num, suffix='B'):
    units = ['','K','M','G','T','P','E','Z']
    last_unit = 'Y'

    if suffix == 'b':
        num *= 8
        units = ['','K','M','G','T','P','E','Z']
        last_unit = 'Y'

    for unit in units:
        if abs(num) < 1000.0:
            if unit == "":
                return "%.0f %s%s" % (num, unit, suffix)
            else:
                return "%.2f %s%s" % (num, unit, suffix)
        num /= 1000.0

    return "%.2f%s%s" % (num, last_unit, suffix)

def program_setup(configdir, dispall=False, verbosity = 0):
    reticulum = RNS.Reticulum(configdir = configdir, loglevel = 3+verbosity)
    
    ifstats = reticulum.get_interface_stats()
    if ifstats != None:
        for ifstat in ifstats:
            name = ifstat["name"]

            if dispall or not (name.startswith("LocalInterface[") or name.startswith("TCPInterface[Client")):
                print("")
                if ifstat["status"]:
                    ss = "Up"
                else:
                    ss = "Down"

                if ifstat["clients"] != None:
                    clients = ifstat["clients"]
                    if name.startswith("Shared Instance["):
                        clients_string = "Connected applications: "+str(max(clients-1,0))
                    else:
                        clients_string = "Connected clients: "+str(clients)

                else:
                    clients = None

                print(" {n}".format(n=ifstat["name"]))
                print("\tStatus: {ss}".format(ss=ss))

                if "i2p_b32" in ifstat:
                    print("\tI2P B32: {ep}".format(ep=str(ifstat["i2p_b32"])))

                if clients != None:
                    print("\t"+clients_string)
                print("\tRX: {rxb}\n\tTX: {txb}".format(rxb=size_str(ifstat["rxb"]), txb=size_str(ifstat["txb"])))

        print("")
                
    else:
        print("Could not get RNS status")

def main():
    try:
        parser = argparse.ArgumentParser(description="Reticulum Network Stack Status")
        parser.add_argument("--config", action="store", default=None, help="path to alternative Reticulum config directory", type=str)
        parser.add_argument("--version", action="version", version="rnstatus {version}".format(version=__version__))

        parser.add_argument(
            "-a",
            "--all",
            action="store_true",
            help="show all interfaces",
            default=False
        )

        parser.add_argument('-v', '--verbose', action='count', default=0)
        
        args = parser.parse_args()

        if args.config:
            configarg = args.config
        else:
            configarg = None

        program_setup(configdir = configarg, dispall = args.all, verbosity=args.verbose)

    except KeyboardInterrupt:
        print("")
        exit()

if __name__ == "__main__":
    main()
