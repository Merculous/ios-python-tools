try:
    import usb
except ImportError:
    raise


class USB:
    def __init__(self):
        super().__init__()

        # Some stuff with WTF, maybe we can force DFU somehow?

        # 05ac:1260 Nano 2G regular/disk mode

        # ffff:8642 Nano 2G iBugger Loader

        # dev.idVendor == 0x05ac and dev.idProduct == 0x1220 Bootrom DFU

        # dev.idVendor == 0x05ac and dev.idProduct == 0x1240 Nano 2G NOR DFU (WTF I think/SoftDFU)

        # 05ac:12a8 Normal mode iPhone 5S

        # 05ac:1227 DFU mode iPhone 5S

        # 05ac:1281 Recovery mode iPhone 5S

        # Uploading /home/merculous/Documents/ibugger/ibugger/core-2.bin to 0x22000000.... done
        # Passing control to code at 0x22000020... done
        # Connected to iBugger Core v0.1.1 on iPod Nano 2G, USB version 00.01

        # TODO Add Pwnage 2.0 support. Just uploading a malformed certificate/file

    def getDevices(self):
        pass

    def sendPacket(self):
        pass

    def unpackPacket(self, packet):
        pass

    def debugNano2G(self):
        pass

    def sendCommand(self, command):
        pass

    def enterRecovery(self):
        pass
