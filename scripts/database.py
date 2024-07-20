import json, os

from scripts import crypt 

def read(dbpath: str) -> dict:
    if os.path.exists(dbpath) != True:
        print(f'{dbpath} does not exist')
        return None
    
    with open(dbpath, "r") as database:
        data = json.load(database)
        return data


def write(dbpath: str, data: dict) -> str:
    try:
        with open(dbpath, "w") as database:
            database.seek(0)  
            json.dump(data, database)
            database.truncate() 
        print(f"Data scuessfully written to {dbpath}")
    except Exception as e:
        print(f"Failed to write the data to {dbpath}: {e}")
