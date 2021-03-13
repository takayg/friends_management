from django.shortcuts import render, redirect
from django.views import generic
from .models import Event, Friend
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
import datetime, calendar
from .forms import EventForm, DateForm
from django.urls import reverse_lazy

class CalendarRedirectView(LoginRequiredMixin, generic.RedirectView):
    date_now = datetime.datetime.now()
    url = '/event/calendar/' + str(date_now.year) + '/' + str(date_now.month)

class CalendarView(LoginRequiredMixin, generic.FormView):
    template_name = 'calendar.html'
    date_now = datetime.datetime.now()
    form_class = DateForm

    def get_context_data(self, **kwargs):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        weeks = calendar.monthcalendar(year, month)
        schedule_dic = {}

        for week in weeks:
            for day in week:
                if day == 0:
                    continue
                schedule = Event.objects.filter(user=self.request.user, date=datetime.date(year, month, day))
                schedule_dic[day] = schedule

        context = super().get_context_data()
        context['weeks'] = weeks
        context['schedule_dic'] = schedule_dic
        context['year'] = year
        context['month'] = month
        context['prev_year'] = year - 1 if month == 1 else year
        context['prev_month'] = month - 1 if month > 1 else 12
        context['next_year'] = year + 1 if month == 12 else year
        context['next_month'] = month + 1 if month < 12 else 1

        date_now = datetime.datetime.now()
        context['today'] = date_now.day
        context['today_flag'] = False
        if year == date_now.year and month == date_now.month:
            context['today_flag'] = True
        return context

    def form_valid(self, form):
        year = form.data.get('year')
        month = form.data.get('month')
        # リダイレクト先のパスを取得する
        url = reverse_lazy('event:calendar', kwargs={'year': year, 'month': month})
        return redirect(url)
    
    def form_invalid(self, form):
        return super().form_invalid(form)

class EventCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'event_create.html'
    model = Event
    form_class = EventForm

    def form_valid(self, form):
        event = form.save(commit=False)
        event.user = self.request.user
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        event.date = datetime.date(year, month, day)
        event.save()
        url = reverse_lazy('event:add_friend', kwargs={'pk': event.pk})
        return redirect(url)
    
    def form_invalid(self, form):
        return super().form_invalid(form)

@login_required
def add_friend(request, pk):
    user = request.user
    event = Event.objects.get(pk=pk)
    if request.method == 'GET':
        friends = Friend.objects.filter(user=user).order_by('friend_name')
        if friends:
            context = {'friends': friends}
            return render(request, 'add_friend.html', context)
        else:
            url = reverse_lazy('event:event_detail', kwargs={'pk': pk})
            return redirect(url)

    else:
        friends_id = request.POST.getlist("choice")
        for id in friends_id:
            event.friend_name.add(Friend.objects.get(id=int(id)))
        event.save()
        url = reverse_lazy('event:event_detail', kwargs={'pk': pk})
        return redirect(url)

class EventDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'event_detail.html'
    model = Event
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk')
        context = super().get_context_data()
        event = Event.objects.filter(pk=pk)
        friends = event[0].friend_name.all()
        context['friends_name'] = friends
        return context

class EventUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'event_update.html'
    model = Event
    form_class = EventForm
    context_object_name = 'event'

    def get_success_url(self):
        return reverse_lazy('event:update_friend', 
        kwargs={'pk': self.kwargs['pk']})
    
    def form_valid(self, form):
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return super().form_invalid(form)

@login_required
def update_friend(request, pk):
    user = request.user
    event = Event.objects.get(pk=pk)
    if request.method == 'GET':
        friends = Friend.objects.filter(user=user).order_by('friend_name')
        context = {'friends': friends}
        return render(request, 'add_friend.html', context)
    else:
        friends_id = request.POST.getlist("choice")
        event.friend_name.clear()
        for id in friends_id:
            event.friend_name.add(Friend.objects.get(id=int(id)))
        event.save()
        url = reverse_lazy('event:event_detail', kwargs={'pk': pk})
        return redirect(url)

class EventDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = 'event_delete.html'
    model = Event
    success_url = reverse_lazy('event:calendar_redirect')
    context_object_name = 'event'

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)