from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# from routes.user import api_bp


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///skivisi.db"
db = SQLAlchemy(app)

class User(db.Model):
    userId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, unique=True, nullable=False)
    employeeNumber = db.Column(db.Integer)
    joinDate = db.Column(db.String)
    userName = db.Column(db.String)
    affiliation = db.Column(db.String)
    businessSituation = db.Column(db.Boolean)
    password = db.Column(db.String)
    confirmPassword = db.Column(db.String)
    createdAt = db.Column(db.DateTime, default=datetime.now)

#ユーザーの登録
@app.route('/api/register',methods=['POST'])
def post_user():
    data = request.json
    email = data.get('email')
    employeeNumber = data.get('employeeNumber')
    joinDate = data.get('joinDate')
    userName = data.get('userName')
    affiliation = data.get('affiliation')
    businessSituation = data.get('businessSituation')
    password = data.get('password')
    confirmPassword = data.get('confirmPassword')

    user = User(
        email=email,
        employeeNumber=employeeNumber,
        joinDate=joinDate,
        userName=userName,
        affiliation=affiliation,
        businessSituation=businessSituation,
        password=password,
        confirmPassword=confirmPassword
    )

    db.session.add(user)
    db.session.commit()

    return jsonify(message="User information has been successfully posted."), 201

#ユーザーのログイン
@app.route('/api/login', methods=['GET'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')


    # ユーザーの検証と情報の取得
    user = User.query.filter_by(email=email, password=password).first()
    if user:
        # ユーザーが存在する場合はログイン成功
        response = {
                'userId': user.userId,
                'email': user.email,
                'employeeNumber': user.employeeNumber,
                'joinDate': user.joinDate,
                'userName': user.userName,
                'affiliation': user.affiliation,
                'businessSituation': user.businessSituation,
                'createdAt': user.createdAt
        }

        return jsonify(response), 200
    else:
        # ユーザーが存在しない場合はログイン失敗
        response = {'message': 'Invalid email or password.'}
        return jsonify(response), 401

# ユーザーのIDからユーザーの情報を取得
@app.route('/api/user/<int:userId>', methods=['GET'])
def get_user(userId):
    # ユーザーの情報を取得
    user = User.query.get(userId)

    if user:
        # ユーザーが存在する場合は情報を返す
        response = {
            'userId': user.userId,
            'email': user.email,
            'employeeNumber': user.employeeNumber,
            'joinDate': user.joinDate,
            'userName': user.userName,
            'affiliation': user.affiliation,
            'businessSituation': user.businessSituation,
            'createdAt': user.createdAt
        }
        return jsonify(response), 200
    else:
        # ユーザーが存在しない場合はエラーメッセージを返す
        response = {'message': 'User not found.'}
        return jsonify(response), 404

# app.register_blueprint(api_bp, url_prefix='/api')




# if __name__ == '__main__':
#     app.run(port=8003)
