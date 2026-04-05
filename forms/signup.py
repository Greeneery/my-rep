from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length


class SignupForm(FlaskForm):
    name = StringField("Username", validators=[DataRequired()])
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=8, max=100)]
    )
    password2 = PasswordField("Confirm Password", validators=[EqualTo("password")])
    submit = SubmitField("Sign Up")
