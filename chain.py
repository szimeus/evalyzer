import sys
import time
from pykd import *


class ChainFinder:
    usage = """USAGE:
    chain find -a <hex address> [ -l <maxlength> ] [ -dw <scanrange> ] [ -r <register name>]

    Starts from a register and tries to find a chain of pointers pointing to the specified address
    maxlength: specifies maximum number of dereferences (default=3)
    scanrange: specifies the range to be searched around the address in the count of dwords (default: 20)
    register name: what register value to start the search from (default: esp)"""
    __hits = []

    def __init__(self, args):
        if not args:
            args = []
        if len(args) > 1:
            thiscmd = args[1].lower().strip()
            if thiscmd == "find":
                dprintln("Starting find...")
            else:
                self.printusage()

            try:
                addridx = args.index("-a")
                addr = args[addridx + 1].lower().strip()
                addr = int(addr, 16)
                if "-l" in args:
                    maxhopidx = args.index("-l")
                    maxhops = int(args[maxhopidx + 1].lower().strip())
                else:
                    # using default value
                    maxhops = 3
                if "-dw" in args:
                    scanrangeidx = args.index("-dw")
                    scanrange = int(args[scanrangeidx + 1].lower().strip())
                else:
                    # using default value
                    scanrange = 20
                if "-r" in args:
                    regidx = args.index("-r")
                    myreg = args[regidx + 1].lower().strip()
                else:
                    # using default value
                    myreg = "esp"                
                dprintln("START: Finding chain to %s, starting from %s (%s)" % (hex(addr),myreg.upper(), hex(reg(myreg))))
                dprintln("max hops: %s, range: %s dwords" % (maxhops,scanrange))
                beginning = time.time()
                self.__hits = []
                self.track(addr64(reg(myreg)), 1, addr, maxhops, scanrange, myreg)
                if len(self.__hits) > 0:
                    self.__hits.sort(key=len)
                    for hit in self.__hits:
                        dprintln(hit)
                else:
                    dprintln("No chains were found. Maybe you could try with different arguments?")
                dprintln("DONE. Total time elapsed: %0.2f seconds" % (time.time() - beginning))
            except:
                self.printusage()
        else:
            self.printusage()

    def track(self, address, depth, target, maxhops, scanrange, path):
        for ofs in range(-scanrange, scanrange):
            sign = "" if(ofs < 0) else "+"
            dstaddr = address + (4 * ofs)
            if isValid(dstaddr):
                ptr = ptrDWord(dstaddr)
                if ptr == target:
                    self.__hits.append("poi(%s%s%s)" % (path, sign, hex(4 * ofs)))
                elif (isValid(ptr)) and (depth <= maxhops):
                    self.track(ptr, depth + 1, target, maxhops, scanrange, "poi(%s%s%s)" % (path, sign, hex(4 * ofs)))

    def printusage(self):
        dprintln(self.usage)
        quit()


if __name__ == "__main__":
    ChainFinder(sys.argv)
