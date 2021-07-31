from django.shortcuts import redirect, render
from django.db.models import Q, CharField, Value
from itertools import chain

from .models import Ticket, Review
from .forms import TicketCreateForm, ReviewForm
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
		form = TicketCreateForm()
	return render(request, 'reviews/ask.html', {'form': form})

def create(request, ticket_id = None):
	context = {}

	if ticket_id is not None:
		ticket = Ticket.objects.get(id__exact=ticket_id)
		as_reviewed = Review.objects.filter(user__exact=request.user, ticket_id__exact=ticket_id)
		if len(as_reviewed) > 0:
			return redirect('reviews:index')
		context['ticket'] = ticket
		context['form'] = ReviewForm()
	else:
		context["ticket_form"] = TicketCreateForm()
		context['form'] = ReviewForm()

	if request.method == "POST":
		form = ReviewForm(request.POST)

		ticket = None
		if ticket_id is not None:
			ticket = Ticket.objects.get(id__exact=ticket_id)
		else:
			form2 = TicketCreateForm(request.POST, request.FILES)

			if form2.is_valid():
				req = Ticket()
				req.title = form2.cleaned_data['title']
				req.description = form2.cleaned_data['description']
				req.image = form2.cleaned_data['image']
				req.user = request.user
				req.save()
				ticket = req

		if form.is_valid():
			rev = Review()
			rev.headline = form.cleaned_data['headline']
			rev.body = form.cleaned_data['body']
			rev.rating = form.cleaned_data['rating']
			rev.ticket = ticket
			rev.user = request.user
			rev.save()
			return redirect('reviews:index')
	
	return render(request, 'reviews/create.html', context)

def edit(request, review_id: int):
	review = Review.objects.get(id__exact=review_id)
	if request.method =="POST":
		form = ReviewForm(request.POST)
		if form.is_valid():
			review.headline = form.cleaned_data['title']
			review.body = form.cleaned_data['body']
			review.rating = form.cleaned_data['rating']
			review.save()
			return redirect('reviews:index')

	form = ReviewForm()
	form.fields['title'].initial = review.headline
	form.fields['body'].initial = review.body
	form.fields['rating'].initial = review.rating

	return render(request, 'reviews/edit.html', {'form': form, 'review': review, 'ticket': Ticket.objects.get(id__exact=review.ticket.id)})

def edit_ticket(request, ticket_id: int):
	pass

def delete_review(request, review_id: int):
	rev = Review.objects.get(id__exact=review_id)
	rev.delete()

	return redirect('reviews:me')

def delete_ticket(request, ticket_id: int):
	ticket = Ticket.objects.get(id__exact=ticket_id)

	ticket.delete()

	return redirect('reviews:me')

def user_posts(request):
	tickets = Ticket.objects.filter(user__exact=request.user)
	reviews = Review.objects.filter(user__exact=request.user)

	tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
	reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

	posts = sorted(
		chain(reviews, tickets),
		key=lambda post: post.time_created,
		reverse=True
	)

	return render(request, 'reviews/me.html', {'posts': posts})