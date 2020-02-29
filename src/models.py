from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    firstname = db.Column(db.String(120), nullable=False)
    lastname = db.Column(db.String(120) )
    password = db.Column(db.String(80), nullable=False)
    avatar = db.Column(db.String(220), default='avatar.png')
    

    def __repr__(self):
        return '<Users %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "avatar": self.avatar,
        }

class datarecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employerId = db.Column(db.Integer)
    courseNumber = db.Column(db.Integer)
    hasRecu = db.Column(db.String(10)) 
    descriptionName = db.Column(db.String(60))
    dateAtten = db.Column(db.String(30))
    ceCo = db.Column(db.String(12))
    trainingGroup = db.Column(db.String(30))
    name = db.Column(db.String(40))
    hours = db.Column(db.String(3))
    days = db.Column(db.Float(7, 2))
    sta = db.Column(db.String(1))
    anp = db.Column(db.Integer)
    insIni = db.Column(db.String(3))
    recurrent = db.Column(db.String(1)) 
    oneYearExpire =  db.Column(db.String(30))
    twoYearExpire =  db.Column(db.String(30))
    threeYearExpire =  db.Column(db.String(30))
    fourYearExpire =  db.Column(db.String(30))

    def serialize(self):
        return {
            "id" : self.id,
            "employerId": self.employerId,
            "courseNumber" : self.courseNumber,
            "hasRecu" : self.hasRecu,
            "descriptionName" : self.descriptionName,
            "dateAtten" : self.dateAtten,
            "ceCo" : self.ceCo,
            "trainingGroup" : self.trainingGroup,
            "name" : self.name,
            "hours" : self.hours,
            "days" : self.days,
            "sta" : self.sta,
            "anp" : self.anp,
            "insIni" : self.insIni,
            "recurrent" : self.recurrent,
            "oneYearExpire" : self.oneYearExpire,
            "twoYearExpire" : self.twoYearExpire,
            "threeYearExpire" : self.threeYearExpire,
            "fourYearExpire" : self.fourYearExpire
        }