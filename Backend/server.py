import jinja2

from markupsafe import escape
from flask import Flask,render_template, request , jsonify 
import model_flow
import firebase_admin
from firebase_admin import credentials,storage 
import numpy as np 
from PIL import Image
from io import BytesIO
import json

## accessing fire base and the bucket 
cred = firebase_admin.credentials.Certificate("Backend/credentials/key.json")
firebase_app = firebase_admin.initialize_app(cred,{"storageBucket":"string-theory-f2ce4.appspot.com"})
bucket = storage.bucket()





# goes blob -> array -> image 

 

app = Flask(__name__)


## convert api route
## the function will return a list [song preview, and track link]
## it will take in the url of the image and input it into the model.

@app.route("/pipeline", methods=['POST'])
def pipeline():
    print("soi")
    print(request.data)
    # Decode the bytes to a string
    response_str = request.data.decode('utf-8')
    # Parse the JSON string
    response_json = json.loads(response_str)
    image_path = response_json.get('url')
    print("john")
    result_data = {'image_path': image_path}
    
    # Use result_data in the response, instead of a set
    print(json.dumps(result_data))
    
    song_vector = model_flow.image_to_emotion(image_path)
    nearest_song = model_flow.nearest_song(song_vector)
    
    return jsonify({"data": model_flow.spotify_demo(nearest_song)})






if __name__ =="__main__":
    app.run(debug=True)



