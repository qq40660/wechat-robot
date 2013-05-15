from django.http import HttpResponse
from bulb.views.verify import Verification
from message import Message, TextMessage
from robot import Robot
import cacti


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
    print request.body
    message = TextMessage.from_xml(request.body)
    bot = Robot()
    bot.add_handler(cacti.handler)
    reply = bot.get_reply(message)
    return HttpResponse(reply, content_type="application/xml")

