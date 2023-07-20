from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, FormView,
                                  ListView, TemplateView, UpdateView)
from multiupload.fields import MultiFileField

from .forms import ContactForm
from .models import Contact, ContactFile


class ContactListView(ListView):
    model = Contact
    template_name = 'contact_list.html'
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ContactListView, self).get_context_data(**kwargs)
        contact = self.get_queryset()
        page = self.request.GET.get('page')
        paginator = Paginator(contact, self.paginate_by)
        try:
            contact = paginator.page(page)
        except PageNotAnInteger:
            contact = paginator.page(1)
        except EmptyPage:
            contact = paginator.page(paginator.num_pages)
        context['contact'] = contact
        return context


class ContactDetailView(DetailView):
    model = Contact
    template_name = 'contact_detail.html'
    context_object_name = 'contact'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['signed_by'] = 'arshameenu'
        return context

    def get_object(self, queryset=None):
        obj = super().get_object()
        obj.email = 'arsha@genercisapp.com'
        obj.save()
        return obj


class ContactCreateView(CreateView):
    model = Contact
    template_name = 'contact_create.html'
    fields = ('name', 'email', 'address', 'phone')
    success_url = reverse_lazy('list-view')


class ContactUpdateView(UpdateView):
    model = Contact
    template_name = 'contact_create.html'
    fields = ('name', 'email', 'address', 'phone')
    context_object_name = 'contact'

    def get_success_url(self):
        return reverse_lazy('detail-view', kwargs={'pk': self.object.id})


class ContactDeleteView(DeleteView):
    model = Contact
    template_name = 'contact_delete.html'
    success_url = reverse_lazy('list-view')


class ContactFormView(FormView):
    template_name = 'contact_form.html'
    form_class = ContactForm
    success_url = reverse_lazy('list-view')

    # def form_valid(self, form):
    #     form.save()
    #     return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST or None,request.FILES or None)
        files = request.FILES.getlist('files')
        print('file',files)
        if form.is_valid():
            contact = form.save()
            if files:
                for file in files:
                    # ContactFile.objects.create(contact =contact,file=file)
                    pass
                    # with open('/home/sayone/ArshaMeenu_files/courses/benchmarking_project/core/media/documents/' +
                    # file.name, 'wb') as destination: print('destination',destination) for chunk in file.chunks():
                    # destination.write(chunk)
            return redirect('list-view')
        else:
            return redirect('form-view')


class ContactTemplateView(TemplateView):
    template_name = 'contact_template.html'
