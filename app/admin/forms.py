from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, Email
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ..models import Department, Role, MenuItems, Stalls, Location

class DepartmentForm(FlaskForm):
    """
    Form for admin to add or edit a department
    """
    name = StringField('Name', validators=[DataRequired(),Length(max=25)])
    description = StringField('Description', validators=[DataRequired(),Length(max=255)])
    submit = SubmitField('Submit')

class RoleForm(FlaskForm):
    """
    Form for admin to add or edit a role
    """
    name = StringField('Name', validators=[DataRequired(),Length(max=25)])
    description = StringField('Description', validators=[DataRequired(),Length(max=255)])
    submit = SubmitField('Submit')

class EmployeeAssignForm(FlaskForm):
    """
    Form for admin to assign departments and roles to employees
    """
    department = QuerySelectField(query_factory=lambda: Department.query.all(),
                                  get_label="name")
    role = QuerySelectField(query_factory=lambda: Role.query.all(),
                            get_label="name")
    submit = SubmitField('Submit')

class MenuForm(FlaskForm):
    """
    Form for admin to add menu items related to stall
    """
    name = StringField('Name', validators=[DataRequired(),Length(max=25)])
    description = StringField('Description',validators=[Length(max=255)])
    price = IntegerField('Price', validators=[DataRequired()])
    stall = QuerySelectField(query_factory=lambda: Stalls.query.all(), 
                            get_label="name")
    location = QuerySelectField(query_factory=lambda: Location.query.all(), 
                                get_label="location")

class StallsForm(FlaskForm):
    """
    Form for admin to register stalls for the respective location
    """
    name = StringField('Name', validators=[DataRequired(),Length(max=25)])
    description = StringField('Description',validators=[Length(max=255)])
    ownername = StringField('OwnerName', validators=[DataRequired(),Length(max=25)])
    contact_number = StringField('ContactNumber', validators=[Length(max=25)])
    mobile_number = StringField('MobileNumber', validators=[DataRequired(),Length(max=25)])
    address = StringField('Address', validators=[DataRequired(),Length(max=255)])
    notes = StringField('Notes', validators=[Length(max=255)])
    location = QuerySelectField(query_factory=lambda: Location.query.all(), 
                                get_label='location', 
                                allow_blank=True, 
                                blank_text=(u'Select a location'), 
                                get_pk=lambda x: x.id)
    submit = SubmitField('Submit')

class CustomerForm(FlaskForm):
    """
    Form for admin to add customer details
    """
    name = StringField('Name', validators=[DataRequired(),Length(max=25)])
    mobile_number = StringField('MobileNumber', validators=[DataRequired(),Length(max=25)])
    email_id = StringField('EmailId',validators=[Email(message='Please enter a valid email id!')])
    submit = SubmitField('Submit')

class StatusForm(FlaskForm):
    """
    Form for admin to add customer details
    """
    name = StringField('UniqueStatusName', validators=[DataRequired(),Length(max=25)])
    submit = SubmitField('Submit')