from django.shortcuts import render
from django.db.models import Q, CharField, Value
from itertools import chain

from .models import Ticket, Review
from .forms import TicketCreateForm
from authentification.models import UserFollows

# Create your views here.
def index(request):

	followed_users = UserFollows.objects.filter(user__exact=request.user)
	tickets = Ticket.objects.filter(Q(user__id__in=followed_users.values_list('followed_user')) | Q(user__exact=request.user))
	reviews = Review.objects.filter(Q(user__id__in=followed_users.values_list('followed_user')) | Q(user__exact=request.user))

	tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
	reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

	posts = sorted(
		chain(reviews, tickets),
		key=lambda post: post.time_created,
		reverse=True
	)

	return render(request, 'reviews/index.html', {'posts': posts})

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

def create(request, ticket_id: int = None):
	pass