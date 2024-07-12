import json

# Reads the database
def read(dbpath: str) -> list:
    with open(dbpath, "r") as database:
        data = json.load(database)
    return data

# Writes to database
def write(dbpath: str, data: list) -> str:
    print(data)
    try:
        with open(dbpath, "w") as database:
            json.dump(data, database)
        return f"Data scuessfully written to {dbpath}"
    except:
        return f"Failed to write the data to {dbpath}"
