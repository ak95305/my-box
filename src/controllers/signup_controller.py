from flask import Response, json, request
import smtplib
from marshmallow import Schema, fields, ValidationError

from src import session

from src.models.user import User

def unique_email(value):
    if session.query(User).filter_by(email=value).first():
        raise ValidationError(f"Email '{value}' is already taken.")

class SignupSchema(Schema):
    first_name = fields.String(required=True)
    last_name = fields.String(required=False)
    email = fields.Email(required=True, validate=[unique_email])
    password = fields.String(required=True)
    disk_storage = fields.Integer(required=True)

def signup():
    data = request.get_json()
    signup_schema = SignupSchema()

    try:
        result = signup_schema.load(data)
    except ValidationError as err:
        print(err.messages)

        return Response(
            response=json.dumps({
                'status': True, 
                "message": err.messages
            }),
            status=400,
            mimetype='application/json'
        )

    user = User.create(data)
    
    # smtp = smtplib.SMTP('smtp.zoho.in', 587)
    # smtp.starttls()
    # smtp.login('amanhere@zohomail.in', 'aman70482')
    # message = "Username: "+user.username+", OTP: "+str(user.otp)
    # smtp.sendmail("amanhere@zohomail.in", user.email, message)
    # smtp.quit()

    if(user):
        return Response(
            response=json.dumps({
                'status': True, 
                "message": 'Please Verfiy Your Email!',
                "data": user.to_dict(),
            }),
            status=200,
            mimetype='application/json'
        )
    else:
        return Response(
            response=json.dumps({'status': False, "message": 'Something\'s Wrong!'}),
            status=400,
            mimetype='application/json'
        )
    

def verify_otp(token):
    data = request.get_json()
    otp = data['otp']

    user = User.getRow({"token": token, "otp": otp})
    
    if(user):
        return Response(
            response=json.dumps({
                'status': True, 
                "message": "User Verfied!"
            }),
            status=200,
            mimetype='application/json'
        )
