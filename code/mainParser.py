from bs4 import BeautifulSoup

# Initialize the File
file =open("../test/testprogramm.xml", "r")
soup = BeautifulSoup("".join(file.readlines()), 'xml')
# Find all Subroutines
central = soup.find_all("o", attrs={"classname": "ftProSubroutineFunction"})
hauptprogramm = central[0]
# Find all objects inside the subroutine
objects = []

# Find all New-Process-Elements
starts = hauptprogramm.find_all("o", attrs={"classname": "ftProProcessStart"})
starts += hauptprogramm.find_all("o", attrs={"classname": "ftProFlowIf"})
starts += hauptprogramm.find_all("o", attrs={"classname": "ftProDataIn"})
starts += hauptprogramm.find_all("o", attrs={"classname": "ftProDataOutDual"})
starts += hauptprogramm.find_all("o", attrs={"classname": "ftProProcessStop"})
starts += hauptprogramm.find_all("o", attrs={"classname": "ftProDataMssg"})
for startEl in starts:
    obj = {"type": startEl.attrs["classname"]} #, "id": startEl.attrs["id"]}
    pins = startEl.find_all("o", attrs={"classname": "ftProObjectPin"})
    pinList = [{"id": x.attrs["id"], "pinid": x.attrs["pinid"], "name": x.attrs["name"], "pinclass": x.attrs["pinclass"]} for x in pins]
    print("ELEMENT", obj["type"])
    for pin in pinList:
        print(" -> PIN", "I" + pin["id"], pin["pinclass"], pin["name"])

wires = hauptprogramm.find_all("o", attrs={"classname": "ftProFlowWire"})
wires += hauptprogramm.find_all("o", attrs={"classname": "ftProDataWire"})
for wireEl in wires:
    pins = wireEl.find_all("o", attrs={"classname": "wxCanvasPin"})
    pointList = [{"id": x.attrs["id"], "name": x.attrs["name"], "resolve": x.attrs["resolveid"], "type": x.attrs["pinclass"]} for x in pins]
    print("WIRE")
    for pin in pointList:
        # if pin["name"] is not "dynamic":
        print("-|-", "I" + pin["id"], "R" + pin["resolve"], pin["type"])
