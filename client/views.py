import csv

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from client.forms import AddCommentForm, AddFileForm
from client.models import Client, Comment, ClientFile
from task.models import Task


# Create your views here.
# Client list
class ClientListView(ListView):
    model = Client

    def get_queryset(self):
        queryset = super(ClientListView, self).get_queryset()
        queryset = queryset.filter(created_by=self.request.user)

        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(last_name__icontains=query) |
                Q(company__icontains=query) |
                Q(email__icontains=query)
            )
        return queryset


# Client detail page
class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AddCommentForm()
        context['tasks'] = Task.objects.filter(client_id=self.kwargs.get('pk'))
        context['fileform'] = AddFileForm()

        comment_list = Comment.objects.filter(client_id=self.kwargs.get('pk')).order_by('-created_at')
        paginator = Paginator(comment_list, 8)

        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['comments'] = page_obj

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
            messages.success(request, "Comment added successfully.")
        else:
            messages.error(request, "Failed to add comment. Please try again.")

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

# Delete client comment
@login_required
def delete_client_comment(request, client_id, comment_id):
    client = get_object_or_404(Client, id=client_id)
    comment = get_object_or_404(Comment, id=comment_id, client=client)

    # Optional: Only allow the creator of the comment or an admin to delete it
    if request.user == comment.created_by or request.user.is_staff:
        comment.delete()
        messages.success(request, "Comment deleted successfully.")
    else:
        messages.error(request, "You do not have permission to delete this comment.")

    return redirect('client:detail', pk=client.id)

# Edit Comment View
class EditCommentView(LoginRequiredMixin, View):
    def post(self, request, client_id, comment_id):
        client = get_object_or_404(Client, id=client_id)
        comment = get_object_or_404(Comment, id=comment_id, client=client)

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

        return redirect('client:detail', pk=client_id)

# Delete lead file
def delete_client_file(request, client_id, file_id):
    if request.method == "POST":
        client = get_object_or_404(Client, id=client_id)
        file_instance = get_object_or_404(ClientFile, id=file_id, client=client)
        file_instance.delete()
        messages.success(request, "File deleted successfully.")
    return redirect('client:detail', pk=client_id)



