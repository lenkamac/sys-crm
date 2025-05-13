import csv

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.views import View

from task.models import Task
from .models import Lead, LeadFile
from .forms import AddCommentForm, AddFileForm


# Create your views here.
# Lead list
class LeadListView(ListView):
    model = Lead

    def get_queryset(self):
        queryset = super(LeadListView, self).get_queryset()
        return queryset.filter(created_by=self.request.user, converted_to_client=False)


# Lead detail page
class LeadDetailView(LoginRequiredMixin, DetailView):
    model = Lead

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AddCommentForm()
        context['tasks'] = Task.objects.filter(lead_id=self.kwargs.get('pk'))
        context['fileform'] = AddFileForm()
        return context

    def get_queryset(self):
        queryset = super(LeadDetailView, self).get_queryset()
        return queryset.filter(created_by=self.request.user, pk=self.kwargs.get('pk'))


# Comment view
class AddCommentView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')

        form = AddCommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.created_by = request.user
            comment.lead_id = pk
            comment.save()

        return redirect('lead:detail', pk=pk)


# File view
class AddFileView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')

        form = AddFileForm(request.POST, request.FILES)

        if form.is_valid():
            file = form.save(commit=False)
            file.lead_id = pk
            file.created_by = request.user
            file.save()

        return redirect('lead:detail', pk=pk)


# Create a new lead
class LeadCreateView(LoginRequiredMixin, CreateView):
    model = Lead
    success_url = reverse_lazy('lead:list')
    fields = ('company', 'first_name', 'last_name','phone', 'address', 'city', 'country', 'zipcode', 'email', 'description',
                  'priority', 'status', 'status_sale')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.save()

        return redirect(self.get_success_url())


# Delete Lead from his detail page
class LeadDeleteView(LoginRequiredMixin, DeleteView):
    model = Lead
    success_url = reverse_lazy('lead:list')

    def get_queryset(self):
        queryset = super(LeadDeleteView, self).get_queryset()
        return queryset.filter(created_by=self.request.user, pk=self.kwargs.get('pk'))

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


# Lead update
class LeadUpdateView(LoginRequiredMixin, UpdateView):
    model = Lead

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Lead'
        return context

    fields = ('company', 'first_name', 'last_name', 'phone','email', 'address', 'city', 'zipcode', 'description',
              'priority', 'status', 'status_sale')
    success_url = reverse_lazy('lead:list')

    def get_queryset(self):
        queryset = super(LeadUpdateView, self).get_queryset()
        return queryset.filter(created_by=self.request.user, pk=self.kwargs.get('pk'))


# Export leads in csv
@login_required
def leads_export(request):
    leads = Lead.objects.filter(created_by=request.user)

    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="leads.csv"'},
    )

    writer = csv.writer(response)
    writer.writerow(['Last name', 'First name', 'Phone', 'Email', 'Description', 'Created at', 'Created by'])

    for lead in leads:
        writer.writerow([lead.last_name, lead.first_name, lead.phone, lead.email, lead.description,
                         lead.created_at, lead.created_by])

    return response


@login_required
def leads_bulk_delete(request):
    if request.method == "POST":
        lead_ids = request.POST.getlist("lead_ids")  # Get selected lead IDs as a list
        selected_leads = request.POST.getlist('lead_ids')

        if lead_ids:
            # Delete leads that belong to the requesting user
            Lead.objects.filter(id__in=lead_ids, created_by=request.user).delete()

            messages.success(request, 'Selected leads were deleted successfully.')
        elif selected_leads:
            Lead.objects.filter(id__in=selected_leads).delete()
            messages.success(request, 'Selected leads have been deleted successfully.')
        else:
            messages.warning(request, 'No leads were selected.')

    return redirect('lead:list')
