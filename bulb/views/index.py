from django.http import HttpResponse
from bulb.views.verify import Verification
import robot

__author__ = "hellojohn201@gmail.com"

def index(request):
    if request.method == "GET":
        return handle_get(request)
    elif request.method == "POST":
        return handle_post(request)
    else:
        return None

def handle_get(request):
    # TODO: move token to settings file.
    query = request.GET.dict()
    token = "funshionwebsys"
    result = Verification(query, token).do_verify()
    return HttpResponse(result, content_type="text/plain")

def handle_post(request):
    reply = robot.handle(request.body)
    return HttpResponse(reply, content_type="application/xml")

