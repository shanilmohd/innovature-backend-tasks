
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import uuid 
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)
#configuration
app.config['SECRET_KEY'] ="41129EFF630CFBB48E92DA7101AD0A57A6E65590123B4956E881C54A5AE448C4"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///userdata.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
app.app_context().push()


class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	public_id = db.Column(db.String(50), unique = True)
	name = db.Column(db.String(100))
	email = db.Column(db.String(70), unique = True)
	password = db.Column(db.String(80))




# verifying the JWT
def token_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		token = None
		if 'access-token' in request.headers:
			token = request.headers['access-token']
		if not token:
			return jsonify({'message' : 'Token is missing !!'}), 401
		try:
			data = jwt.decode(token, app.config['SECRET_KEY'])
			current_user = User.query.filter_by(public_id = data['public_id']).first()
		except:
			return jsonify({
				'message' : 'Token is invalid !!'
			}), 401
		return f(current_user, *args, **kwargs)

	return decorated

#Routes
@app.route('/getuser', methods =['GET'])
@token_required
def get_all_users(current_user):
	users = User.query.all()
	output = []
	for user in users:
		output.append({
			'public_id': user.public_id,
			'name' : user.name,
			'email' : user.email
		})

	return jsonify({'users': output})
#token-refresh
@app.route("/refresh", methods=["POST"])
@token_required
def refresh_token(current_user):
    try:
        decoded_token = jwt.decode(request.headers['access-token'], app.config['SECRET_KEY'], algorithms=['HS256'])
        if datetime.utcnow() < datetime.utcfromtimestamp(decoded_token['exp']):
            new_token = jwt.encode({
                'public_id': current_user.public_id,
                'exp': datetime.utcnow() + timedelta(minutes=30)
            }, app.config['SECRET_KEY'])
            return jsonify({'token': new_token.decode('UTF-8')}), 200
        else:
            return jsonify({'message': 'Token has expired'}), 401
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401

#login
@app.route('/login', methods =['POST'])
def login():
	auth = request.form
	if not auth or not auth.get('email') or not auth.get('password'):
		return make_response(
			'Could not verify',
			401,
			{'WWW-Authenticate' : 'Basic realm ="Login required !!"'}
		)
	user = User.query.filter_by(email = auth.get('email')).first()
	#user donot exist
	if not user:
		return make_response(
			'Could not verify',
			401,
			{'WWW-Authenticate' : 'Basic realm ="User does not exist !!"'}
		)

	if check_password_hash(user.password, auth.get('password')):
		token = jwt.encode({
			'public_id': user.public_id,
			'exp' : datetime.utcnow() + timedelta(minutes = 30)
		}, app.config['SECRET_KEY'])
		return make_response(jsonify({'token' : token.decode('UTF-8')}), 201)
	return make_response(
		'Could not verify',
		403,
		{'WWW-Authenticate' : 'Basic realm ="Wrong Password !!"'}
	)

#signup
@app.route('/signup', methods =['POST'])
def signup():
	data = request.form
	name, email = data.get('name'), data.get('email')
	password = data.get('password')
	user = User.query.filter_by(email = email).first()
	if not user:
		user = User(
			public_id = str(uuid.uuid4()),
			name = name,
			email = email,
			password = generate_password_hash(password)
		)
		db.session.add(user)
		db.session.commit()

		return make_response('Successfully registered.', 201)
	else:
		return make_response('User already exists. Please Log in.', 202)

if __name__ == "__main__":
	app.run(debug = True,port=10000)






