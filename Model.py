from app import *

class Teacher(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    role=db.Column(db.String(10),nullable=False,default="Teacher")
    username = db.Column(db.String(64), unique=True,nullable=False)
    password= db.Column(db.String(64),nullable=False)
    name=db.Column(db.String(64),nullable=False)
    lastname=db.Column(db.String(64),nullable=False)
    telephone=db.Column(db.String(11),nullable=False)
    email=db.Column(db.String(100),nullable=False,unique=True)
    dtime=db.Column(db.DateTime,nullable=False,default=datetime.datetime.utcnow())

    __tablename__='teacher'
    def __init__(self,username,password,name,lastname,telephone,email):
        self.username=username
        self.password=password
        self.name=name
        self.lastname=lastname
        self.telephone=telephone
        self.email=email

    @classmethod
    def create(cls):
        cls.__table__.create(engine)
    
    @classmethod
    def remove(cls):
        cls.__table__.drop(engine)
        
    def __repr__(self):
        return '<Student {}>'.format(self.username)

class Student(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    role=db.Column(db.String(10),nullable=False,default="Student")
    username = db.Column(db.String(64), unique=True,nullable=False)
    password= db.Column(db.String(64),nullable=False)
    name=db.Column(db.String(64),nullable=False)
    lastname=db.Column(db.String(64),nullable=False)
    telephone=db.Column(db.String(11),nullable=False)
    email=db.Column(db.String(100),nullable=False,unique=True)
    dtime=db.Column(db.DateTime,nullable=False,default=datetime.datetime.utcnow())
    __tablename__='student'
    def __init__(self,username,password,name,lastname,telephone,email):
        self.username=username
        self.password=password
        self.name=name
        self.lastname=lastname
        self.telephone=telephone
        self.email=email

    @classmethod
    def create(cls):
        cls.__table__.create(engine)
    
    @classmethod
    def remove(cls):
        cls.__table__.drop(engine)
        
    def __repr__(self):
        return '<Student {}>'.format(self.username)


class Classes(UserMixin, db.Model):
    __tablename__='classes'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    teacherid=db.Column(db.Integer,db.ForeignKey('teacher.id',ondelete='CASCADE'),nullable=False)
    className=classKey=db.Column(db.String(100),nullable=False)
    classKey=db.Column(db.String(100),nullable=False,unique=True)#like username for users.
    classPassword=db.Column(db.String(64),nullable=False)
    dtime=db.Column(db.DateTime,nullable=False,default=datetime.datetime.utcnow())
    fk_teacherid=db.relationship('Teacher',foreign_keys=[teacherid])
    def __init__(self,teacherid,classKey,classPassword,className):
        self.teacherid=teacherid
        self.classKey=classKey
        self.classPassword=classPassword
        self.className=className

    @classmethod
    def create(cls):
        cls.__table__.create(engine)
    
    @classmethod
    def remove(cls):
        cls.__table__.drop(engine)
        
    def __repr__(self):
        return '<Class {}>'.format(self.id) 


class ClassMembers(UserMixin, db.Model):
    __tablename__='classmembers'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    classid=db.Column(db.Integer,db.ForeignKey('classes.id',ondelete='CASCADE'),nullable=False)
    studentid=db.Column(db.Integer,db.ForeignKey('student.id',ondelete='CASCADE'),nullable=False)
    dtime=db.Column(db.DateTime,nullable=False,default=datetime.datetime.utcnow())
    fk_classid=db.relationship('Classes',foreign_keys=[classid])
    fk_studentid=db.relationship('Student',foreign_keys=[studentid])
    def __init__(self,classid,studentid):
        self.classid=classid
        self.studentid=studentid
        

    @classmethod
    def create(cls):
        cls.__table__.create(engine)
    
    @classmethod
    def remove(cls):
        cls.__table__.drop(engine)
        
    def __repr__(self):
        return '<ClassMembers {}>'.format(self.id) 




class Exams(UserMixin, db.Model):
    __tablename__='exams'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    examName=db.Column(db.String(64),nullable=False)
    classid= db.Column(db.Integer,db.ForeignKey('classes.id',ondelete='CASCADE'),nullable=False)
    starttime=db.Column(db.DateTime,nullable=False)
    endtime=db.Column(db.DateTime,nullable=False)
    dtime=db.Column(db.DateTime,nullable=False,default=datetime.datetime.utcnow()) #datetime that exam is configured at
    fk_classid=db.relationship('Classes',foreign_keys=[classid])

    def __init__(self,examName,classid,starttime,endtime):
        self.classid=classid
        self.starttime=starttime
        self.endtime=endtime
        self.examName=examName

    @classmethod
    def create(cls):
        cls.__table__.create(engine)
    
    @classmethod
    def remove(cls):
        cls.__table__.drop(engine)
        
    def __repr__(self):
        return '<Exam {}>'.format(self.id) 


class Questions(UserMixin, db.Model):
    __tablename__='questions'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    classid= db.Column(db.Integer,db.ForeignKey('classes.id',ondelete='CASCADE'),nullable=False)
    examid= db.Column(db.Integer,db.ForeignKey('exams.id',ondelete='CASCADE'),nullable=False)
    question=db.Column(db.String(1000),nullable=False)
    dtime=db.Column(db.DateTime,nullable=False,default=datetime.datetime.utcnow()) #datetime that exam is configured at
    fk_classid=db.relationship('Classes',foreign_keys=[classid])
    fk_examid=db.relationship('Exams',foreign_keys=[examid])

    def __init__(self,question,classid,examid):
        self.question=question
        self.classid=classid
        self.examid=examid

    @classmethod
    def create(cls):
        cls.__table__.create(engine)
    
    @classmethod
    def remove(cls):
        cls.__table__.drop(engine)
        
    def __repr__(self):
        return '<Question {}>'.format(self.id)


class QuestionAnswerOptions(UserMixin, db.Model):
    __tablename__='questionansweroptions'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    questionid=db.Column(db.Integer,db.ForeignKey('questions.id',ondelete='CASCADE'),nullable=False)
    answeroption=db.Column(db.String(1000),nullable=False)
    optionOrder=db.Column(db.Integer,nullable=False)
    fk_questionid=db.relationship('Questions',foreign_keys=[questionid])


    def __init__(self,questionid,answeroption,optionOrder):
        self.questionid=questionid
        self.answeroption=answeroption
        self.optionOrder=optionOrder

    @classmethod
    def create(cls):
        cls.__table__.create(engine)
    
    @classmethod
    def remove(cls):
        cls.__table__.drop(engine)
        
    def __repr__(self):
        return '<QuestionAnswerOptions {}>'.format(self.id)




class QuestionAnswer(UserMixin, db.Model):
    __tablename__='questionanswer'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    questionid=db.Column(db.Integer,db.ForeignKey('questions.id',ondelete='CASCADE'),nullable=False)
    answerorder=db.Column(db.Integer,nullable=False)#Example:answerorder=2 means in options as answer determined for question,second option determined as a correct answer.
    fk_questionid=db.relationship('Questions',foreign_keys=[questionid])

    def __init__(self,questionid,answerorder):
        self.questionid=questionid
        self.answerorder=answerorder

    @classmethod
    def create(cls):
        cls.__table__.create(engine)
    
    @classmethod
    def remove(cls):
        cls.__table__.drop(engine)
        
    def __repr__(self):
        return '<QuestionAnswer {}>'.format(self.id)



class StudentAnswerSheet(UserMixin, db.Model):
    __tablename__='studentanswersheet'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    classid= db.Column(db.Integer,db.ForeignKey('classes.id',ondelete='CASCADE'),nullable=False)
    studentid=db.Column(db.Integer,db.ForeignKey('student.id',ondelete='CASCADE'),nullable=False)
    questionid=db.Column(db.Integer,db.ForeignKey('questions.id',ondelete='CASCADE'),nullable=False)
    answerorder=db.Column(db.Integer,nullable=False)#answeroption=3 means that student figured out the 3th answer option as an correct answer of question. answer option example=>1)a 2)b 3)c 4)d
    fk_questionid=db.relationship('Questions',foreign_keys=[questionid])
    fk_classid=db.relationship('Classes',foreign_keys=[classid])
    fk_studentid=db.relationship('Student',foreign_keys=[studentid])

    def __init__(self,classid,studentid,questionid,answerorder):
        self.classid=classid
        self.studentid=studentid
        self.questionid=questionid
        self.answerorder=answerorder

    @classmethod
    def create(cls):
        cls.__table__.create(engine)
    
    @classmethod
    def remove(cls):
        cls.__table__.drop(engine)
        
    def __repr__(self):
        return '<StudentAnswerSheet {}>'.format(self.id)







db.create_all()
