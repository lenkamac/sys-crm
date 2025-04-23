import csv

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from client.forms import AddCommentForm, AddFileForm
from client.models import Client


# Create your views here.
class ClientListView(ListView):
    model = Client

    def get_queryset(self):
        queryset = super(ClientListView, self).get_queryset()
        return queryset.filter(created_by=self.request.user)


# Client detail page
class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AddCommentForm()
        context['fileform'] = AddFileForm()
        return context

    def get_queryset(self):
        queryset = super(ClientDetailView, self).get_queryset()
        return queryset.filter(created_by=self.request.user, pk=self.kwargs.get('pk'))


# Comment view
class AddCommentView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')

        form = AddCommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.created_by = request.user
            comment.client_id = pk
            comment.save()

        return redirect('client:detail', pk=pk)


# File view
class AddFileView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')

        form = AddFileForm(request.POST, request.FILES)

        if form.is_valid():
            file = form.save(commit=False)
            file.client_id = pk
            file.created_by = request.user
            file.save()

        return redirect('client:detail', pk=pk)


# Create a new client
class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    success_url = reverse_lazy('client:list')
    fields = ('company', 'first_name', 'last_name','phone', 'address', 'city', 'country', 'zipcode', 'email', 'description',
                  'status')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.save()

        return redirect(self.get_success_url())


# Delete client from his detail page
class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('client:list')

    def get_queryset(self):
        queryset = super(ClientDeleteView, self).get_queryset()
        return queryset.filter(created_by=self.request.user, pk=self.kwargs.get('pk'))

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


# Update client
class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Client'
        return context

    fields = ('company', 'first_name', 'last_name', 'phone','email', 'address', 'city', 'zipcode', 'description',
              'status')
    success_url = reverse_lazy('client:list')

    def get_queryset(self):
        queryset = super(ClientUpdateView, self).get_queryset()
        return queryset.filter(created_by=self.request.user, pk=self.kwargs.get('pk'))


# Export leads in csv
@login_required
def clients_export(request):
    clients =Client.objects.filter(created_by=request.user)

    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="clients.csv"'},
    )

    writer = csv.writer(response)
    writer.writerow(['Last name', 'First name', 'Phone', 'Email', 'Description', 'Created at', 'Created by'])

    for client in clients:
        writer.writerow([client.last_name, client.first_name, client.phone, client.email, client.description,
                         client.created_at, client.created_by])

    return response


# Bulk delete clients
@login_required
def clients_bulk_delete(request):
    if request.method == "POST":
        client_ids = request.POST.getlist("client_ids")  # Get selected lead IDs as a list
        selected_clients = request.POST.getlist('client_ids')

        if client_ids:
            # Delete leads that belong to the requesting user
            Client.objects.filter(id__in=client_ids, created_by=request.user).delete()

            messages.success(request, 'Selected clients were deleted successfully.')
        elif selected_clients:
            Client.objects.filter(id__in=selected_clients).delete()
            messages.success(request, 'Selected clients have been deleted successfully.')
        else:
            messages.warning(request, 'No clients were selected.')

    return redirect('client:list')

