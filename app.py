from flask import Flask,request,jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_marshmallow import Marshmallow
from marshmallow import ValidationError,fields
from flask_migrate import Migrate


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@flask_db:5432/postgres"
db = SQLAlchemy(app)
migrate = Migrate(app,db)

class Currency(db.Model):
    __tablename__ = 'currencies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    code = db.Column(db.String(10), unique=True, nullable=False)
    exchange_rate = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Currency {self.name}>'
        
    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "exchange_rate": self.exchange_rate
        }

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    default_currency_id = db.Column(db.Integer, db.ForeignKey('currencies.id'))


    default_currency = db.relationship('Currency')

    def __repr__(self):
        return f'<User {self.username}>'



class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    currency_id = db.Column(db.Integer, db.ForeignKey('currencies.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    currency = db.relationship('Currency', backref=db.backref('transactions', lazy=True))
    user = db.relationship('User', backref=db.backref('transactions', lazy=True))

    def __repr__(self):
        return f'<Transaction {self.id}>'



# Marshmallow

ma = Marshmallow(app)

class CurrencySchema(ma.Schema):
    class Meta:
        model = Currency
        load_instance = True


    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    code = fields.Str(required=True)
    exchange_rate = fields.Float(required=True)


class UserSchema(ma.Schema):
    class Meta:
        model = User
        load_instance = True

    id = fields.Int(dump_only=True)
    username = ma.Str(required=True)
    email = ma.Str(required=True)
    default_currency_id = ma.Int(required=True)


class TransactionSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Transaction
        load_instance = False
        include_fk = True 

    id = ma.auto_field(dump_only=True)
    amount = ma.auto_field(required=True)
    currency_id = ma.auto_field(required=True)
    user_id = ma.auto_field(required=True)




# ENDPOINTS

@app.route('/currencies', methods=['POST'])
def add_currency():
    data = request.get_json()
    currency_schema = CurrencySchema()
    try:

        new_currency_data = currency_schema.load(data)
        new_currency = Currency(**new_currency_data) 

        db.session.add(new_currency)
        db.session.commit()
        return jsonify(currency_schema.dump(new_currency)), 201
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400


@app.route('/currencies', methods=['GET'])
def get_currencies():
    currencies = Currency.query.all()
    return jsonify([currency.json() for currency in currencies]), 200

@app.route('/currencies/<int:currency_id>', methods=['GET'])
def get_currency(currency_id):
    currency = Currency.query.get(currency_id)
    if currency:
        return jsonify(currency.json()), 200
    return jsonify({'message': 'Currency not found'}), 404

@app.route('/currencies/<int:currency_id>', methods=['PUT'])
def update_currency(currency_id):
    currency = Currency.query.get(currency_id)
    if currency:
        data = request.get_json()
        currency.name = data['name']
        currency.code = data['code']
        currency.exchange_rate = data['exchange_rate']
        db.session.commit()
        return jsonify({'message': 'Currency updated', 'currency': currency.json()}), 200
    return jsonify({'message': 'Currency not found'}), 404

@app.route('/currencies/<int:currency_id>', methods=['DELETE'])
def delete_currency(currency_id):
    currency = Currency.query.get(currency_id)
    if currency:
        db.session.delete(currency)
        db.session.commit()
        return jsonify({'message': 'Currency deleted'}), 200
    return jsonify({'message': 'Currency not found'}), 404


# Users and Transactions


@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user_schema = UserSchema()
    try:
        new_user_data = user_schema.load(data)  
        new_user = User(**new_user_data)  
        db.session.add(new_user) 
        db.session.commit()
        return jsonify(user_schema.dump(new_user)), 201
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400



@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_schema = UserSchema(many=True)  
    result = user_schema.dump(users)
    return jsonify(result), 200



@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if user:
        data = request.get_json()
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        user.default_currency_id = data.get('default_currency_id', user.default_currency_id)
        db.session.commit()
        return jsonify({'message': 'User updated', 'user': user.json()}), 200
    return jsonify({'message': 'User not found'}), 404


@app.route('/transactions', methods=['POST'])
def add_transaction():
    data = request.get_json()
    transaction_schema = TransactionSchema()
    try:
        new_transaction_data = transaction_schema.load(data)
        new_transaction = Transaction(**new_transaction_data)

        db.session.add(new_transaction)
        db.session.commit()

        return jsonify(transaction_schema.dump(new_transaction)), 201
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/transactions', methods=['GET'])
def get_transactions():
    transactions = Transaction.query.all()
    return jsonify([transaction.json() for transaction in transactions]), 200

@app.route('/transactions/<int:transaction_id>', methods=['GET'])
def get_transaction(transaction_id):
    transaction = Transaction.query.get(transaction_id)
    if transaction:
        return jsonify(transaction.json()), 200
    return jsonify({'message': 'Transaction not found'}), 404


