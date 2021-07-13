from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

# Create your views here.
@require_http_methods(['GET'])
def home(request):
    print("Access: ", request.META.get("ACCESSTOKEN"))
    return JsonResponse({"msg": "Hello " + str(request.user)})