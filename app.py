from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate

# from routes.user import api_bp


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///skivisi.db"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

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
    updatedAt = db.Column(db.DateTime, onupdate=datetime.now)
    skills = db.relationship('Skill', backref=db.backref('user', lazy=True))
    skillPoints = db.relationship('SkillPoint', backref=db.backref('user', lazy=True))
    specialAbilities = db.relationship('SpecialAbility', backref=db.backref('user', lazy=True))
    specs = db.relationship('Spec', backref=db.backref('user', lazy=True))
    requests = db.relationship('Request', backref=db.backref('user', lazy=True))

class Skill(db.Model):
    skillId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.userId'))
    InherentName = db.Column(db.String)
    InherentDescription = db.Column(db.String)
    updatedAt = db.Column(db.DateTime, onupdate=datetime.now)

class SkillPoint(db.Model):
    skillPointId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.userId'))
    FR = db.Column(db.Integer)
    BK = db.Column(db.Integer)
    DB = db.Column(db.Integer)
    SBR = db.Column(db.Integer)
    AR = db.Column(db.Integer)
    TS = db.Column(db.Integer)
    COM = db.Column(db.Integer)

class SpecialAbility(db.Model):
    specialAbilityId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.userId'))
    skillList = db.Column(db.String)
    skillSelection = db.Column(db.Boolean)

class Spec(db.Model):
    specId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.userId'))
    github = db.Column(db.String)
    offHours = db.Column(db.String)
    createdAt = db.Column(db.DateTime, default=datetime.now)
    portfolios = db.relationship('Portfolio', backref=db.backref('spec', lazy=True))
    skillSummaries = db.relationship('SkillSummary', backref=db.backref('spec', lazy=True))
    sellingPoints = db.relationship('SellingPoint', backref=db.backref('spec', lazy=True))
    qualifications = db.relationship('Qualification', backref=db.backref('spec', lazy=True))
    previousWorks = db.relationship('PreviousWork', backref=db.backref('spec', lazy=True))
    developmentExperiences = db.relationship('DevelopmentExperience', backref=db.backref('spec', lazy=True))

class Portfolio(db.Model):
    portfolioId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    specId = db.Column(db.Integer, db.ForeignKey('spec.specId'))
    heading = db.Column(db.String)
    url = db.Column(db.String)

class SkillSummary(db.Model):
    skillSummaryId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    specId = db.Column(db.Integer, db.ForeignKey('spec.specId'))
    autoCalibrationId = db.Column(db.Integer, db.ForeignKey('auto_calibration.autoCalibrationId'))

class SellingPoint(db.Model):
    sellingPointId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    specId = db.Column(db.Integer, db.ForeignKey('spec.specId'))
    title = db.Column(db.String)
    content = db.Column(db.String)

class Qualification(db.Model):
    qualificationId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    specId = db.Column(db.Integer, db.ForeignKey('spec.specId'))
    credential = db.Column(db.String)
    acquisitionDate = db.Column(db.String)

class PreviousWork(db.Model):
    previousWorkId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    specId = db.Column(db.Integer, db.ForeignKey('spec.specId'))
    industry = db.Column(db.String)
    occupation = db.Column(db.String)
    JobDuties = db.Column(db.String)

class DevelopmentExperience(db.Model):
    developmentExperienceId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    specId = db.Column(db.Integer, db.ForeignKey('spec.specId'))
    startDate = db.Column(db.String)
    duration = db.Column(db.String)
    assignedTask = db.Column(db.String)
    teamSize = db.Column(db.String)
    totalProjectHeadcount = db.Column(db.String)
    projectName = db.Column(db.String)
    jobDuties = db.Column(db.String)
    img = db.Column(db.String)
    autoCalibrationId = db.Column(db.Integer, db.ForeignKey('auto_calibration.autoCalibrationId'))

class AutoCalibration(db.Model):
    autoCalibrationId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    skill = db.Column(db.String)
    membership = db.Column(db.Integer)
    category = db.Column(db.Integer)
    FR = db.Column(db.Integer)
    CL = db.Column(db.Integer)
    ML = db.Column(db.Integer)
    QA = db.Column(db.Integer)
    JAVA = db.Column(db.Integer)
    PHP = db.Column(db.Integer)
    skillSummaries = db.relationship('SkillSummary', backref=db.backref('autoCalibration', lazy=True))
    developmentExperiences = db.relationship('DevelopmentExperience', backref=db.backref('autoCalibration', lazy=True))

class Request(db.Model):
    applicationId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.userId'))
    status = db.Column(db.Integer)
    adminComment = db.Column(db.String)
    engineerComment = db.Column(db.String)
    adminId = db.Column(db.Integer, db.ForeignKey('admin.adminId'))
    createdAt = db.Column(db.DateTime, default=datetime.now)
    resultedAt = db.Column(db.DateTime)

class Admin(db.Model):
    adminId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    name = db.Column(db.String)
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

#管理者の登録
@app.route('/api/admin/register', methods=['POST'])
def create_admin():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')

    admin = Admin(email=email, password=password, name=name)
    db.session.add(admin)
    db.session.commit()

    return jsonify({'message': 'Admin created successfully'}), 201

#管理者のログイン
@app.route('/api/admin/login', methods=['GET'])
def login_admin():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    admin = Admin.query.filter_by(email=email).first()

    if admin and admin.password == password:
        admin_info = {
            'adminId': admin.adminId,
            'email': admin.email,
            'name': admin.name,
            'createdAt': admin.createdAt
        }
        return jsonify(admin_info), 200
    else:
        return jsonify({'message': 'Invalid email or password'}), 401
