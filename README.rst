****************
Supported boards
****************

Check https://www.zebra.com/us/en/support-downloads/software/developer-tools/scanner-sdk-for-linux.html

******************
Known issues
******************

MS4717: CMD_DEVICE_SWITCH_HOST_MODE does not work

**********
Installing
**********

It's working on Ubuntu 18.04 with Zebra SDK 4.4, which you can download from https://www.zebra.com/de/de/support-downloads/software/developer-tools/scanner-sdk-for-linux.html
You can easily install zebra_scanner with pip:

.. code-block:: sh

 sudo apt-get install libboost-dev libboost-python-dev libpugixml-dev
 sudo pip3 install pybind11
 sudo pip3 install zebra-scanner


*****************
A minimal example
*****************

.. code-block:: python

 import pprint
 import time
 
 from zebra_scanner import CoreScanner
 
 pp = pprint.PrettyPrinter(indent=4)
 scanners = []
 cs = CoreScanner()
 
 
 @cs.on_scanner_added
 def on_scanner_added(scanner):
     print("New scanner found:")
     pp.pprint(scanner.__dict__)
     scanners.append(scanner)
     scanner.pull_trigger()
 
     scanner.fetch_attributes()
     for id, attribute in scanner.attributes.items():
         if id<10:
             pp.pprint({
                 "id": id,
                 "datatype": attribute.datatype,
                 "value": attribute.value,
                 "permission": attribute.permission
             })
 
     @scanner.on_barcode
     def on_barcode(barcode):
         print("Scanned:")
         print(barcode.code, barcode.type)
 
 @cs.on_scanner_removed
 def on_scanner_removed(scanner):
     print("Scanner removed:")
     scanner.release_trigger()
     scanners.remove(scanner)
     pp.pprint(scanner.__dict__)
 
 while True:
     time.sleep(0.1)
     # do nothing while the scanner is reading in continous mode


*******************
Running the example
*******************

.. code-block:: sh

 ~/Development/zebra-scanner/examples$ python test.py
 New scanner found:
 {   'DoM': '10Mar18',
     'GUID': 'AFF531D4821A3E4BB2127A380DA81FB0',
     'PID': '1900',
     'VID': '05e0',
     'firwmare': 'PAABLS00-005-R05',
     'modelnumber': 'PL-3307-B100R',
     'scannerID': '1',
     'serialnumber': '00000000K10U532B',
     'type': 'SNAPI'}
 {   'datatype': 'F', 'id': 0, 'permission': 7, 'value': True}
 {   'datatype': 'F', 'id': 1, 'permission': 7, 'value': True}
 {   'datatype': 'F', 'id': 2, 'permission': 7, 'value': True}
 {   'datatype': 'F', 'id': 3, 'permission': 7, 'value': True}
 {   'datatype': 'F', 'id': 4, 'permission': 7, 'value': True}
 {   'datatype': 'F', 'id': 5, 'permission': 7, 'value': False}
 {   'datatype': 'F', 'id': 6, 'permission': 7, 'value': True}
 {   'datatype': 'F', 'id': 7, 'permission': 7, 'value': False}
 {   'datatype': 'F', 'id': 8, 'permission': 7, 'value': True}
 {   'datatype': 'F', 'id': 9, 'permission': 7, 'value': False}
 Scanned:
 ('Hello World', '3')
 Scanned:
 ('00140092390052832143', '15')
 Scanned:
 ('31039999993000000072\x1d', '15')
 Scanned:
 ('01540092393881021000017500861331', '15')
 Scanned:
 ('00140092390052832143', '15')
 ^CScanner removed:
 {   'DoM': '10Mar18',
     'GUID': 'AFF531D4821A3E4BB2127A380DA81FB0',
     'PID': '1900',
     'VID': '05e0',
     'firwmare': 'PAABLS00-005-R05',
     'modelnumber': 'PL-3307-B100R',
     'scannerID': '1',
     'serialnumber': '00000000K10U532B',
     'type': 'SNAPI'}

