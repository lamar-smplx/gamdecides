from flask_bcrypt import Bcrypt
import re, MySQLdb.cursors
from flask_mysqldb import MySQL
from flask import Flask, render_template, url_for, flash, redirect, request, session, g
from forms import RegistrationForm, LoginForm,RegistrationPoll, OpeningForm, ClosingForm, VotingForm
from forms import RegistrationForm, LoginForm,RegistrationPoll, OpeningForm, RegistrationCons, RegistrationObs

app = Flask(__name__)


mysql = MySQL()

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'mydb'

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

mysql.init_app(app)
bcrypt = Bcrypt(app)

@app.errorhandler(404)
def error_404(error):
    return render_template('404.html'), 404

@app.errorhandler(403)
def error_403(error):
    return render_template('403.html'), 403

@app.errorhandler(500)
def error_500(error):
    return render_template('500.html'), 500

app.register_error_handler(404,error_404)
app.register_error_handler(403,error_403)
app.register_error_handler(500,error_500)

@app.route("/", methods=['GET', 'POST'])
@app.route("/login", methods=['GET', 'POST'])
def login():
    session.pop('loggedin', None)
    cur = mysql.connection.cursor()
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        cur.execute("SELECT * FROM login WHERE email=(%s)", (email,))
        account = cur.fetchone()
        if account:
            if account[2]=='localobserver':
                if bcrypt.check_password_hash(account[1],password):
                    cur.execute("SELECT * FROM local_obs WHERE email=(%s)", (email,))
                    data = cur.fetchone()
                    session['loggedin'] = 'localobserver'
                    session['type'] = 'Local Observer'
                    session['email'] = account[0]
                    session['id'] = data[0]
                    session['name'] = data[1]
                    return redirect(url_for('local_home'))
                else:
                    flash(f'Password is Incorrect','danger')                   
            elif account[2]=='observer':
                if (password):
                    cur.execute("SELECT * FROM observer WHERE email=(%s)", (email,))
                    data = cur.fetchone()
                    session['loggedin'] = 'observer'
                    session['type'] = 'Observer'
                    session['email'] = account[0]
                    session['id'] = data[0]
                    session['name'] = data[1]
                    return redirect(url_for('observer_home'))
                else:
                    flash(f'Password is Incorrect','danger') 
            elif account[2]=='superobserver':
                if bcrypt.check_password_hash(account[1],password):
                    cur.execute("SELECT * FROM super_obs WHERE email=(%s)", (email,))
                    data = cur.fetchone()
                    session['loggedin'] = 'superobserver'
                    session['type'] = 'Super Observer'
                    session['email'] = account[0]
                    session['id'] = data[0]
                    session['name'] = data[1]
                    return redirect(url_for('super_home'))
                else:
                    flash(f'Password is Incorrect','danger')
        else:
            flash(f'Username does not exist','danger')
    return render_template('login.html', title='Welcome')

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('type', None)
   session.pop('email', None)
   session.pop('id', None)
   session.pop('name', None)
   # Redirect to login page
   return redirect(url_for('login'))

@app.route("/local_home")
def local_home():
    if g.loggedin=='localobserver':
        return render_template('local_home.html', title='Local Observer Home')
    return render_template('login.html', title='Welcome')

@app.before_request
def before_request():
     g.loggedin = None
     if 'loggedin' in session:
         g.loggedin = session['loggedin'] 

@app.route("/opening", methods=['GET', 'POST'])
def opening():
    form = OpeningForm()
    if form.validate_on_submit():
        if request.method == "POST":
            arr = [session['id']]
            for val in ('arrivaltime','departuretime','q1','q2','q3','q3c','q4','q5','q6','q6c','q7','q7c','q8','q8c','q9','q9c','q10','q10c','q11','q11c','q12','q12c','q13','q14','q15','q16','q17','q18','q18c','q19','q20'):
                arr.append(request.form[val])
            cur = mysql.connection.cursor()
            arr = tuple(arr)
            cur.execute("SELECT * from opening where l_id=(%s)",(str(session['id'])))
            exist = cur.fetchone()
            if exist:
                flash('You have already submitted your opening form','danger')
            else:
                cur.execute(f"INSERT INTO opening VALUES {arr}")
                mysql.connection.commit()
                flash(f'Opening Form sent!!!','success')
            return redirect(url_for('local_home'))
    if g.loggedin=='localobserver':
        return render_template('opening.html', title='Opening Form',form=form)
    return render_template('login.html', title='Welcome')

@app.route("/voting", methods=['GET', 'POST'])
def voting():
    form = VotingForm()
    if form.validate_on_submit():
        if request.method == "POST":
            arr = [session['id']]
            for val in ('arrivaltime','departuretime','q1','q2','q3','q4','q4c','q5','q6','q7','q8','q9','q9c','q10','q10c','q11','q11c','q12','q12c','q13','q13c','q14','q14c','q15','q16','q17','q18','q19','q20','q21','q22','q23','q23c','q24','q24c','q25','q25c','q26','q26c','q27','q28'):
                arr.append(request.form[val])
            cur = mysql.connection.cursor()
            arr = tuple(arr)
            cur.execute(f"INSERT INTO voting(l_id,arrival_time,departure_time,q1,q2,q3,q4,q4c,q5,q6,q7,q8,q9,q9c,q10,q10c,q11,q11c,q12,q12c,q13,q13c,q14,q14c,q15,q16,q17,q18,q19,q20,q21,q22,q23,q23c,q24,q24c,q25,q25c,q26,q26c,q27,q28) VALUES {arr}")
            mysql.connection.commit()
            flash(f'Voting Form sent!!!','success')
            return redirect(url_for('local_home'))
    if g.loggedin=='localobserver':
        return render_template('voting.html', title='Voting Form',form=form)
    return render_template('login.html', title='Welcome')

@app.route("/closing", methods=['GET', 'POST'])
def closing():
    form = ClosingForm()
    if form.validate_on_submit():
        if request.method == "POST":
            arr = [session['id']]
            for val in ('arrivaltime','departuretime','q1','q1c','q2','q2c','q3','q3c','q4','q4c','q5','q5c','q6','q6c','q7','q7c','q8','q8c','q9','q9c','q10','q10c','q11','q12','q13','q14','q15','q16','q17','q17c','q18','q19','q20','q20c','q21','q21c','q22','q22c','q23','q23c','q24','q25','q26','q27','q28','q29','q29c','q30','q31','q32'):
                arr.append(request.form[val])
            cur = mysql.connection.cursor()
            arr = tuple(arr)
            cur.execute("SELECT * from closing where l_id=(%s)",(str(session['id'])))
            exist = cur.fetchone()
            if exist:
                flash('You have already submitted your closing form','danger')
            else:
                cur.execute(f"INSERT INTO closing VALUES {arr}")
                mysql.connection.commit()
                flash('Closing form sent!!!', 'success')
            return redirect(url_for('local_home'))
    if g.loggedin=='localobserver':
        return render_template('closing.html', title='Closing Form', form=form)
    return render_template('login.html', title='Welcome')


@app.route("/observer_home")
def observer_home():
    if g.loggedin=='observer':
        return render_template('observer_home.html', title='observer Home')
    return render_template('login.html', title='Welcome')


@app.route("/view_observerForms/<string:id>/")
def view_observerForms(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM opening WHERE l_id=(%s)", (id,))
    opening = cur.fetchall()
    cur.execute("SELECT * FROM voting where l_id=(%s)",(id))
    voting = cur.fetchall()
    cur.execute("SELECT * FROM closing where l_id=(%s)",(id))
    closing = cur.fetchall()
    return render_template('view_observerForms.html',opening=opening,voting=voting,closing=closing)


@app.route("/add_local", methods=['GET', 'POST'])
def add_local():
    form = RegistrationForm()
    # to be used for the drop down
    form.poll.choices = []        
    for row in polls_drop('polling', 'psname'):
        polls = str(row[0])
        form.poll.choices += [(polls, polls)]
    if request.method == 'POST':
        #Use the variable names of RegistrationCons() in form.py  
        if form.validate_on_submit():           
            fullname = request.form['fullname']
            tel = request.form['tel']
            poll = request.form['poll']
            email = request.form['email']
            hashed_password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
            lobs = 'localobserver'
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO login VALUES (%s, %s, %s)", (email, hashed_password,lobs))
            cur.execute(f"INSERT INTO local_obs(fname,telephone,email,pscode) VALUES (%s, %s, %s, %s)", (fullname,tel,email,poll))
            mysql.connection.commit()
            flash(f'Account created for {form.fullname.data} at {form.poll.data} Polling Station', 'success')
            return redirect(url_for('view_local'))
    if g.loggedin=='observer':
        return render_template('add_local.html', title='Register Local Observer', form=form)
    return render_template('login.html', title='Welcome')
#for drop polls down
def polls_drop(table_name, column):

        cur = mysql.connection.cursor()
        cur.execute("SELECT pscode FROM polling")
        return cur.fetchall()

@app.route("/add_observer", methods=['GET', 'POST'])
def add_observer():
    form = RegistrationObs()
    # to be used for the drop down
    form.constituency.choices = []        
    for row in cons_drop('constituency', 'cons_name'):
        cons = str(row[0])
        form.constituency.choices += [(cons, cons)]
    if request.method == 'POST':
        #Use the variable names of RegistrationCons() in form.py
        if form.validate_on_submit():
            fullname = request.form['fullname']
            tel = request.form['tel']
            constituency = request.form['constituency']
            email = request.form['email']
            hashed_password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
            obs = 'observer'
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO login VALUES (%s, %s, %s)", (email, hashed_password,obs))
            cur.execute(f"INSERT INTO observer(fname,telephone,email,cons_name ) VALUES (%s, %s, %s, %s)", (fullname, tel,email,constituency))
            mysql.connection.commit()
            flash(f'Account created for {form.fullname.data} at {form.constituency.data} Constituency', 'success')
            return redirect(url_for('view_observer'))
    if g.loggedin=='superobserver':
        return render_template('add_observer.html', title='Register Observer', form=form)
    return render_template('login.html', title='Welcome')
    

#for drop cons down
def cons_drop(table_name, column):
        cur = mysql.connection.cursor()
        cur.execute("SELECT cons_name FROM constituency")
        return cur.fetchall()



@app.route("/add_polls", methods=['GET', 'POST'])
def add_polls():
    poll = RegistrationPoll()
    # to be used for the drop down
    poll.constituency.choices = []        
    for row in cons_drop('constituency', 'cons_name'):
        cons = str(row[0])
        poll.constituency.choices += [(cons, cons)]

    if poll.validate_on_submit():
        if request.method == 'POST':
            #Use the variable names of RegistrationCons() in form.py
            name = request.form['name']
            cons = request.form['constituency']
            code = request.form['code']

            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO polling (pscode, psname, cons_name ) VALUES (%s, %s, %s)", (code, name, cons))
            mysql.connection.commit()
       
        flash(f'Polling stations is been created for  {poll.name.data} in {poll.constituency.data}!', 'success')
        return redirect(url_for('view_polls'))
    if g.loggedin=='observer':
        return render_template('add_polls.html', title='Register Local Observer', form=poll)
    return render_template('login.html', title='Welcome')



@app.route("/add_constituency", methods=['GET', 'POST'])
def add_constituency():
    cons = RegistrationCons()
    if cons.validate_on_submit():
        if request.method == 'POST':
            #Use the variable names of RegistrationCons() in form.py
            cons_name = request.form['name']
            cons_region = request.form['region']
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO constituency VALUES (%s, %s)", (cons_name, cons_region))
            mysql.connection.commit()
            # return 'Done!S'
        flash(f'Constituency is been created for  {cons.name.data}!', 'success')
        return redirect(url_for('view_constituency'))
    if g.loggedin=='superobserver':
        return render_template('add_constituency.html', title='Register Constituency', form=cons)
    return render_template('login.html', title='Welcome')
  
@app.route("/view_local", methods = ["POST", 'GET'])
def view_local():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM local_obs")
    local = cur.fetchall()
    if g.loggedin=='observer':
        return render_template('view_local.html', title='List of Local Observers', local=local)
    return render_template('login.html', title='Welcome')

@app.route("/view_polls", methods = ["POST", 'GET'])
def view_polls():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM polling")
    polls = cur.fetchall()
    if g.loggedin=='observer':
        return render_template('view_polls.html', local_observer=polls)
    return render_template('login.html', title='Welcome')

    # return render_template('view_local.html', title='List of Local Observers')


@app.route("/view_super_polls")
def view_super_polls():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM polling")
    polls = cur.fetchall()
    if g.loggedin=='superobserver':
        return render_template('view_super_polls.html', title='List of Polling Stations', local_observer=polls)
    return render_template('login.html', title='Welcome')

@app.route("/view_constituency")
def view_constituency():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM constituency")
    cons = cur.fetchall()
    if g.loggedin=='superobserver':
        return render_template('view_constituency.html', title='List of Constituency',cons=cons)
    return render_template('login.html', title='Welcome')

@app.route("/local_reports")
def local_reports():
    if g.loggedin=='observer':
        return render_template('local_reports.html', title='Reports')
    return render_template('login.html', title='Welcome')

@app.route("/super_reports")
def super_reports():
    if g.loggedin=='superobserver':
        return render_template('super_reports.html', title='Reports')
    return render_template('login.html', title='Welcome')
    
@app.route("/super_home")
def super_home():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    count_cons= cursor.execute("SELECT * FROM constituency") 
    count_obs= cursor.execute("SELECT * FROM observer") 
    count_polls= cursor.execute("SELECT * FROM polling") 
    count_local= cursor.execute("SELECT * FROM local_obs") 
<<<<<<< HEAD
    if g.loggedin=='superobserver':
        return render_template('super_home.html', title='Super Observer Home',count_cons=count_cons,count_obs=count_obs, count_polls=count_polls, count_local=count_local )
=======
    voting1= cursor.execute("SELECT * FROM voting WHERE l_id = 1")
    voting2= cursor.execute("SELECT * FROM voting WHERE l_id = 2") 
    voting3= cursor.execute("SELECT * FROM voting WHERE l_id = 3")
    voting4= cursor.execute("SELECT * FROM voting WHERE l_id = 4")
    voting5= cursor.execute("SELECT * FROM voting WHERE l_id = 5")
    voting6= cursor.execute("SELECT * FROM voting WHERE l_id = 6")
    voting7= cursor.execute("SELECT * FROM voting WHERE l_id = 7")
    voting8= cursor.execute("SELECT * FROM voting WHERE l_id = 8")
    voting9= cursor.execute("SELECT * FROM voting WHERE l_id = 9")

    count_opening= cursor.execute("SELECT * FROM opening") 
    count_voting= cursor.execute("SELECT * FROM voting") 
    count_closing= cursor.execute("SELECT * FROM closing") 



    if g.loggedin:
        return render_template('super_home.html', title='Super Observer Home',count_cons=count_cons,count_obs=count_obs, count_polls=count_polls, count_local=count_local, 
                                voting1=voting1,
                                voting2=voting2,
                                voting3=voting3,
                                voting4=voting4,
                                voting5=voting5,
                                voting6=voting6,
                                voting7=voting7,
                                voting8=voting8,
                                voting9=voting9,
                                
                                count_opening=count_opening,
                                count_voting=count_voting,
                                count_closing=count_closing

                                 )

>>>>>>> 87305061992c9d0da0db661ae4ac1e774129dd25
    return render_template('login.html', title='Welcome')
    

@app.route("/view_observer")
def view_observer():
    cur = mysql.connection.cursor()
    cur.execute("SELECT fname,telephone,email,cons_name FROM observer")
    observer = cur.fetchall()
    if g.loggedin=='superobserver':
        return render_template('view_observer.html', title='List of Observers',observer=observer)
    return render_template('login.html', title='Welcome')

@app.route("/super_tables")
def super_tables():
    if g.loggedin=='superobserver':
        return render_template('super_tables.html', title='Tables')
    return render_template('login.html', title='Welcome')

if __name__ == '__main__':
    app.run(debug=True)