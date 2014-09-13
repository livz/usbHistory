usbHistory
==========

This tool can gather various pieces of evidence related to USB devices from the Windows registry. It can be used during the investigation of a live Windows machine and will extract details about a drive (manufacturer, product name, version and the unique serial number), when it was used for the first and last time and also whether it was accessed during the current login session or not.

Currently the tool supports only Windows 7, but support for other versions will be added in the future.

Sample output:

    [*] 2 USB devices detected:
    [+] Vendor/Product/Version:  Corsair Padlock_v2 1.12
    [+] Unique S/N:  14061130104893120E87&0
    [+] Friendly name: I:\
    [+] Volume ID (GUID): 52b85489-3932-11e4-840f-080027fcbd50
    [+] Drive letter: I
    [+] This device was used by the current user!
    [+] First used: 2014/09/13 09:54:04.456 UTC
    [+] Last used:  2014/09/13 19:07:48 UTC
    
    [+] Vendor/Product/Version:  UFD_2.0 Silicon-Power4G 1100
    [+] Unique S/N:  1111121400001117&0
    [+] Friendly name: PENDRIVE
    [+] Volume ID (GUID): 29ab6224-10d2-11e3-b1d0-080027fcbd50
    [+] Drive letter: G
    [+] This device was used by the current user!
    [+] First used: 2013/08/29 21:45:07.218 UTC
    [+] Last used:  2014/09/13 17:07:12 UTC


References
----------

 - [Extract USB History](http://cyberinc.co.uk/extract-usb-history/)
 - [Python 2.x _winreg    module](https://docs.python.org/2/library/_winreg.html)
 - [USB History Dump](http://sourceforge.net/projects/usbhistory/) 
 - Harlan Carvey – [Windows Forensic Analysis
   Toolkit](http://www.amazon.com/Windows-Forensic-Analysis-Toolkit-Edition/dp/1597494224)
 - SANS – [Digital Forensics and Incident Response
   Poster](http://digital-forensics.sans.org/blog/2012/06/18/sans-digital-forensics-and-incident-response-poster-released)


