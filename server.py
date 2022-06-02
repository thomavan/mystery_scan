import pprint
import time
import requests

from zebra_scanner import CoreScanner

pp = pprint.PrettyPrinter(indent=4)
cs = CoreScanner()

scanners = []
scanners.append("Les scanners")

@cs.on_scanner_added
def on_scanner_added(scanner):
    # print(f"New scanner found: GUID: <{scanner.GUID}> / Serial: <{scanner.serialnumber}>")
    #pp.pprint(dir(scanner.attributes))

    scanner.pull_trigger()

    scanner.fetch_attributes()
    skip_scanner = True
    scanners.append(scanner.serialnumber)
    for x in scanners:
    	print(x)
    #scanners[int(scanner.scannerID)] = scanner.serialnumber
    for id, attribute in scanner.attributes.items():
        if id<10:
            skip_scanner = False
             # pp.pprint({
                # "id": id,
                # "datatype": attribute.datatype,
                # "value": attribute.value,
                # "permission": attribute.permission
            # })
        else:
            # print(f"-DD- Skipping {id}")
            pass
    if scanner.GUID != "" or scanner.GUID == "" :
        print(f"Registering scanner ID: <{scanner.scannerID}> / scanner GUID: <{scanner.GUID}> / Serial: <{scanner.serialnumber}>")
        @scanner.on_barcode
        def on_barcode(barcode):
            print(f"Scanned by : Serial: <{scanner.serialnumber}>")
            print(barcode.code)
            try:
                print("Sending request ...")
                r = requests.post('https://app.asnco.eu/api/v1/scanned-barcode/', data={ 'scanner': scanner.GUID, 'barcode': barcode.code })
                print("Request response : ", r.status_code)
                print("Request result : ", r.json()[0])
                print("Request scanner : ", r.json()[1])
                scannerId = scanners.index(r.json()[1])
                print("Scanner id : ", scannerId)
                if r.status_code == 200:
                	print("Success")
                	scanner.scan_success(str(scannerId))
                elif r.json()[0] == "Error: barcode deleted":
                	print("Barcode deleted")
                	scanner.scan_warning(str(scannerId))
                else:
                	print("Failed")
                	scanner.scan_error(str(scannerId))
            except:
                print("Request error - Unable to send request")
                #print("Better luck next year")
                scanner.scan_error(str(scannerId))

@cs.on_scanner_removed
def on_scanner_removed(scanner):
    print("Scanner removed:")
    scanner.release_trigger()
    # pp.pprint(scanner.__dict__)

while True:
    time.sleep(0.1)
    # do nothing while the scanner is reading in continous mode
