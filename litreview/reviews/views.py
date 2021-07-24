from django.shortcuts import render
from django.http import HttpResponse

from .models import Ticket, Request
from .forms import TicketCreateForm
from authentification.models import UserFollows

# Create your views here.
def index(request):

	FollowedUsers = UserFollows.objects.filter(user__exact=request.user)
	Tickets = Ticket.objects.filter(user__exact=request.user)
	Requests = Request.objects.filter(user__exact=request.user)

	print(FollowedUsers)

	return render(request, 'reviews/index.html')

def ask(request):
	if request.method == "POST":
		form = TicketCreateForm(request.POST, request.FILES)

		if form.is_valid():
			req = Ticket()
			req.title = form.cleaned_data['title']
			req.description = form.cleaned_data['description']
			req.image = form.cleaned_data['image']
			req.user = request.user
			req.save()
		else:
			print(form.errors)
	else:
		form = TicketCreateForm()
	return render(request, 'reviews/ask.html', {'form': form})