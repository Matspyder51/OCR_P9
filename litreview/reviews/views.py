from django.shortcuts import render
from django.http import HttpResponse

from .models import Ticket, Request
from authentification.models import UserFollows

# Create your views here.
def index(request):

	FollowedUsers = UserFollows.objects.filter(user__exact=request.user)
	Tickets = Ticket.objects.filter(user__exact=request.user)
	Requests = Request.objects.filter(user__exact=request.user)

	print(FollowedUsers)

	return render(request, 'reviews/index.html')

def ask(request):
	return render(request, 'reviews/ask.html')