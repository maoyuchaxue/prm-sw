#!/usr/bin/env python3
"""
OpenOCD RPC example, covered by GNU GPLv3 or later
Copyright (C) 2014 Andreas Ortmann (ortmann@finf.uni-hannover.de)
"""

import socket
import itertools
import sys

def hexify(data):
    return "<None>" if data is None else ("0x%08x" % data)

class OpenOcd:
    COMMAND_TOKEN = '\x1a'
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.tclRpcIp       = "127.0.0.1"
        self.tclRpcPort     = 6666
        self.bufferSize     = 4096

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __enter__(self):
        self.sock.connect((self.tclRpcIp, self.tclRpcPort))
        return self

    def __exit__(self, type, value, traceback):
        try:
            self.send("exit")
        finally:
            self.sock.close()

    def send(self, cmd):
        """Send a command string to TCL RPC. Return the result that was read."""
        data = ('capture "' + cmd + '"' + OpenOcd.COMMAND_TOKEN).encode("utf-8")
        if self.verbose:
            print("<- ", data)

        self.sock.send(data)
        return self._recv()

    def _recv(self):
        """Read from the stream until the token (\x1a) was received."""
        data = bytes()
        while True:
            chunk = self.sock.recv(self.bufferSize)
            data += chunk
            if bytes(OpenOcd.COMMAND_TOKEN, encoding="utf-8") in chunk:
                break

        if self.verbose:
            print("-> ", data)

        data = data.decode("utf-8").strip()
        data = data[:-1] # strip trailing \x1a

        return data.strip()

if __name__ == "__main__":
    if sys.argv[1] == 'start':
        asm = [
                0x000104b7, # lui s1, 0x10
                0x0404849b, # addiw s1, s1, 0x40
                ]
    else:
        asm = [
                0x000104b7, # lui s1, 0x10
                ]
    asm += [
            0x7b149073, # csrw dpc, s1
            0x7b002473, # csrr s0, dcsr
            0x00346413, # ori s0, s0 3 # change to m-mode
            0x7b041073, # csrw dcsr, s0
            0x00100073  # ebreak
            ]

    disable_vm = [
            0x00000493, # li s1, 0x0
            0x18049073, # csrw satp, s1
            0x00100073  # ebreak
            ]

    print(asm)

    progbuf_cmds = [(i + 0x20, data) for i, data in enumerate(asm)]
    with OpenOcd() as ocd:
        # Halt
        ocd.send("riscv dmi_write 0x10 0x80000001")
        # Progbuf
        for reg, data in progbuf_cmds:
            ocd.send("riscv dmi_write {} {}".format(reg, data))
        # Access Register
        ocd.send("riscv dmi_write 0x17 0x361001") # regno = sp, postexec, transfer, 64-bit
        abstractcs = ocd.send("riscv dmi_read 0x16")
        if abstractcs != "0x10000002":
            print("Exec error: abstracts " + abstractcs)
        # Resume
        ocd.send("riscv dmi_write 0x10 0x40000001")
