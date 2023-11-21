import replicate
from Data_Collection import pinecone_database
from credentials import pinecone_cred
import authorized
from credentials import replicate_cred
from PIL import Image
from io import BytesIO
import requests
import base64
import json


sp = authorized.sp

# This file dictates the overall flow of the application
# The model will take in an image and output the probabilities of the image. 
# We'll then use these probabilities and map them to the closest vector in the pinecone database. 

## this function takes an image  and queries the LLAVA model to retrive the emotions associated to the image.
def image_to_emotion(image_path):
    ## image path is the URL of the image that is retrieved from fire base. 
    response = requests.get(image_path)
    prompt = 'Assign a probability for each of these emotions based on what the image evokes, be very detailed and accurate, if you are unsure about a specific emotion set it to 0: aggressive, calm , chilled, dark, energetic, epic, happy, romantic, sad, scary, sexy, ethereal, uplifting. Only include their respective values.'
    image = response.content
    print("quick")
    image = base64.b64encode(image).decode('utf-8')
    print("not")
    image = 'data:image/jpeg;base64,'+image
    print("tit")


    output = replicate.run(
        "yorickvp/llava-13b:2facb4a474a0462c15041b78b1ad70952ea46b5ec6ad29583c0b29dbd4249591",
        input={"image": image,"prompt":prompt}
    )

    # The yorickvp/llava-13b model can stream output as it's running.
    # The predict method returns an iterator, and you can iterate over that output.
    ## a list split up into words. 
    ## for example ' a picture of a man and a dog' ==> ['a','picture', 'of' ...]
    stored_output = []
    for item in output:
        # https://replicate.com/yorickvp/llava-13b/versions/2facb4a474a0462c15041b78b1ad70952ea46b5ec6ad29583c0b29dbd4249591/api#output-schema
        stored_output.append(item)
    try:
        ## repalce \n from every item
        stored_output = [item.replace('\n', '') for item in stored_output]

        ## extract only the numerical outputs. 
        numerical_output =  [float(item) for item in stored_output if ':' not in item and all(char.isdigit() or char=='.' for char in item)]

    except Exception:
        raise TypeError("Try Again!")



    ## check if there are exactly 13 numbers in the list. If not return an error to the client. 

    if len(numerical_output)!=13:
        raise  TypeError("Try a Different Image!")


    return numerical_output


# ## takes in the emotion of the image given above and returns the song that is closest to it with respect to emotion.
# ## It queries the pinecone database in search of the nearest song.  

def nearest_song(given_song_vector):
    the_song = pinecone_database.index.query(vector=given_song_vector,
    top_k=1,
    include_values=False)
    return  the_song



## This function takes the ID of the nearest song above and returns a link 
## to listen to the preview of the song itself. 
## we want to return  both track preview and track link
## because sometimes preview is not available
## in which case we will just display the song. 

def spotify_demo(song_vector):
    id = song_vector['matches'][0]['id']
    track = sp.track(id)
    track_preview= track['preview_url']
    track_link = track['external_urls']["spotify"]
    return [track_preview,track_link] ## returns the track link and the track preview
    
    






