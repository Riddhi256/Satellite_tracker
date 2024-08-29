from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///missions.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)


# Define the MissionScenario model
class MissionScenario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(200), nullable=False)


# Define the CustomScenario model
class CustomScenario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    mission_scenario_id = db.Column(db.Integer, nullable=False)


# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)


# Define the MissionScenario schema
class MissionScenarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = MissionScenario
        load_instance = True


# Define the CustomScenario schema
class CustomScenarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = CustomScenario
        load_instance = True


# Define the User schema
class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True


# Create database tables and add initial data
with app.app_context():
    db.create_all()

    # Adding mission scenarios if not already present
    if not MissionScenario.query.first():
        mission1 = MissionScenario(name="Mission 1", description="Description for Mission 1")
        mission2 = MissionScenario(name="Mission 2", description="Description for Mission 2")
        mission3 = MissionScenario(name="Mission 3", description="Description for Mission 3")
        db.session.add_all([mission1, mission2, mission3])
        db.session.commit()

    # Adding custom scenarios if not already present
    if not CustomScenario.query.first():
        custom_scenario1 = CustomScenario(user_id=1, mission_scenario_id=1)
        custom_scenario2 = CustomScenario(user_id=1, mission_scenario_id=2)
        custom_scenario3 = CustomScenario(user_id=2, mission_scenario_id=3)
        db.session.add_all([custom_scenario1, custom_scenario2, custom_scenario3])
        db.session.commit()


# Define API endpoints
@app.route('/missions', methods=['GET'])
def get_missions():
    missions = MissionScenario.query.all()
    return jsonify(MissionScenarioSchema(many=True).dump(missions))


@app.route('/custom_scenarios', methods=['GET'])
def get_custom_scenarios():
    custom_scenarios = CustomScenario.query.all()
    return jsonify(CustomScenarioSchema(many=True).dump(custom_scenarios))


@app.route('/create_custom_scenario', methods=['POST'])
def create_custom_scenario():
    data = request.json
    custom_scenario = CustomScenario(**data)
    db.session.add(custom_scenario)
    db.session.commit()
    return jsonify({'message': 'Custom scenario created successfully'}), 201


@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify(UserSchema(many=True).dump(users))


@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.json
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201


# Default route to show available endpoints
@app.route('/', methods=['GET'])
def index():
    return "Welcome to the Flask API. Use /missions, /custom_scenarios, /create_custom_scenario, /users, and /create_user endpoints."


if __name__ == '__main__':
    app.run(debug=True)
