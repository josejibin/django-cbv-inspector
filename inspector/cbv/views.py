# Create your views here.
from django.views.generic import DetailView
from cbv.models import Klass, Module, ProjectVersion
from django.http import HttpResponse,HttpResponseRedirect
from pprint import pformat,pprint

class KlassDetailView(DetailView):
    model = Klass

    def get_queryset(self):
        return super(DetailView, self).get_queryset().select_related()

    def get_object(self):
        return self.model.objects.get(
            name__iexact=self.kwargs['klass'],
            module__name__iexact=self.kwargs['module'],
            module__project_version__version_number__iexact=self.kwargs['version'],
            module__project_version__project__name__iexact=self.kwargs['package'],
        )


class ModuleDetailView(DetailView):
    model = Module
    push_state_url = None

    def get_object(self):
        try: 
            return self.model.objects.get(
                name=self.kwargs['module'],
                project_version__version_number=self.kwargs['version'],
                project_version__project__name=self.kwargs['package'],
            )
        except self.model.DoesNotExist:
            obj = self.model.objects.get(
                name__iexact=self.kwargs['module'],
                project_version__version_number__iexact=self.kwargs['version'],
                project_version__project__name__iexact=self.kwargs['package'],
            )
            self.push_state_url = obj.get_absolute_url()
            return obj

    def get_context_data(self, **kwargs):
        context = super(ModuleDetailView, self).get_context_data(**kwargs)
        context['push_state_url'] = self.push_state_url
        return context


class VersionDetailView(DetailView):
    model = ProjectVersion

    def get_object(self):
        return self.model.objects.get(
            version_number__iexact=self.kwargs['version'],
            project__name__iexact=self.kwargs['package'],
        )
