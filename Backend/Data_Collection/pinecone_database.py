import pinecone
import pandas as pd

#from credentials import pinecone_cred

import credentials.pinecone_cred as pinecone_cred
## this is a file to populate the vector database. 

#the_table = pd.read_csv('smaller_feature_table.csv').drop('Unnamed: 0',axis=1)

## make a seperate file to store api keys 
pinecone.init(api_key=pinecone_cred.api_key, environment = pinecone_cred.environment)
index = pinecone.Index('song-image-smaller')
## convert df into dictionary to add it eventually to pinecone

#list_of_lists = the_table.values.tolist()


## restructuring dictionary to fit pinecone. 
def restructure_data_frame(list_of_lists):
    vectors = []
    for row_number in range(len(list_of_lists)):
        dictionary = {}
        dictionary['id'] = list_of_lists[row_number][0]
        dictionary['values'] = list_of_lists[row_number][1:14]
        vectors.append(dictionary)
    return vectors



## This function populates the pine cone database from our song databsae. 
def upsert_batches(list_of_dictionaries,n):      
    # looping till length l 
    for i in range(0, len(list_of_dictionaries), n):  
        chunk = list_of_dictionaries[i:i + n]
        print(chunk)
        #index.upsert(chunk)
        print('done')
    return 
        

"""
TODO: Create a function that will allow us to find the most similar to a given vector. 

"""


#restructured_data = restructure_data_frame(list_of_lists)
#upsert_batches(restructured_data,100)

