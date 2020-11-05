from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField, TimeField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    fullname = StringField('Fullname',
                        validators=[DataRequired(), Length(min=2, max=50)])
    tel = StringField('Telephone',
                           validators=[DataRequired(), Length(min=7, max=15)])
                        
    poll = SelectField('Polling Station Code', validators=[DataRequired(), Length(min=2, max=50)],
                                choices=[])     
    email = StringField('Email',validators=[DataRequired(), Email(),
                        Length(min=2, max=50)
    ])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')

class RegistrationPoll(FlaskForm):
    name = StringField('Name of Polling Station',
                           validators=[DataRequired(), Length(min=2, max=50)])
    constituency = SelectField('Constituency', validators=[DataRequired(), Length(min=2, max=50)],
                                choices=[])     
    code = StringField('Polling Station Code',
                           validators=[DataRequired(), Length(min=2, max=50)])

    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class OpeningForm(FlaskForm):
    arrivaltime = TimeField('Arrival Time(HH:MMam/pm)',format="%H:%M",validators=[DataRequired()])
    departuretime = TimeField('Departure Time(HH:MMam/pm)',format="%H:%M",validators=[DataRequired()])
    submit = SubmitField('Submit Form')

class VotingForm(FlaskForm):
    arrivaltime = TimeField('Arrival Time(HH:MMam/pm)',format="%H:%M",validators=[DataRequired()])
    departuretime = TimeField('Departure Time(HH:MMam/pm)',format="%H:%M",validators=[DataRequired()])
    submit = SubmitField('Submit Form')

class ClosingForm(FlaskForm):
    arrivaltime = TimeField('Arrival Time(HH:MMam/pm)',format="%H:%M",validators=[DataRequired()])
    departuretime = TimeField('Departure Time(HH:MMam/pm)',format="%H:%M",validators=[DataRequired()])
    submit = SubmitField('Submit Form')

class RegistrationCons(FlaskForm):
    name = StringField('Name of Constituency',
                           validators=[DataRequired(), Length(min=2, max=50)] )
    region = StringField('Region',
                           validators=[DataRequired(), Length(min=1, max=50)] )

    submit = SubmitField('Submit')


class RegistrationObs(FlaskForm):
    fullname = StringField('Fullname',
                           validators=[DataRequired(), Length(min=2, max=50)])
    tel = StringField('Telephone',
                           validators=[DataRequired(), Length(min=7, max=15)])
 
    
    constituency = SelectField('Constituency', validators=[DataRequired(), Length(min=2, max=20)],
                               choices=[] )                    


    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')