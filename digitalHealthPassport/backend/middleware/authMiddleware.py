import json
import jwt

from django.http import JsonResponse


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self,request):
        # This gets the root url from .path
        urlPathL = list(filter(None,request.path_info.split('/')))
        
        # Checks to see if this is for the favicon
        if len(urlPathL) < 2:
            return self.get_response(request)
        urlPath = f'/{urlPathL[0]}/{urlPathL[1]}'
        res = {}

        if urlPath == '/api/testing':
            # res will either have a response object = error
            # or it will be a None type = success
            res = self.handleJWT(request)

        # return response
        if not res:
            response = self.get_response(request)
            # Successful res will pass it to the next api
            return response
        else:
            return JsonResponse(res)
    
    def handleJWT(self, req):
        # Checks if jwt is in the headers
        # If no jwt then it will return a pre made response
        if 'jwt' not in req.headers:
            return {
                "success": False,
                "msg": "No token provided"
            }
        else:
            try:
                # It will try to decode the jwt 
                # if successful then it will return nothing
                token = req.headers['jwt']
                payload = jwt.decode(token, 'servsat1324jm', algorithms=['HS256'])
                print('Token Verified!')
            except:
                # If token cannot be decoded then it will return a pre made response
                print('Token Expired')
                return {
                    "success": False,
                    "msg": "Token is expired"
                }