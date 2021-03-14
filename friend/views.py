from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Friend
from .forms import FriendForm


""" View for the Index """
class IndexView(generic.TemplateView):

    template_name = 'index.html'

""" View for the Friend List """
class FriendListView(LoginRequiredMixin, generic.ListView):

    template_name = 'friend_list.html'
    context_object_name = 'friends'

    # making the data from database sending to the html file 
    def get_queryset(self):
        friends = Friend.objects.filter(user=self.request.user).order_by('friend_name')
        return friends
    
""" View for Displaying the Detail of the Event """
class FriendDetailView(LoginRequiredMixin, generic.DetailView):

    template_name = 'friend_detail.html'
    model = Friend
    context_object_name = 'friend'

    # making data for sending to html file
    def get_context_data(self, **kwargs):
        # get primary key of the friend and user information from the url
        pk = self.kwargs.get('pk')
        user = self.request.user
        context = super().get_context_data()
        # get the events information of the friend
        friend = Friend.objects.filter(pk=pk, user=user)
        events = friend[0].event_set.order_by('-date')
        context['last_5_events'] = events[:5] # last 5 events
        context['event_count'] = len(events) # the counts of played with the friend
        return context

""" View for Displaying List of the Event played with the Friend """
class FriendEventListView(LoginRequiredMixin, generic.TemplateView):

    template_name = 'friend_event_list.html'

    # making data for sending to html file
    def get_context_data(self, **kwargs):
        # get primary key of the friend and user information from the url
        pk = self.kwargs.get('pk')
        user = self.request.user
        context = super().get_context_data()
        # get the events information of the friend
        friend = Friend.objects.filter(pk=pk, user=user)
        events = friend[0].event_set.order_by('-date')
        context['events'] = events
        context['event_count'] = len(events) # the counts of played with the friend
        context['friend_name'] = friend[0].friend_name
        return context

""" View for Creating Friend """
class FriendCreateView(LoginRequiredMixin, generic.CreateView):

    template_name = 'friend_create.html'
    model = Friend
    form_class = FriendForm
    success_url = reverse_lazy('friend:friend_list') # the url redirect to when the input of the form is valid

    # save the data in database if the input of the form is valid
    def form_valid(self, form):
        friend = form.save(commit=False)
        friend.user = self.request.user # add user information
        friend.save()
        return super().form_valid(form)
    
    # display error message if the input of the form is invalid
    def form_invalid(self, form):
        return super().form_invalid(form)

""" View for Updating the Friend """
class FriendUpdateView(LoginRequiredMixin, generic.UpdateView):

    template_name = 'friend_update.html'
    model = Friend
    form_class = FriendForm
    context_object_name = 'friend'

    # determine the url redirect to when the input of the form is valid
    def get_success_url(self):
        return reverse_lazy('friend:friend_detail', 
        kwargs={'pk': self.kwargs['pk']})
    
    # redirect to the url if the input of the form is valid
    def form_valid(self, form):
        return super().form_valid(form)
    
    # display error message if the input of the form is invalid
    def form_invalid(self, form):
        return super().form_invalid(form)
    
""" View for Deleting the Friend """
class FriendDeleteView(LoginRequiredMixin, generic.DeleteView):

    template_name = 'friend_delete.html'
    model = Friend
    success_url = reverse_lazy('friend:friend_list') # the url redirect to when the input of the form is valid
    context_object_name = 'friend'

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)