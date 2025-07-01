import os
from acdh_baserow_pyutils import BaseRowClient

BASEROW_URL = "https://baserow.acdh-dev.oeaw.ac.at/api/"

# store baserow credentials as ENV-Variables
BASEROW_USER = os.environ.get("BASEROW_USER")
BASEROW_PW = os.environ.get("BASEROW_PW")
BASEROW_TOKEN = os.environ.get("BASEROW_TOKEN") # you need to create a token via baserow
DATABASE_ID = "594" # you can get this ID from Baserow

# initialize the client
br_client = BaseRowClient(BASEROW_USER, BASEROW_PW, BASEROW_TOKEN, br_base_url=BASEROW_URL)

# writes all tables from Database as json.files into a folder 'out' (the folder needs to exist!) and returns a list of the file names
files = br_client.dump_tables_as_json(DATABASE_ID, folder_name='out')
print(files)
# ['out/place.json', 'out/person.json', 'out/profession.json']