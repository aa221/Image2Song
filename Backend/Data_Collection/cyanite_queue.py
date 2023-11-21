
from python_graphql_client import GraphqlClient
import pandas as pd
from requests.auth import AuthBase
import json
import multiprocessing
import time
from multiprocessing import Process
import numpy as np
## clean this up.
class BearerAuth(AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["Authorization"] = f"Bearer {self.token}"
        return r


# Instantiate the client with an endpoint.
client = GraphqlClient(endpoint="https://api.cyanite.ai/graphql")



token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiSW50ZWdyYXRpb25BY2Nlc3NUb2tlbiIsInZlcnNpb24iOiIxLjAiLCJpbnRlZ3JhdGlvbklkIjo0MzYsInVzZXJJZCI6MTkxMjUsImFjY2Vzc1Rva2VuU2VjcmV0IjoiODNlNGY1M2QxZmNkNmNjMzk0YzZjYzYxN2UwZjMzNmE4NTAxNzQ1ZDk2ODZlMjczYzIxMTZmNzlmZDhhMDBlZCIsImlhdCI6MTY3NDA5ODE1N30.gUE-BzTVJ3g73otcsU5NFO40OoMQ-0dDlPYbcIoMfTg"
auth = BearerAuth(token)


## A lot of the songs are not on cyanite. Below is a function to iterate through the track data frame and enque them

def enqueue(df):
    for id in df['id']:
        try: 
            query= """
                    mutation SpotifyTrackEnqueueMutation($input: SpotifyTrackEnqueueInput!) {
        spotifyTrackEnqueue(input: $input) {
            __typename
            ... on SpotifyTrackEnqueueSuccess {
            enqueuedSpotifyTrack {
                id
            }
            }
            ... on Error {
            message
            }
        }
        }


            """
            
            variables = { "input": { "spotifyTrackId": id} }
            variables = json.dumps(variables)
            print(variables)
            

            data = client.execute(query=query, variables=variables,auth=auth)

            print(data)
        except: 
            continue

    return 

tracks = pd.read_csv('tracks.csv')


def task(df):
    enqueue(df)


def split_tables(table,number_of_splits=8):
    the_tables = [table for table in np.array_split(table, number_of_splits)]
    return the_tables



## Here I use multi processing with about 100 processes 
## What this means is that I will be enqueing tracks using 100 different processors 
## I used 100 processors so that I can process these songs much faster than if I had a singular for loop
## These are 100 for loops at the same time. 
if __name__ == "__main__":
    print("start")
 
    # Creates 8 processes
    processes = [multiprocessing.Process(target=task, args=(split_tables(tracks,100)[x],)) for x in range(0,100)]
    [p.start() for p in processes]
    result = [p.join() for p in processes]
    print(result)
 
  

