<<<<<<< HEAD
import pprint
import time
import requests

from zebra_scanner import CoreScanner

pp = pprint.PrettyPrinter(indent=4)
cs = CoreScanner()

# Scanners array: list all scanners
scanners = []
scanners.append("Les scanners")

@cs.on_scanner_added
def on_scanner_added(scanner):
    # Get scanner attribute
    scanner.pull_trigger()
    scanner.fetch_attributes()
    skip_scanner = True

    # Add scanner serial number to scanners array
    scanners.append(scanner.serialnumber)
    for x in scanners:
    	print(x)

    for id, attribute in scanner.attributes.items():
        if id<10:
            skip_scanner = False
        else:
            pass

    # if scanner is not a base / is a capture device
    if scanner.GUID != "" or scanner.GUID == "" :
        # display scanner info on screen
        print(f"Registering scanner ID: <{scanner.scannerID}> / scanner GUID: <{scanner.GUID}> / Serial: <{scanner.serialnumber}>")
        @scanner.on_barcode
        def on_barcode(barcode):
            # scanned by
            print(f"Scanned by : Serial: <{scanner.serialnumber}>")
            print(barcode.code)

            # we send a request to API
            try:
                print("Sending request ...")

                # sending request with scanner guid and barcode scanned
                r = requests.post('https://app.asnco.eu/api/v1/scanned-barcode/', data={ 'scanner': scanner.GUID, 'barcode': barcode.code })

                # print response from API
                print("Request response : ", r.status_code)
                print("Request result : ", r.json()[0])
                print("Request scanner : ", r.json()[1])

                # get scanner id that has scanned
                scannerId = scanners.index(r.json()[1])
                print("Scanner id : ", scannerId)

                if r.status_code == 200:
                    # if success, emit success sound and color
                	print("Success")
                	scanner.scan_success(str(scannerId))
                elif r.json()[0] == "Error: barcode deleted":
                    # if barcode is cancelled, emit warning sound and color
                	print("Barcode deleted")
                	scanner.scan_warning(str(scannerId))
                elif r.json()[0] == "Error: barcode already scanned":
                    # if barcode is cancelled, emit warning sound and color
                	print("Barcode already scanned")
                	scanner.scan_long_error(str(scannerId))
                else:
                    # if fail, emit error sound and color
                	print("Failed")
                	scanner.scan_error(str(scannerId))
            except:
                # if error while sending request
                print("Request error - Unable to send request")
                
                # emit error sound and color
                scanner.scan_error(str(scannerId))

# when a scanne ris removed/unplugged
@cs.on_scanner_removed
def on_scanner_removed(scanner):
    print("Scanner removed:")
    scanner.release_trigger()

while True:
    time.sleep(0.1)
    # do nothing while the scanner is reading in continous mode
=======
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
>>>>>>> 8cf17c635484f486e2b554cf9910d28b699d310d
