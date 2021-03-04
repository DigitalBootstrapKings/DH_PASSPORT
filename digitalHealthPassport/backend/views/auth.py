from rest_framework.decorators import api_view
from rest_framework.response import Response
from twilio.rest import Client
from datetime import datetime, timedelta


from ..models import User, CovidTest, Vaccinated, OneTimeText, Employee

import datetime
import bcrypt
import shortuuid
import requests
import jwt

SECRET_SID = 'AC2abdf90f0ef603f03502151d67c39998' 
AUTH_TOKEN = '70944a185d6eef67d2d5976c8a054543' 
JWT_KEY = 'servsat1324jm'

@api_view(['GET'])
def testApi(request):
    print('In the test API!!')
    t = datetime.datetime.utcnow() + timedelta(seconds=600)
    return Response({
        'success': True,
        'msg': 'Just trying some stuff out!'
    })

@api_view(['POST'])
def keyVerification(request):
    try:
        if request.data['type'] == 'vaccinated':
            status = 'vaccinated'
        else:
            status = 'covid_test'

        if status == 'vaccinated':
            # Here we will call a 3rd party API which will verify the given vaccination key
            # It should return OHIP number, last name, first name and Date of birth
            record = vaccinationAPI(request.data['v_key'])
            if(record['success'] == False):
                return Response({
                    'success': False,
                    'msg': 'Vaccination key provided is incorrect!'
                })
        else:
            record = covidTestAPI(request.data['c_key'])
            if(record['success'] == False):
                return Response({
                    'success': False,
                    'msg': 'Covid test key provided is incorrect!'
                })
        date_f = record['DOB'].split('/')
        date_t = datetime.date(int(date_f[2]), int(date_f[1]), int(date_f[0]))
        
        user = User(lastName=record['last_name'], firstName=record['first_name'], OHIP=record['OHIP'], DOB=date_t)
        if status == 'vaccinated':
            user.vaccineStatus = True
        user.save()
        
        date_f = record['date_taken'].split('/')
        date_t = datetime.date(int(date_f[2]), int(date_f[1]), int(date_f[0]))
        if status == 'covid_test':
            c_test = CovidTest(userId=user, dateTaken=date_t, testResults=record['result'])
            c_test.save()
        else:
            v_test = Vaccinated(userId=user, vaccinationDate=date_t, vaccinationType=record['type'])
            v_test.save()


        return Response({
            'success': True,
            'msg': 'Key successfully verified',
            'data': {
                'OHIP': record['OHIP'],
                'DOB': record['DOB']
            }
        })
    except:
        return Response({
            'success': False,
            'msg': 'Something went wrong...'
        })

        
@api_view(['POST'])
def identityVerification(request):
    try:
        users = User.objects.filter(OHIP=request.data['OHIP'], lastName=request.data['lastName'], firstName=request.data['firstName'])

        if users:
            return Response({
                "success": True,
                "msg": "Identity successfully verified!"
            })
        else:
            return Response({
                "success": False,
                "msg": "Identity could not be verified!"
            })
    except:
        return Response({
            'success': False,
            'msg': 'Something went wrong...'
        })

@api_view(['POST'])
def signup(request):
    try:
        users = User.objects.filter(email=request.data['email'])
        if users:
            return Response({
                'success': False,
                'msg': 'Email already registered!'
            })

        hashed = bcrypt.hashpw(request.data['password'].encode('utf8'), bcrypt.gensalt())
        user = User.objects.get(OHIP=request.data['OHIP'])
        user.email = request.data['email']
        user.phoneNumber = request.data['phoneNumber']
        user.password = hashed
        user.save()

        return Response({
            'success': True,
            'msg': 'User successfully registered',
        })
    except:
        return Response({
            'success': False,
            'msg': 'Something went wrong...'
        })
    
@api_view(['POST'])
def sendOneTimeText(request):
    try:
        phone = request.data['phoneNumber']
        # Generates a unique id
        u_id = shortuuid.ShortUUID().random(length=7)

        # Check the database for the users unique id with a value of not verified
        user = User.objects.get(phoneNumber=phone)
        db_text = OneTimeText.objects.filter(userId=user, stillValid=True)
        
        # If there is an entry of not verified - we change the status
        if db_text:
            db_text[0].stillValid = False
            db_text[0].save()

        # Store the uniqued id in the db
        un_text = OneTimeText(userId=user,oneTimeValue=u_id, stillValid=True)
        un_text.save()
        # Send a text message to the user containing the unique id
        client = Client(SECRET_SID, AUTH_TOKEN)
        message = client.messages.create(  
                                messaging_service_sid='MG57180d14384644fee5935dc3733225e2', 
                                body=f'Your one time key - {str(u_id)}',      
                                to=f'+1{phone}') 

        return Response({
            'success': True,
            'msg': 'Successfully sent a text!'
        })
    except:
        return Response({
            'success': False,
            'msg': 'Something went wrong...'
        })


@api_view(['POST'])
def verifyOneTimeText(request):
    try:   
        phone = request.data['phoneNumber']
        one_key = request.data['key']
        # Fetch user from db
        user = User.objects.get(phoneNumber=phone)

        # Query db to see if critrea fit
        db_text = OneTimeText.objects.filter(userId=user, stillValid=True, oneTimeValue=one_key)

        # If one time text is valid, change status to False
        # Assign a token to the user and save in db
        if db_text:
            db_text[0].stillValid = False
            db_text[0].save()
            # JWT only lasts for 10minutes
            payload = {
                'email': user.email,
                'exp': datetime.datetime.utcnow() + timedelta(seconds=600)
            }
            jwt_token = jwt.encode(payload, JWT_KEY, 'HS256')
            user.secureToken = jwt_token
            user.save()
            return Response({
                'success': True,
                'msg': 'Successfully logged user in!',
                "data": {
                    "token": jwt_token
                }
            })
        else:
            return Response({
                'success': False,
                'msg': 'Key not valid.'
            })
    except:
        return Response({
            'success': False,
            'msg': 'Something went wrong...'
        })

@api_view(['POST'])
def loginUser(request):
    try:
        users = User.objects.filter(email=request.data['email'])
        if users and bcrypt.checkpw(request.data['password'].encode('utf8'), users[0].password[2:-1].encode('utf8')):
            
            return Response({
                'success': True,
                'msg': 'Verified email and password!'
            })
        else:
            return Response({
                'success': False,
                'msg': 'Credentials incorrect!'
            })
    except:
        return Response({
            'success': False,
            'msg': 'Something went wrong...'
        })
@api_view(['POST'])
def loginEmployee(request):
    employees = Employee.objects.filter(email=request.data['email'])
    if employees and employees[0].password == request.data['password']:
        payload = {
                'email': employees[0].email,
                'exp': datetime.datetime.utcnow() + timedelta(seconds=600)
            }
        jwt_token = jwt.encode(payload, JWT_KEY, 'HS256')
        employees[0].secureToken = jwt_token
        employees[0].save()
        return Response({
                'success': True,
                'msg': 'Verified email and password!',
                 "data": {
                    "token": jwt_token
                }
        })
    else:
        return Response({
            'success': False,
            'msg': 'Incorrect credentials!'
        })

def vaccinationAPI(vaccine_key):
    faux_db = [
        {
            'vaccine_key': '123456789',
            'OHIP': '5584486674YM',
            'last_name': 'Walker',
            'first_name': 'Jean',
            'DOB': '15/12/1985',
            'date_taken': '21/02/2021',
            'type': 'Phizer'
        },
        {
            'vaccine_key': '178567338',
            'OHIP': '9084454674OP',
            'last_name': 'Mahmud',
            'first_name': 'Jemal',
            'DOB': '17/07/1995',
            'date_taken': '01/01/2021',
            'type': 'Phizer'
        },
        {
            'vaccine_key': '273400785',
            'OHIP': '0081484674YM',
            'last_name': 'Cage',
            'first_name': 'Nicholas',
            'DOB': '05/04/1973',
            'date_taken': '13/01/2021',
            'type': 'Moderna'
        },
        {
            'vaccine_key': '832547698',
            'OHIP': '3284480074YM',
            'last_name': 'Adam',
            'first_name': 'Sarah',
            'DOB': '23/02/2000',
            'date_taken': '23/01/2021',
            'type': 'Moderna'
        },
    ]

    for record in faux_db:
        if record['vaccine_key'] == vaccine_key:
            f_record = record
            record['success'] = True
    
    if f_record is None:
        return {
            'success': False
        }
    else:
        return f_record

def covidTestAPI(c_key):
    faux_db = [
        {
            'c_key': '123456789',
            'OHIP': '5584486674YM',
            'last_name': 'Walker',
            'first_name': 'Jean',
            'DOB': '15/12/1985',
            'result': True,
            'date_taken': '23/01/2021'
        },
        {
            'c_key': '178567338',
            'OHIP': '9084454674OP',
            'last_name': 'Mahmud',
            'first_name': 'Jemal',
            'DOB': '17/07/1995',
            'result': False,
            'date_taken': '13/01/2021'
        },
        {
            'c_key': '273400785',
            'OHIP': '0081484674YM',
            'last_name': 'Cage',
            'first_name': 'Nicholas',
            'DOB': '05/04/1973',
            'result': False,
            'date_taken': '01/01/2021'
        },
        {
            'c_key': '832547698',
            'OHIP': '3284480074YM',
            'last_name': 'Adam',
            'first_name': 'Sarah',
            'DOB': '23/02/2000',
            'result': True,
            'date_taken': '21/02/2021'
        },
    ]

    for record in faux_db:
        if record['c_key'] == c_key:
            f_record = record
            record['success'] = True
    
    if f_record is None:
        return {
            'success': False
        }
    else:
        return f_record