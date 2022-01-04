import random
from app import *
from Model import *
from Forms import *
from forgetpassVerification import mailVerCode


@login_manager.user_loader
def load_user(user_id):
    return Teacher.query.get(user_id)

@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


@app.route('/home/signup-teacher/',methods=['POST','GET'])
def signupTeacher():
    form=SignupForm()
    if request.method=='POST':
        if form.validate_on_submit():
            username=request.form['username']
            password=request.form['password']
            name=request.form['name']
            lastname=request.form['lastname']
            telephone=request.form['telephone']
            email=request.form['email']
            if Teacher.query.filter_by(username=username).filter_by(email=email).first():
                return 'this username or email is occupied.please try different one'
            teacher=Teacher(username,password,name,lastname,telephone,email)
            try:
                db.session.add(teacher)
                db.session.commit()
                logout_user()
                login_user(teacher)
            except BaseException as e:
                return str(e)
            else:
                return redirect(url_for('signupTeacher',signup_message='you signed up sucessfully'))
        else:
            return str(form.errors)
    elif request.method=='GET':
        signup_message=None
        if 'signup_message' in request.args:
            signup_message=request.args.get('signup_message')
        return render_template('signup-teacher.html',form=form,signup_message=signup_message)

@app.route('/home/login-teacher/',methods=['POST','GET'])
def loginTeacher():
    form=LoginForm()
    if request.method=='POST':
        if form.validate_on_submit():
            if current_user.is_authenticated:
                logout_user()
            username=request.form['username']
            password=request.form['password']
            user=Teacher.query.filter_by(username=username).filter_by(password=password).first()
            if user:
                logout_user()
                login_user(user)
                return redirect(url_for('TeacherDash'))
            else:
                return "user not found!"
        else:
            return str(form.errors)
    elif request.method=='GET':
        return render_template('login-teacher.html',form=form)

@app.route('/logout/<role>')
def logout(role):
    if role=='Teacher':
        if current_user.is_authenticated:
            logout_user()
        return redirect(url_for('loginTeacher'))
    elif role=='Student':
        if 'username' in session and 'password' in session:
            del session['username']
            del session['password']
        return redirect(url_for('loginStudent'))
    else:
        return redirect(url_for('Home'))

@app.route('/home/teacher-dashboard/',methods=['GET'])
def TeacherDash():
    if current_user.is_authenticated:
        if current_user.role=='Teacher':
            return render_template('teacher-dashboard.html',Classes=Classes,Exams=Exams,Student=Student,ClassMembers=ClassMembers)
        else:
            logout_user()
            return redirect(url_for('loginTeacher'))
    return redirect(url_for('loginTeacher'))



@app.route('/home/signup-student/',methods=['POST','GET'])
def signupStudent():
    form=SignupForm()
    if request.method=='POST':
        if form.validate_on_submit():
            username=request.form['username']
            password=request.form['password']
            name=request.form['name']
            lastname=request.form['lastname']
            telephone=request.form['telephone']
            email=request.form['email']
            if Student.query.filter_by(username=username).filter_by(email=email).first():
                return 'username or email is occupied.please try different one.'
            student=Student(username,password,name,lastname,telephone,email)
            try:
                db.session.add(student)
                db.session.commit()
            except BaseException as e:
                return str(e)
            else:
                return redirect(url_for('loginStudent'))
        else:
            return str(form.errors)
    elif request.method=='GET':
        signup_message=None
        return render_template('signup-student.html',form=form,signup_message=signup_message)


@app.route('/home/login-student/',methods=['GET','POST'])
def loginStudent():
    form=LoginForm()
    if request.method=='POST':
        if form.validate_on_submit():
            username=request.form['username']
            password=request.form['password']
            student=Student.query.filter_by(username=username).filter_by(password=password).first()
            if student:
                session['username']=username
                session['password']=password
                return redirect(url_for('StudentDash'))
            else:
                return 'Student not found'
        else:
            return str(form.errors)
    elif request.method=='GET':
        return render_template('login-student.html',form=form)


@app.route('/home/student-dashboard/',methods=['GET'])
def StudentDash():
    if ('username' in session) and ('password' in session):
        username=session['username']
        password=session['password']
        student=Student.query.filter_by(username=username).filter_by(password=password).first()
        if student:
            return render_template('student-dashboard.html',ClassMembers=ClassMembers,student=student,Classes=Classes,Exams=Exams,datetime=datetime,abs=abs)
        else:
            return "user not found!"
    else:
        return redirect(url_for('loginStudent'))


@app.route('/home/forget-password/',methods=['GET','POST'])#for both teachers and students
def forgetPassword():
    form=forgetpasswordForm()
    if request.method=='POST':
        if form.validate_on_submit():
            role=request.form['role']
            email=request.form['email']
            if role=='Teacher':
                teacher=Teacher.query.filter_by(email=email).first()
                if teacher:
                    user=teacher
                else:
                    return 'user is not found'
            elif role=='Student':
                student=Student.query.filter_by(email=email).first()
                if student:
                    user=student
                else:
                    return 'user is not found'
            vercode=[str(random.randint(1,9)) for i in range(6)]
            vercode=''.join(vercode)
            session['verification']={'role':role,'code':vercode,'email':email}
            if mailVerCode(Email=email,Code=vercode):
                return render_template('resetPassword.html',form=resetpasswordForm())
            else:
                return "config your service email again"
        return str(form.errors)
    return render_template('forgetPassword.html',form=form)
    
@app.route('/home/forget-password/reset-password/',methods=['POST','GET'])
def ResetPassword():
    form=resetpasswordForm()
    if request.method=='POST':
        if form.validate_on_submit():
            vercode=request.form['vercode']
            password=request.form['password']
            if vercode==session['verification']['code']:
                role=session['verification']['role']
                email=session['verification']['email']
                if role=='Teacher':
                    teacher=Teacher.query.filter_by(email=email).first()
                    try:
                        teacher.password=password
                        db.session.commit()
                    except BaseException as e:
                        return str(e)
                    else:
                        del session['verification']
                        return 'password reseted!'
                elif role=='Student':
                    student=Student.query.filter_by(email=email).first()
                    try:
                        student.password=password
                        db.session.commit()
                    except BaseException as e:
                        return str(e)
                    else:
                        if 'username' and 'password' in session:
                            session['password']=password
                        del session['verification']
                        return 'password reseted!'
                        
                else:
                    return 'Something wrong is happend'
            else:
                return render_template('resetPassword.html',form=form)
        else:
            return str(form.errors)
    elif request.method=='GET':
        if not('verification' in session):
            return redirect(url_for('forgetPassword'))
        return render_template('resetPassword.html',form=form)
                    

@app.route('/home/student-dashboard/join-class/',methods=['POST'])
def JoinClass():
    username=session['username']
    classKey=request.form['classKey']
    classPassword=request.form['classPassword']
    _class=Classes.query.filter_by(classKey=classKey).filter_by(classPassword=classPassword).first()
    if _class:
        student=Student.query.filter_by(username=username).first()
        if ClassMembers.query.filter_by(studentid=student.id).filter_by(classid=_class.id).first():
            return jsonify({
                'message':'You already joined to this class.'
            })
        classmember=ClassMembers(_class.id,student.id)
        try:
            db.session.add(classmember)
            db.session.commit()
        except BaseException as e:
            return str(e)
        else:
            return jsonify({
                'message':'You joind successfully'
            })
    else:
        return jsonify({
            'message':'Class not found '
        })

@app.route('/home/teacher-dashboard/build-class/',methods=['POST'])
def BuildClass():
    classKey=request.form['classKey']
    classPassword=request.form['classPassword']
    className=request.form['className']
    teacherid=request.form['teacherid']
    _class=Classes.query.filter_by(classKey=classKey).first()
    if _class:
        return jsonify({
            'message':'this class key is unavailable.try another key please.'
        })
    _class=Classes(teacherid, classKey, classPassword, className)
    try:
        db.session.add(_class)
        db.session.commit()
    except BaseException as e:
        return jsonify({
            'message':str(e)
        })
    else:
        return jsonify({
            'message':'The class is built successfully'
        })


@app.route('/home/teacher-dashboard/configure-exam/',methods=['POST'])
def ConfigureExam():
    if request.method=='POST':
        if current_user.is_authenticated:
            classid=request.form['examclassId']
            examName=request.form['examName']
            starttime=request.form['examStart'].split('T')[1].split(':')
            startdate=request.form['examStart'].split('T')[0].split('-')
            endtime=request.form['examEnd'].split('T')[1].split(':')
            enddate=request.form['examEnd'].split('T')[0].split('-')
            startdatetime=datetime.datetime(int(startdate[0]),int(startdate[1]),int(startdate[2]),int(starttime[0]),int(starttime[1]))
            enddatetime=datetime.datetime(int(enddate[0]),int(enddate[1]),int(enddate[2]),int(endtime[0]),int(endtime[1]))
            if startdatetime>enddatetime or startdatetime<datetime.datetime.now() or enddatetime<datetime.datetime.now():
                return jsonify({
                    'message':'date time configuration for exam start time and end time is not valid.try again'
                })
            try:
                exam=Exams(examName,classid,startdatetime,enddatetime)
                db.session.add(exam)
                db.session.commit()
            except BaseException as e:
                return jsonify({
                    'message':str(e)
                })
            else:
                return jsonify({
                    'message':'Exam is configed well'})
@app.route('/home/teacher-dashboard/delete-exam/',methods=['POST'])
def delExam():
    if request.method=='POST':
        if current_user.is_authenticated:
            examid=request.form['examid']
            exam=Exams.query.filter_by(id=examid).first()
            if exam:
                try:
                    db.session.delete(exam)
                    db.session.commit()
                except BaseException as e:
                    return jsonify({
                        'message':str(e)
                    })
                else:
                    return jsonify({
                        'message':'exam deleted'
                    })

@app.route('/home/teacher-dashboard/delete-class/',methods=['POST'])
def delClass():
    if request.method=='POST':
        if current_user.is_authenticated:
            classid=request.form['classid']
            _class=Classes.query.filter_by(id=classid).first()
            if _class:
                try:
                    db.session.delete(_class)
                    db.session.commit()
                except BaseException as e:
                    return jsonify({
                        'message':str(e)
                    })
                else:
                    return jsonify({
                        'message':'class deleted'
                    })


@app.route('/home/teacher-dashboard/configure-exam-questions/',methods=['POST','GET'])
def ConfigExamQuestions():
    if request.method=='POST':
        if current_user.is_authenticated:
            examid=request.form['examid']
            classid=request.form['classid']
            question=request.form['question']
            ansopt1=request.form['option-1'] #answer option 1
            ansopt2=request.form['option-2']
            ansopt3=request.form['option-3']
            ansopt4=request.form['option-4']
            correct_answer_order=request.form['correct-answer-order']
            question=Questions(question, classid, examid)
            try:
                db.session.add(question)
                db.session.flush()
            except BaseException as e:
                return str(e)
            questionid=Questions.query.filter_by(examid=examid).order_by(desc(Questions.id)).first().id
            answeroption1=QuestionAnswerOptions(questionid,ansopt1,1)
            answeroption2=QuestionAnswerOptions(questionid, ansopt2,2)
            answeroption3=QuestionAnswerOptions(questionid, ansopt3,3)
            answeroption4=QuestionAnswerOptions(questionid, ansopt4,4)
            try:
                db.session.add(answeroption1)
                db.session.commit()
                db.session.add(answeroption2)
                db.session.commit()
                db.session.add(answeroption3)
                db.session.commit()
                db.session.add(answeroption4)
                db.session.flush()
            except BaseException as e:
                return str(e)


            question_answer=QuestionAnswer(questionid,correct_answer_order)
            try:
                db.session.add(question_answer)
                db.session.commit()
            except BaseException as e:
                return str(e)
            else:
                return redirect(url_for('ConfigExamQuestions'))
    elif request.method=='GET':
        if current_user.is_authenticated:
            if 'examid' in request.args:
                examid=request.args.get('examid')
                exam=Exams.query.filter_by(id=examid).first()
                _class=Classes.query.filter_by(id=exam.classid).first()
                teacher=Teacher.query.filter_by(id=_class.teacherid).first()
                return render_template('ConfigExamQuestions-teacher.html',teacher=teacher,exam=exam,_class=_class,Questions=Questions)
            else:
                return redirect(url_for('TeacherDash'))
        return redirect(url_for('loginTeacher'))
    

@app.route('/home/student-dashboard/load-exam/',methods=['GET'])
def LoadExam():
    if 'username' in session and 'password' in session:
        username=session['username']
        password=session['password']
        examid=request.args.get('examid')
        exam=Exams.query.filter_by(id=examid).first()
        classid=request.args.get('classid')
        _class=Classes.query.filter_by(id=classid).first()
        teacher=Teacher.query.filter_by(id=_class.teacherid).first()
        student=Student.query.filter_by(username=username).filter_by(password=password).first()
        if student:
            if ClassMembers.query.filter_by(studentid=student.id).first():
                return render_template('exampage-student.html',student=student,_class=_class,teacher=teacher,exam=exam,
                Questions=Questions,QuestionAnswerOptions=QuestionAnswerOptions)
            return 'You are not joined to this class.please join first.'
        else:
            return 'Student is not found'
    return redirect(url_for('loginStudent'))

@app.route('/home/student-dashboard/load-exam/send-answer/',methods=['POST'])
def SubmitAnswer():
    if request.method=='POST':
        if 'username' in session and 'password' in session:
            username=session['username']
            password=session['password']
            classid=request.form['classid']
            questionid=request.form['questionid']
            answerorder=request.form['answer_order']
            student=Student.query.filter_by(username=username).filter_by(password=password).first()
            studentid=student.id
            
            studentanswersheet=StudentAnswerSheet.query.filter_by(questionid=questionid).filter_by(studentid=studentid).first()
            if studentanswersheet:
                studentanswersheet.answerorder=answerorder
                db.session.commit()
                return jsonify({
                    'message':f'answer-order modified to {answerorder}'
                })
            else:
                studentanswersheet=StudentAnswerSheet(classid,studentid,questionid,answerorder)
                try:
                    db.session.add(studentanswersheet)
                    db.session.commit()
                except BaseException as e:
                    return jsonify({
                        'message':str(e)
                    })
                else:
                    return jsonify({
                        'message':f'answer-order {answerorder} submitted.'
                    })


@app.route('/home/student-dashboard/exam-result/',methods=['GET'])#a student can observe his/her exams results from his/her dashboard
def ExamResult():
    if 'username' in session and 'password' in session:
        if ('examid' in request.args):
            examid=request.args['examid']
            exam=Exams.query.filter_by(id=examid).first()
            username=session['username']
            password=session['password']
            if exam:
                student=Student.query.filter_by(username=username).filter_by(password=password).first()
                if ClassMembers.query.filter_by(classid=exam.classid).filter_by(studentid=student.id).first():
                    #calculate correct and incorret answers
                    correct_answers=0
                    incorrect_answers=0
                    for question in Questions.query.filter_by(examid=exam.id).all():
                        stAnswer=StudentAnswerSheet.query.filter_by(questionid=question.id).filter_by(studentid=student.id).first()
                        if stAnswer:
                            stAnswer=stAnswer.answerorder
                        else:
                            return f'you have not participated at exam.'
                        correctAnswer=QuestionAnswer.query.filter_by(questionid=question.id).first().answerorder
                        if stAnswer==correctAnswer:
                            correct_answers+=1
                        else:
                            incorrect_answers+=1
                    #end
                    return render_template('examresult.html',exam=exam,student=student,Questions=Questions,StudentAnswerSheet=StudentAnswerSheet,QuestionAnswer=QuestionAnswer,correct_answers=correct_answers,
                    incorrect_answers=incorrect_answers)
                else:
                    return redirect(url_for('StudentDash'))
            else:
                return redirect(url_for('StudentDash'))

        else:
            return redirect(url_for('StudentDash'))
    else:
        return redirect(url_for('loginStudent'))


@app.route('/home/teacher-dashboard/setudents-reportcard/',methods=['GET'])
def StudentsReportCard():#shows students report card to the teacher.
    if current_user.is_authenticated:
        examid=request.args.get('examid')
        exam=Exams.query.filter_by(id=examid).first()
        _class=Classes.query.filter_by(teacherid=current_user.id).filter_by(id=exam.classid).first()#make sure that this teacher(current_user) is owner of class not other teacher who tries to read the another class students report cards.
        if _class:
            #reportcardSummary
            reportcardSummary=dict()
            for classmember in ClassMembers.query.filter_by(classid=_class.id).all():
                student=Student.query.filter_by(id=classmember.studentid).first()
                wrong_answers=0
                correct_answers=0
                for question in Questions.query.filter_by(examid=exam.id).all():
                    studentanswer=StudentAnswerSheet.query.filter_by(studentid=student.id).filter_by(questionid=question.id).first().answerorder
                    correctanswer=QuestionAnswer.query.filter_by(questionid=question.id).first().answerorder
                    if studentanswer==correctanswer:
                        correct_answers+=1
                    else:
                        wrong_answers+=1
                reportcardSummary[student.id]={
                    'wrong_answers':wrong_answers,
                    'correct_answers':correct_answers,
                    'exam':exam.examName
                }
            #End
            return render_template('students-reportcard.html',exam=exam,_class=_class,ClassMembers=ClassMembers,Student=Student,Questions=Questions,
            StudentAnswerSheet=StudentAnswerSheet,QuestionAnswer=QuestionAnswer,reportcardSummary=reportcardSummary)
        else:
            return redirect(url_for('TeacherDash'))
    return redirect(url_for('signupTeacher'))
app.run(debug='True')
