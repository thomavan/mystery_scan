import pprint
import time

from zebra_scanner import CoreScanner

pp = pprint.PrettyPrinter(indent=4)
cs = CoreScanner()

@cs.on_scanner_added
def on_scanner_added(scanner):
    print(f"New scanner found: <{scanner.GUID}>")
    # pp.pprint(scanner.__dict__)
    scanner.pull_trigger()

    scanner.fetch_attributes()
    skip_scanner = True
    for id, attribute in scanner.attributes.items():
        if id<10:
            skip_scanner = False
            pp.pprint({
                "id": id,
                "datatype": attribute.datatype,
                "value": attribute.value,
                "permission": attribute.permission
            })
        else:
            # print(f"-DD- Skipping {id}")
            pass
    if scanner.GUID != "":
        print(f"Registering scanner -{scanner.GUID}-")
        @scanner.on_barcode
        def on_barcode(barcode):
            print("Scanned:")
            print(barcode.code, barcode.type)
            print("Sending request ...")
            r = requests.post('https://test.ocelot.test/api/v1/scanned-barcode/', data={ 'key1': scanner.GUID, 'barcode': barcode.code })
            print("Request result : ", r)

@cs.on_scanner_removed
def on_scanner_removed(scanner):
    print("Scanner removed:")
    scanner.release_trigger()
    # pp.pprint(scanner.__dict__)

while True:
    time.sleep(0.1)
    # do nothing while the scanner is reading in continous mode
