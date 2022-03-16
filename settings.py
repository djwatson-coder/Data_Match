import json

WRITE_TABLE = True
PDF_EXTENSION = "/Payments"

f = open("./client_information.json")
CLIENT_INFORMATION = json.load(f)["client_information"]
f.close()

EXAMPLE_NAME = "Laureau"
