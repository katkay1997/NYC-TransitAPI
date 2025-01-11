import requests
import itertools
from google.transit import gtfs_realtime_pb2
from google.protobuf.json_format import MessageToJson 
import json

# List of API keys
BUS_API = [
    "https://gtfsrt.prod.obanyc.com/tripUpdates?key=82b0450b-205f-491e-9ba1-2cdd76eef126",

    "https://gtfsrt.prod.obanyc.com/vehiclePositions?key=82b0450b-205f-491e-9ba1-2cdd76eef126",

    #MTA Bus Time system
]

Real_Time_Feeds = [ 
     #ACE trains
    "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-ace ",
    #12347 trains
    "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs" ,
    #j and z train
    "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-jz ",
   #b d f trains
    "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-bdfm"  
]
    
    


#I need to figure out how to add Real Time Feeds to Python code
# Create a cycle of API keys to rotate through them
api_key_cycle = itertools.cycle(BUS_API)
api_time_cycle = itertools.cycle(Real_Time_Feeds)

def fetch_mta_data():
    for attempt in Real_Time_Feeds:
        headers = {"x-api-key": attempt}

        try:
            # Placeholder for actual logic
            pass
        except Exception as e:
            print(f"Error with API time {attempt}: {e}")
            continue

    for attempt in range(len(BUS_API)):
        # Get the next API key from the cycle
        api_key = next(api_key_cycle)
        headers = {"x-api-key": api_key}

        try:
            # Make the GET request
            response = requests.get(Real_Time_Feeds, headers=headers)
            response.raise_for_status()  # Check for HTTP errors

            # Parse JSON response (if Protobuf, you'd decode here)
            feed = gtfs_realtime_pb2.FeedMessage()
            feed.ParseFromString(response.content)
            data = response.json()
            return data

        except requests.exceptions.RequestException as e:
            print(f"Error with API key {api_key}: {e}")
            # Try the next API key if an error occurs
            continue

    # If all keys fail
    print("All API keys failed. Please check your keys or internet connection.")
    return None

def display_data(data):
    # Example: Print the first few entries (adjust based on actual API response)
    if data:
        print("Sample Data from MTA API:")
        print(json.dumps(data, indent=2))  # Pretty-print JSON
    else:
        print("No data to display.")

if __name__ == "__main__":
    print("Fetching MTA data...")
    mta_data = fetch_mta_data()
    display_data(mta_data)


