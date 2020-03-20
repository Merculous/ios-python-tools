import sys

from pymobiledevice.afc import AFC2Client, AFCShell
from pymobiledevice.diagnostics_relay import DIAGClient
from pymobiledevice.lockdown import LockdownClient
from pymobiledevice.mobilebackup2 import MobileBackup2
from pymobiledevice.syslog import Syslog


"""

Gets all the info I could possibly get from using pymobiledevice (patched version)

"""


class USB(object):
    def __init__(self):
        super().__init__()

    def deviceISPaired(self):
        device = LockdownClient()
        return device.validate_pairing()

    def copyToDevice(self, input, output=False):  # AFC2
        if self.deviceISPaired():
            print('[NOTE] AFC is restricted to a certain directory: /var/mobile/Media')
            device = AFC2Client()
            print(device.read_directory('.'))
            if output:
                device.set_file_contents(output, input)
            else:
                device.set_file_contents(input, input)
            print(device.read_directory('.'))
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
        # Apparently this works only for stock devices, and jailbroken devices due to another reboot binary?
        # You need to delete the file /sbin/reboot which is not present on stock iOS. [https://github.com/libimobiledevice/libimobiledevice/issues/586]
        # Still not working on iOS 10.3.3 iPhone 5S

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

    def listDirectoryWithAFC(self):
        device = AFCShell()
        device.do_ls('.')

    def backup(self):
        device = MobileBackup2()
        device.backup()  # full backup is true by default

    def syslog(self):
        data = Syslog()
        data.watch()

    def pair(self):
        device = LockdownClient()
        paired = device.pair()
        if paired:
            return sys.exit('Device is already paired!')
        else:
            return sys.exit('Device is NOT paired!')

    def diagnostics(self):
        device = DIAGClient()
        print(device.diagnostics('GasGauge'))
        print(device.diagnostics('HDMI'))
        print(device.diagnostics('NAND'))
        print(device.diagnostics('WiFi'))

    def proxy(self):
        # device = installation_proxy()
        # data = device.browse() # Returns tons of data :D
        pass
