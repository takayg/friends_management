from django.shortcuts import render
from django.views import generic
from .models import Friend
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import FriendForm
from django.urls import reverse_lazy

""" Home """
class IndexView(generic.TemplateView):
    template_name = 'index.html'

""" Friend List """
class FriendListView(LoginRequiredMixin, generic.ListView):
    template_name = 'friend_list.html'

    def get_queryset(self):
        friends = Friend.objects.filter(user=self.request.user).order_by('friend_name')
        return friends
    
    context_object_name = 'friends' # Templateで使う際にdefaultではobject_listなので変更

""" Friend Detail """
class FriendDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'friend_detail.html'
    model = Friend
    context_object_name = 'friend'

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk')
        context = super().get_context_data()
        friend = Friend.objects.filter(pk=pk)
        events = friend[0].event_set.order_by('-date')
        context['last_5_events'] = events[:5]
        context['event_count'] = len(events)
        return context

""" Friend Create """
class FriendCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'friend_create.html'
    model = Friend
    form_class = FriendForm
    success_url = reverse_lazy('friend:friend_list')

    def form_valid(self, form):
        friend = form.save(commit=False)
        friend.user = self.request.user
        friend.save()
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return super().form_invalid(form)

""" Friend Update """
class FriendUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'friend_update.html'
    model = Friend
    form_class = FriendForm
    context_object_name = 'friend'

    def get_success_url(self):
        return reverse_lazy('friend:friend_detail', 
        kwargs={'pk': self.kwargs['pk']})
    
    def form_valid(self, form):
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return super().form_invalid(form)
    
""" Friend Delete """
class FriendDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = 'friend_delete.html'
    model = Friend
    success_url = reverse_lazy('friend:friend_list')
    context_object_name = 'friend'

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)