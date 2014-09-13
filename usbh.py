import os
import _winreg 

from datetime import datetime
from logger import *

'''
	Converts Windows Date/Time stamps to Unix Date/Time
	windate - 100 nanosecond intervals in windows timestamp
'''
def convert_win_to_unix(windate):
	delta = 11644473600 # number of seconds between 1/1/1601 and 1/1/1970
	no_nano = windate/10000000
	unix = no_nano - delta
	return unix
	
if __name__ == "__main__":
	usbstor = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, 
		r"SYSTEM\CurrentControlSet\Enum\USBSTOR", 0, _winreg.KEY_READ)
	devNum = _winreg.QueryInfoKey(usbstor)[0]
	logInfo("%d USB devices detected:" % devNum)
	
	for i in range(devNum):
		# Get Vendor, Product and Version
		devstr = _winreg.EnumKey(usbstor, i)
		info = devstr.split('&')
		logOk("Vendor/Product/Version:  %s %s %s" % 
			(info[1][4:], info[2][5:], info[3][4:]))
			
		# Get unique serial number
		dev = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, 
			r"SYSTEM\CurrentControlSet\Enum\USBSTOR\\" + devstr, 0, 
			_winreg.KEY_READ)
		sn = _winreg.EnumKey(dev, 0)
		logOk("Unique S/N:  %s" % sn)
		
		# Get device "friendly" name
		portableDevs = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, 
			r"SOFTWARE\Microsoft\Windows Portable Devices\Devices", 0, _winreg.KEY_READ)
		for j in range(_winreg.QueryInfoKey(portableDevs)[0]):
			pdevStr = _winreg.EnumKey(portableDevs, j)
			if sn in pdevStr:
				pdev = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, 
					r"SOFTWARE\Microsoft\Windows Portable Devices\Devices\\" + pdevStr,
					0, _winreg.KEY_READ)
				logOk("Friendly name: %s " % _winreg.QueryValueEx(pdev, "FriendlyName")[0])
		
		# Get drive letter and GUID from MountedDevices
		guid = ""
		mountedDevs = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, 
			r"SYSTEM\MountedDevices", 0, _winreg.KEY_READ)
		for j in range(_winreg.QueryInfoKey(mountedDevs)[1]):
			name = _winreg.EnumValue(mountedDevs, j)[0]
			data = _winreg.EnumValue(mountedDevs, j)[1].replace("\x00", "")
			if sn in data:
				if "DosDevices" in name:
					logOk("Drive letter: %s " % name[12])
				if "Volume" in name:
					guid = name[10:].strip("{}")
					logOk("Volume ID (GUID): %s " % guid)

		# Check if the current user mounted the USB drive
		# Volume GUID will exist within NTUSER.dat in:
		# \Software\Microsoft\Windows\CurrentVersion\Explorer\MountPoints2
		mountPoints = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER,
			r"Software\Microsoft\Windows\CurrentVersion\Explorer\MountPoints2", 
			0, _winreg.KEY_READ)
		for j in range(_winreg.QueryInfoKey(mountPoints)[0]):
			if guid in _winreg.EnumKey(mountPoints, j):
				logOk("This device was used by the current user!")

		# Get time when device was first used
		with open(os.environ["WINDIR"] + "\\inf\\setupapi.dev.log") as f:
			searchlines = f.readlines()
			for i, line in enumerate(searchlines):
				if sn in line: 
					logOk("First used: %s UTC" % " ".join(searchlines[i+1].split()[3:]))
					break
		
		# When was it last time connected
		usb = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, 
			r"SYSTEM\CurrentControlSet\Enum\USB", 0, _winreg.KEY_READ)
		for j in range(_winreg.QueryInfoKey(usb)[0]):
			vidStr = _winreg.EnumKey(usb, j)
			usbsn = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, 
				r"SYSTEM\CurrentControlSet\Enum\USB\\" + vidStr, 0, _winreg.KEY_READ)

			if _winreg.EnumKey(usbsn, 0) in sn:		
				usbsnkey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, 
					r"SYSTEM\CurrentControlSet\Enum\USB\\" + vidStr + "\\" +
					_winreg.EnumKey(usbsn, 0), 0, _winreg.KEY_READ)
				# Last modified time, 100s of nanoseconds since Jan 1, 1601
				t = _winreg.QueryInfoKey(usbsnkey)[2]
				date_format = '%Y/%m/%d %H:%M:%S UTC' 
				logOk("Last used:  %s" % 
					datetime.fromtimestamp(int(convert_win_to_unix(t))).strftime(date_format))
			
		print "\r"
	
