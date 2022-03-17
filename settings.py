import json

WRITE_TABLE = True
PAYMENTS_EXTENSION = "/Payments"
BORDEREAU_EXTENSION = "/Bordereau"

f = open("./client_information.json")
CLIENT_INFORMATION = json.load(f)["client_information"]
f.close()

EXAMPLE_NAME = "Laureau"
