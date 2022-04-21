import json

WRITE_TABLE = True
PAYMENTS_EXTENSION = "/Payments"
BORDEREAU_EXTENSION = "/Bordereau"
OUTPUT_SECTION = "C:/Users/david.watson/Documents/Clients/ARAG/0.2 Analysis/Generated files"

f = open("./client_information.json")
CLIENT_INFORMATION = json.load(f)["client_information"]
f.close()
