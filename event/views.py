from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
import datetime, calendar
from .models import Event, Friend
from .forms import EventForm, DateForm

""" View for Redirecting to Calendar with Today's Information """
class CalendarRedirectView(LoginRequiredMixin, generic.RedirectView):

    date_now = datetime.datetime.now() # today's information
    url = '/event/calendar/' + str(date_now.year) + '/' + str(date_now.month)

""" View for the Calendar """
class CalendarView(LoginRequiredMixin, generic.FormView):

    template_name = 'calendar.html'
    form_class = DateForm
    
    # making data for sending to html file
    def get_context_data(self, **kwargs):
        # get date from the url
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        # all dates in 2Darray
        weeks = calendar.monthcalendar(year, month) 
        # key:day value:all events of the day
        schedule_dic = {} 
        for week in weeks:
            for day in week:
                if day == 0:
                    continue
                schedule = Event.objects.filter(user=self.request.user, date=datetime.date(year, month, day))
                schedule_dic[day] = schedule
        # send data to html as a context
        context = super().get_context_data()
        context['weeks'] = weeks
        context['schedule_dic'] = schedule_dic
        # year and month of the specified date
        context['year'] = year
        context['month'] = month
        # previous month
        context['prev_year'] = year - 1 if month == 1 else year
        context['prev_month'] = month - 1 if month > 1 else 12
        # next month
        context['next_year'] = year + 1 if month == 12 else year
        context['next_month'] = month + 1 if month < 12 else 1
        # today's information
        date_now = datetime.datetime.now()
        context['today'] = date_now.day
        # flag Ture:this calendar includes today
        context['today_flag'] = False 
        if year == date_now.year and month == date_now.month:
            context['today_flag'] = True
        
        return context

    # redirect when date is specified by form and if the input is valid
    def form_valid(self, form):
        # get date from form
        year = form.data.get('year')
        month = form.data.get('month')
        # get the redirect path
        url = reverse_lazy('event:calendar', kwargs={'year': year, 'month': month})

        return redirect(url)
    
    # display error message if the input of the form is invalid
    def form_invalid(self, form):
        return super().form_invalid(form)

""" View for Creating Event """
class EventCreateView(LoginRequiredMixin, generic.CreateView):

    template_name = 'event_create.html'
    model = Event
    form_class = EventForm

    # save the data in database if the input of the form is valid
    def form_valid(self, form):
        event = form.save(commit=False)
        event.user = self.request.user # add user information
        # get the specified date from the url
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        event.date = datetime.date(year, month, day) # add date information
        event.save()
        # get the redirect path for adding friend information
        url = reverse_lazy('event:add_friend', kwargs={'pk': event.pk})

        return redirect(url)
    
    # display error message if the input of the form is invalid
    def form_invalid(self, form):
        return super().form_invalid(form)

""" View for Adding Friend Information """
@login_required
def add_friend(request, pk):
    user = request.user # get user information from http request
    event = Event.objects.get(pk=pk)
    # GET request : display the form
    if request.method == 'GET':
        # make choices to select friends
        friends = Friend.objects.filter(user=user).order_by('friend_name')
        # send the choice to the html file if some friends are registered
        if friends:
            context = {'friends': friends}
            return render(request, 'add_friend.html', context)
        # finish the process if no friends are registered
        else: 
            url = reverse_lazy('event:event_detail', kwargs={'pk': pk})
            return redirect(url)
    # POST request : save the friend information in database
    else:
        friends_id = request.POST.getlist("choice") # get the selected friends from the form
        for id in friends_id:
            event.friend_name.add(Friend.objects.get(id=int(id)))
        event.save()
        url = reverse_lazy('event:event_detail', kwargs={'pk': pk})
        return redirect(url)

""" View for Displaying the Detail of the Event """
class EventDetailView(LoginRequiredMixin, generic.DetailView):

    template_name = 'event_detail.html'
    model = Event
    context_object_name = 'event'

    # making data for sending to html file
    def get_context_data(self, **kwargs):
        # get primary key of the event from the url
        pk = self.kwargs.get('pk')
        context = super().get_context_data()
        # get the friends information of the event
        event = Event.objects.filter(pk=pk)
        friends = event[0].friend_name.all()
        context['friends_name'] = friends
        return context

""" View for Updating the Event """
class EventUpdateView(LoginRequiredMixin, generic.UpdateView):

    template_name = 'event_update.html'
    model = Event
    form_class = EventForm
    context_object_name = 'event'

    # determine the url redirect to when the input of the form is valid
    def get_success_url(self):
        return reverse_lazy('event:update_friend', 
        kwargs={'pk': self.kwargs['pk']})
    
    # redirect to the url if the input of the form is valid
    def form_valid(self, form):
        return super().form_valid(form)
    
    # display error message if the input of the form is invalid
    def form_invalid(self, form):
        return super().form_invalid(form)

""" View for Updating Friend Information of the Event """
@login_required
def update_friend(request, pk):
    # get the user information from the http request
    user = request.user
    # get the event informaion using the primary key from the url
    event = Event.objects.get(pk=pk)
    # GET request : display the form
    if request.method == 'GET':
        # make choices to select friends
        friends = Friend.objects.filter(user=user).order_by('friend_name')
        # send the choice to the html file if some friends are registered
        if friends:
            context = {'friends': friends}
            return render(request, 'add_friend.html', context)
        # finish the process if no friends are registered
        else: 
            url = reverse_lazy('event:event_detail', kwargs={'pk': pk})
            return redirect(url)
    # POST request : save the friend information in database
    else:
        friends_id = request.POST.getlist("choice") # get the selected friends from the form
        event.friend_name.clear() # delete once and choose from the beginning
        for id in friends_id:
            event.friend_name.add(Friend.objects.get(id=int(id)))
        event.save()
        url = reverse_lazy('event:event_detail', kwargs={'pk': pk})
        return redirect(url)

""" View for Deleting the Event """
class EventDeleteView(LoginRequiredMixin, generic.DeleteView):

    template_name = 'event_delete.html'
    model = Event
    success_url = reverse_lazy('event:calendar_redirect') # the url redirect to when the input of the form is valid
    context_object_name = 'event'

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)