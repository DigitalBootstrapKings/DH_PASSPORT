from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..models import User, Vaccinated, CovidTest, Employee
import datetime

import requests
@api_view(['GET'])
def testApi(request):
    # emp = Employee(lastName='Doe', firstName='John', email='jdoe@yahoo.com', password='password')
    # emp.save()
    return Response({
        'success': True,
        'msg': 'Just trying some stuff out!'
    })

@api_view(['POST'])
def getProfile(request):
    # recieve unique id/user id
    id = request.data['userId']
    user = User.objects.get(id=id)
    r = requests.post('http://localhost:8000/api/user/checkStatus', data={"userId": id})

    return Response({
        'success': r.json()['success'],
        'msg': r.json()['msg'],
    })

@api_view(['POST'])
def scanUser(request):
    id = request.data['userId']
    r = requests.post('http://localhost:8000/api/user/checkStatus', data={"userId": id}).json()
    return Response({
        'success': r.json()['success'],
        'msg': r.json()['msg'],
    })



@api_view(['POST'])
def checkStatus(request):
    # recieve unique id/user id 
    # Retrieve user
    user = User.objects.get(id=request.data['userId'])
    
    # check vaccineStatus
    if user.vaccineStatus is True:
        vaccine = Vaccinated.objects.get(userId=user)
        datelimit = datetime.date.today() - datetime.timedelta(days=-7)

        if vaccine.vaccinationDate < datelimit:
            return Response({
                'success': True,
                'msg': 'User is safe!'
            })
        else:
            return Response({
                'success': False,
                'msg': 'User has been vaccinated but has not had enough time to let the effects show!'
            })

    # check if they have been exposed 
    if user.exposure is True:
        return Response({
            'success': False,
            'msg': 'User has been exposed recently!'
        })
    
    # check their covid test
    c_test = CovidTest.objects.get(userId=user)
    if c_test.testResults is True:
        return Response({
            'success': False,
            'msg': 'User has covid!'
        })


    c_datelimit = datetime.date.today() - datetime.timedelta(days=-7)
    if c_test.dateTaken > c_datelimit:
        return Response({
            'success': False,
            'msg': 'Users last covid test was to long ago! They must take another.'
        })
    
    return Response({
        'success': True,
        'msg': 'User is good to go!'
    })