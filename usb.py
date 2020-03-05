import os
import sys

from pymobiledevice.afc import AFCClient, AFCShell
from pymobiledevice.diagnostics_relay import DIAGClient
from pymobiledevice.lockdown import LockdownClient


"""

Gets all the info I could possibly get from using pymobiledevice (patched version)

"""


class USB(object):
    def __init__(self):
        super().__init__()

    def deviceISPaired(self):
        device = LockdownClient()
        return device.validate_pairing()

    def copyFromDevice(self, path):
        if self.deviceISPaired():
            print('[NOTE] AFC is restricted to a certain directory: /var/mobile/Media')
            shell = AFCShell()
            print('Downloading:', path)
            shell.do_pull(path)
        else:
            sys.exit('Not continuing since the device is not paired')

    def getInfo(self):
        info = DIAGClient()
        data = info.query_mobilegestalt()  # This is a dict lol
        print('Apnonce:', data['ApNonce'])  # idk which apnonce this belongs to
        print('ChipID:', data['ChipID'])
        print('DeviceClass:', data['DeviceClass'])  # Device family
        print('DeviceName:', data['DeviceName'])  # Device name
        print('FirmwareVersion:', data['FirmwareVersion'])  # iBoot version
        print('HWModelStr:', data['HWModelStr'])  # Model
        print('HardwarePlatform:', data['HardwarePlatform'])  # SoC
        print('MLBSerialNumber:', data['MLBSerialNumber'])  # Serial number
        print('ProductType:', data['ProductType'])
        print('ProductVersion:', data['ProductVersion'])  # iOS
        print('UniqueChipID:', data['UniqueChipID'])  # ECID
        print('UniqueDeviceID:', data['UniqueDeviceID'])  # UDID
        print('encrypted-data-partition:', data['encrypted-data-partition'])  # Data-protection?

    def deviceReboot(self):
        device = DIAGClient()
        device.restart()

    def deviceEnterRecovery(self):
        device = LockdownClient()
        device.enter_recovery()

    def getDevice(self):
        device = DIAGClient()
        data = device.query_mobilegestalt()
        return data['ProductType']

    def getECID(self):
        device = DIAGClient()
        data = device.query_mobilegestalt()
        return data['UniqueChipID']
