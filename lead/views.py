import csv

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.views import View
from django.db.models import Q

from client.models import Client
from task.models import Task
from .models import Lead, Comment, LeadFile
from .forms import AddCommentForm, AddFileForm


# Create your views here.
# Lead list
class LeadListView(ListView):
    model = Lead

    def get_queryset(self):
        queryset = super(LeadListView, self).get_queryset()
        queryset = queryset.filter(created_by=self.request.user, converted_to_client=False)

        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(last_name__icontains=query) |
                Q(company__icontains=query) |
                Q(email__icontains=query)
            )
        return queryset


# Lead detail page
class LeadDetailView(LoginRequiredMixin, DetailView):
    model = Lead

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AddCommentForm()
        context['tasks'] = Task.objects.filter(lead_id=self.kwargs.get('pk'))
        context['fileform'] = AddFileForm()
        context['comments'] = Comment.objects.filter(lead_id=self.kwargs.get('pk'))

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
            messages.success(request, "Comment added successfully.")
        else:
            messages.error(request, "Failed to add comment. Please try again.")

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


# Bulk delete leads
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


# Convert lead to client
def convert_lead_to_client(request, lead_id):
    # Retrieve the Lead instance by ID
    lead = get_object_or_404(Lead, id=lead_id)

    # Create a new Client based on the Lead
    Client.objects.create(
        company=lead.company,
        first_name=lead.first_name,
        last_name=lead.last_name,
        email=lead.email,
        phone=lead.phone,
        status=lead.status_sale,
        description=lead.description,
        created_at=lead.created_at,
        created_by=lead.created_by,
    )

    # Delete the Lead instance from the database
    lead.delete()

    # Set success message and redirect (adjust URL as needed)
    messages.success(request, f"Lead {lead.last_name} {lead.first_name} has been converted to a client.")
    return redirect("client:list")


# Delete lead comment
@login_required
def delete_comment(request, lead_id, comment_id):
    lead = get_object_or_404(Lead, id=lead_id)
    comment = get_object_or_404(Comment, id=comment_id, lead=lead)

    # Optional: Only allow the creator of the comment or an admin to delete it
    if request.user == comment.created_by or request.user.is_staff:
        comment.delete()
        messages.success(request, "Comment deleted successfully.")
    else:
        messages.error(request, "You do not have permission to delete this comment.")

    return redirect('lead:detail', pk=lead.id)


# Edit Comment View
class EditCommentView(LoginRequiredMixin, View):
    def post(self, request, lead_id, comment_id):
        lead = get_object_or_404(Lead, id=lead_id)
        comment = get_object_or_404(Comment, id=comment_id, lead=lead)

        # Restrict to the owner or an admin
        if request.user != comment.created_by and not request.user.is_staff:
            return HttpResponseForbidden("You are not authorized to edit this comment.")

        # Update the comment
        content = request.POST.get("content")
        if content:
            comment.content = content
            comment.save()
            messages.success(request, "Comment updated successfully.")
        else:
            messages.error(request, "Content cannot be empty.")

        return redirect('lead:detail', pk=lead_id)


# Delete lead file
def delete_file(request, lead_id, file_id):
    if request.method == "POST":
        lead = get_object_or_404(Lead, id=lead_id)
        file_instance = get_object_or_404(LeadFile, id=file_id, lead=lead)
        file_instance.delete()
        messages.success(request, "File deleted successfully.")
    return redirect('lead:detail', pk=lead_id)








