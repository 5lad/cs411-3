import os
import pickle
from flask import Flask, request, redirect, url_for
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
import requests
from io import BytesIO
import json
from ezoptic_matching_algo_RUN import match_face_glasses
from rauth import OAuth2Service
from rauth import OAuth1Service
from walmart import walmart
from flask_pymongo import PyMongo

app.config['MONGO_DBNAME'] = 'cs411'
app.config['MONGO_URI'] = 'mongodb://group3:bucs411@ds117711.mlab.com:17711/cs411'
mongo = PyMongo(app)
# save = [FACE_COLS, FACE_DF, FACE_CLF]
with open("save.pickle", 'rb') as f:
	save = pickle.load(f)

# UPLOAD_FOLDER = "uploads"
# ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# def allowed_file(filename):
# 	return '.' in filename and \
# 		   filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def face(url):

	# Replace <Subscription Key> with your valid subscription key.
	subscription_key = "d6dbd454b75d44e098550af6845fc347"
	assert subscription_key

	# You must use the same region in your REST call as you used to get your
	# subscription keys. For example, if you got your subscription keys from
	# westus, replace "westcentralus" in the URI below with "westus".
	#
	# Free trial subscription keys are generated in the westcentralus region.
	# If you use a free trial subscription key, you shouldn't need to change
	# this region.
	face_api_url = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect'


	image_url = url

	headers = {'Ocp-Apim-Subscription-Key': subscription_key, 'Content-Type':'application/json'}
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

@app.route("/", methods=['GET'])
def server():
	url = request.args.get('url')
	userID = request.args.get('userID')

	if url == None:
		return ""

	ret = face(url)
	glass = walmart(match_face_glasses(url, save[0], save[1], save[2]))
	ret.append(glass)

	history = mongo.db.history
	history.update_one({'userID': userID}, {'$push': {'glasses': glass}}, True)
	return json.dumps(ret)

@app.route("/history", methods=['GET'])
def history():
	userID = request.args.get('userID')
	history = mongo.db.history
	ret = history.find({'userID': userID})
	try:
		print("trys")
		ret = ret[0]['glasses']
	except Exception as e:
		ret = {}

	return json.dumps(ret)
	# return json.dumps(ret[0]) if ret.count() > 0 else []
	# return json.dumps(ret)

# class OAuthSignIn(object):
# 	providers = None

# 	def __init__(self, provider_name):
# 		self.provider_name = provider_name
# 		credentials = app.config['OAUTH_CREDENTIALS'][provider_name]
# 		self.consumer_id = credentials['id']
# 		self.consumer_secret = credentials['secret']

# 	def authorize(self):
# 		pass

# 	def callback(self):
# 		pass

# 	def get_callback_url(self):
# 		return url_for('oauth_callback', provider=self.provider_name, _external=True)

# 	@classmethod
# 	def get_provider(self, provider_name):
# 		if self.providers is None:
# 			self.providers = {}
# 			for provider_class in self.__subclasses__():
# 				provider = provider_class()
# 				self.providers[provider.provider_name] = provider
# 		return self.providers[provider_name]
		
# app.config['OAUTH_CREDENTIALS'] = {
# 	'facebook': {
# 		'id': '771932186487787',
# 		'secret': '0cd30f5aadbc73090d623eef2cb00f67'
# 	},
# 	'twitter': {
# 		'id': 'Rkh2TJUkNVRE1NBtnHZJMhEYA',
# 		'secret': 'Phz5NVZsYxrt6uqkxUDoN9wCmoOSjNqbiG2npRhxS3PMXwWvPM'
# 	}
# }
# class FacebookSignIn(OAuthSignIn):
# 	def __init__(self):
# 		print('init fb')
# 		super(FacebookSignIn, self).__init__('facebook')
# 		self.service = OAuth2Service(
# 			name='facebook',
#             client_id=self.consumer_id,
#             client_secret=self.consumer_secret,
# 			authorize_url='https://graph.facebook.com/oauth/authorize',           
# 			access_token_url='https://graph.facebook.com/oauth/access_token',
# 			base_url='https://graph.facebook.com/'
# 		)
# 	def authorize(self):
# 		print('auth fb')
# 		return redirect(self.service.get_authorize_url(
# 			scope='email',
# 			response_type='code',
# 			redirect_uri=self.get_callback_url())
# 		)

# 	def callback(self):
# 		print('callback')
# 		def decode_json(payload):
# 			return json.loads(payload.decode('utf-8'))

# 		if 'code' not in request.args:
# 			return None, None, None
# 		oauth_session = self.service.get_auth_session(
# 			data={'code': request.args['code'],
# 				  'grant_type': 'authorization_code',
# 				  'redirect_uri': self.get_callback_url()},
# 			decoder=decode_json
# 		)
# 		me = oauth_session.get('me').json()
# 		print(me)
# 		return (
# 			'facebook$' + me['id'],
# 			me.get('email').split('@')[0],  # Facebook does not provide
# 											# username, so the email's user
# 											# is used instead
# 			me.get('email')
# 		)

# class TwitterSignIn(OAuthSignIn):
# 	def __init__(self):
# 		super(TwitterSignIn, self).__init__('twitter')
# 		self.service = OAuth1Service(
# 			name='twitter',
# 			consumer_key=self.consumer_id,
# 			consumer_secret=self.consumer_secret,
# 			request_token_url='https://api.twitter.com/oauth/request_token',
# 			authorize_url='https://api.twitter.com/oauth/authorize',
# 			access_token_url='https://api.twitter.com/oauth/access_token',
# 			base_url='https://api.twitter.com/1.1/'
# 		)

# 	def authorize(self):
# 		request_token = self.service.get_request_token(
# 			params={'oauth_callback': self.get_callback_url()}
# 		)
# 		session['request_token'] = request_token
# 		return redirect(self.service.get_authorize_url(request_token[0]))

# 	def callback(self):
# 		request_token = session.pop('request_token')
# 		if 'oauth_verifier' not in request.args:
# 			return None, None, None
# 		oauth_session = self.service.get_auth_session(
# 			request_token[0],
# 			request_token[1],
# 			data={'oauth_verifier': request.args['oauth_verifier']}
# 		)
# 		me = oauth_session.get('account/verify_credentials.json').json()
# 		social_id = 'twitter$' + str(me.get('id'))
# 		username = me.get('screen_name')
# 		return social_id, username, None   # Twitter does not provide email


# @app.route('/authorize/<provider>')
# def oauth_authorize(provider):
# 	# if not current_user.is_anonymous():
# 		# return redirect(url_for('index'))
# 	oauth = OAuthSignIn.get_provider(provider)
# 	return oauth.authorize()

# @app.route('/callback/<provider>')
# def oauth_callback(provider):
# 	# if not current_user.is_anonymous():
# 	# 	return redirect(url_for('index'))
# 	oauth = OAuthSignIn.get_provider(provider)
# 	social_id, username, email = oauth.callback()
# 	if social_id is None:
# 		flash('Authentication failed.')
# 		return redirect(url_for('index'))
# 	user = User.query.filter_by(social_id=social_id).first()
# 	if not user:
# 		user = User(social_id=social_id, nickname=username, email=email)
# 		db.session.add(user)
# 		db.session.commit()
# 	login_user(user, True)
# 	return redirect(url_for('index'))