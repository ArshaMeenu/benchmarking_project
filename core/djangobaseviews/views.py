from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from .forms import BaseViewForm
from .models import BaseViewModel


class BaseView(View):
    form_class = BaseViewForm
    template_name = 'baseview.html'

    def get(self, request):
        queryset = BaseViewModel.objects.all().order_by('-created_at')
        return render(request, self.template_name, {'form': self.form_class(), 'data': queryset})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            queryset = BaseViewModel.objects.all().order_by('-created_at')
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            data = BaseViewModel(title=title, description=description)
            data.save()
            return render(request, self.template_name,
                          {'form': form, 'data': queryset, 'message': 'Data added successfully.'})


class DeleteView(View):
    template_name = 'baseview.html'

    def dispatch(self, request, *args, **kwargs):
        BaseViewModel.objects.filter(id=self.kwargs['id']).delete()
        return redirect('create-read-view')


class UpdateView(View):
    template_name = 'baseview.html'
    form_class = BaseViewForm

    def get(self, request, pk):
        obj = get_object_or_404(BaseViewModel, pk=pk)
        form = self.form_class(instance=obj)
        return render(request, self.template_name, {'form': form})

    def put(self, request, pk):
        obj = get_object_or_404(BaseViewModel, pk=pk)
        form = self.form_class(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('create-read-view')
        return render(request, self.template_name, {'form': form})

