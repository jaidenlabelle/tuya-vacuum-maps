"""Script to download the current realtime map from a vacuum using the Tuya Cloud API."""

import os

import requests
from dotenv import load_dotenv
from tuya_vacuum.tuya import TuyaCloudAPI

# Load environment variables
load_dotenv()

# Get environment variables
SERVER = os.environ.get("SERVER", "https://openapi.tuyaus.com")
CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
DEVICE_ID = os.environ["DEVICE_ID"]


def main():
    """Download the current realtime map from a vacuum using the Tuya Cloud API."""

    endpoint = f"/v1.0/users/sweepers/file/{DEVICE_ID}/realtime-map"

    tuya = TuyaCloudAPI(SERVER, CLIENT_ID, CLIENT_SECRET)
    response = tuya.request("GET", endpoint)

    maps = response["result"]

    for vacuum_map in maps:
        print(vacuum_map)

        map_url = vacuum_map["map_url"]
        map_data = requests.get(map_url, timeout=2.5).content
        map_type = vacuum_map["map_type"]

        if map_type == 1:
            filename = "path.bin"
        elif map_type == 0:
            filename = "layout.bin"
        else:
            filename = f"map_type_{map_type}.bin"
            print(f"Unknown Map Type: {map_type}, saving raw data to {filename}")

        with open(filename, "wb") as file:
            file.write(map_data)


if __name__ == "__main__":
    main()
