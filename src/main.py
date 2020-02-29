"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from models import db, Users, datarecord
from flask_jwt_simple import JWTManager, jwt_required, create_jwt

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)

app.config['JWT_SECRET_KEY'] = 'dfsh3289349yhoelqwru9g'
jwt = JWTManager(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def home():
    return "<div style='text-align: center; background-color: orange'><h1>Backend running...</h1><br/><h3>Welcome back samir</h3><img src='https://media.gettyimages.com/photos/woman-sitting-by-washing-machine-picture-id117852649?s=2048x2048' width='80%' /></div>"

@app.route('/users', methods=['GET'])
def handle_users():

    if request.method == 'GET':
        users = Users.query.all()

        if not users:
            return jsonify({'msg':'User not found'}), 404

        return jsonify( [x.serialize() for x in users] ), 200

    return "Invalid Method", 404


@app.route('/login', methods=['POST'])
def handle_login():

    body = request.get_json()

    user = Users.query.filter_by(email=body['email'], password=sha256(body['password'])).first()

    if not user:
        return 'User not found', 404

    return jsonify({
              'token': create_jwt(identity=1),
              'id': user.id,
              'email': user.email,
              'firstname': user.firstname,
              'lastname': user.lastname,
              'avatar': user.avatar,
              'wallet': user.wallet
              })

@app.route('/register', methods=['POST'])
def handle_register():

    body = request.get_json()

    if body is None:
        raise APIException("You need to specify the request body as a json object", status_code=400)
    if 'firstname' not in body and 'lastname' not in body:
        raise APIException("You need to specify the first name and last name", status_code=400)
    if 'password' not in body and 'email' not in body:
        raise APIException("You need to specify the password and email", status_code=400)
    if 'firstname' not in body:
        raise APIException('You need to specify the first name', status_code=400)
    if 'lastname' not in body:
        raise APIException('You need to specify the last name', status_code=400)
    if 'password' not in body:
        raise APIException('You need to specify the password', status_code=400)
    if 'email' not in body:
        raise APIException('You need to specify the email', status_code=400)



    db.session.add(Users(
        email = body['email'],
        firstname = body['firstname'],
        lastname = body['lastname'],
        password = sha256(body['password'])
    ))
    db.session.commit()

    return jsonify({
        'register': 'success',
        'msg': 'Successfully Registered'
    })

@app.route('/traindata', methods=['POST'])
def get_traindata():
    if request.method == 'POST':

        body = request.get_json()
        records = datarecord.query.filter_by(employerId=body['employerId']).order_by(datarecord.dateAtten.desc())

        if not records:
            return jsonify({'msg':'Record not found'}), 404

        return jsonify( [x.serialize() for x in records] ), 200

    return "Invalid Method", 404 

@app.route('/addrecord', methods=['POST'])
def record_add():
    body = request.get_json()

    if request.method == 'POST':
        db.session.add(datarecord(
            employerId = body['employerId'],
            hasRecu = body['hasRecu'],
            descriptionName = body['descriptionName'],
            dateAtten = body['dateAtten'],
            ceCo = body['ceCo'],
            trainingGroup = body['trainingGroup'],
            name = body['name'],
            hours = body['hours'],
            days = body['days'],
            sta = body['sta'],
            anp = body['anp'],
            insIni = body['insIni'],
            recurrent = body['recurrent'],
            oneYearExpire = body['oneYearExpire'],
            twoYearExpire = body['twoYearExpire'],
            threeYearExpire = body['threeYearExpire'],
            fourYearExpire = body['fourYearExpire']
        ))


        db.session.commit()
        return jsonify({
            'added': 'success',
            'msg': 'Successfully Added'
        })

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
