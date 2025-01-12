import requests
import itertools
from google.transit import gtfs_realtime_pb2
from google.protobuf.json_format import MessageToJson 
import json

# List of API keys
BUS_API = [
   "82b0450b-205f-491e-9ba1-2cdd76eef126",
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
    
# Create a cycle of API keys to rotate through them
api_key_cycle = itertools.cycle(BUS_API)
api_time_cycle = itertools.cycle(Real_Time_Feeds)

print("Libraries are properly installed!")

def fetch_mta_data():
    for feed_url in Real_Time_Feeds:
        # Get the next API key from the cycle
        api_key = next(api_key_cycle)
        headers = {"x-api-key": api_key}

        try:
            # Make the GET request
            response = requests.get(feed_url, headers=headers)
            response.raise_for_status()  # Check for HTTP errors

            # Print the raw content and headers for debugging
            # print(f"Response Content-Type: {response.headers.get('Content-Type')}")
            # print(f"Raw Response Content (First 500 bytes): {response.content[:500]}")
            
            # Deserialize the content using FeedMessage
            feed = gtfs_realtime_pb2.FeedMessage()
            feed.ParseFromString(response.content)  # Parse raw protocol buffer data
            data = MessageToJson(feed)  # Convert to JSON string
            
            # Return parsed JSON as a Python dictionary
            return json.loads(data)

        except requests.exceptions.RequestException as e:
            print(f"Error with API key {api_key}: {e}")
            # Try the next API key if an error occurs
            continue
        except Exception as e:
            print(f"Error parsing response: {e}")
            print("Raw response (for debugging):", response.content[:500])
            continue

    # If all keys fail
    print("All API keys failed. Please check your keys or internet connection.")
    return None



# def fetch_mta_data():
    
#     for feed_url in Real_Time_Feeds :
#         # Get the next API key from the cycle
#         api_key = next(api_key_cycle)
#         headers = {"x-api-key": api_key}

#         try:
#             # Make the GET request
#             response = requests.get(feed_url, headers=headers)
#             response.raise_for_status()  # Check for HTTP errors

#             #error in .FeedMessage(), must be changed
#             #line 47 is not working correctly because of .FeedMessage()
#             feed = gtfs_realtime_pb2.FeedMessage()
#             feed.ParseFromString(response.content)
#             data = MessageToJson(feed)
#             return json.loads(data)

#         except requests.exceptions.RequestException as e:
#             print(f"Error with API key {api_key}: {e}")
#             # Try the next API key if an error occurs
#             continue

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


# Jan 11,2025