
from flask import Flask, request
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
import requests
from io import BytesIO
import json


@app.route("/")
def server():
	url = request.args.get('url')
	return json.dumps(face(url))

def face(url):

	# Replace <Subscription Key> with your valid subscription key.
	subscription_key = "c78cd99ab0054b00a9276750f7d94b36"
	assert subscription_key

	# You must use the same region in your REST call as you used to get your
	# subscription keys. For example, if you got your subscription keys from
	# westus, replace "westcentralus" in the URI below with "westus".
	#
	# Free trial subscription keys are generated in the westcentralus region.
	# If you use a free trial subscription key, you shouldn't need to change
	# this region.
	face_api_url = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect'

	# Set image_url to the URL of an image that you want to analyze.
	# image_url = 'https://how-old.net/Images/faces2/main007.jpg'
	image_url = url

	headers = {'Ocp-Apim-Subscription-Key': subscription_key}
	params = {
	    'returnFaceId': 'true',
	    'returnFaceLandmarks': 'false',
	    'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,' +
	    'emotion,hair,makeup,occlusion,accessories,blur,exposure,noise'
	}
	data = {'url': image_url}
	response = requests.post(face_api_url, params=params, headers=headers, json=data)
	faces = response.json()

	return faces

