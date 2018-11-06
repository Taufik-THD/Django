from django.conf import settings
import jwt

class User_authorization:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        response = self.get_response(request)
        return response
        
    def verify_token(self, request, view_func, view_args, view_kwargs):
        headers = request.META.get('HTTP_TOKEN')
            
        try:
            decode = jwt.decode(str(headers), 'secret_token', algorithms=['HS256'])
            return None
        except:
            return HttpResponse('Please input a valid token..')