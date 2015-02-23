from django.utils.translation import ugettext as _
from django.views.generic.base import TemplateView
from apps.porsuk.models import Package, Component
from django.core.paginator import Paginator

class IndexView(TemplateView):
    title = _("Site Index")
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        from collections import OrderedDict

        context = super(IndexView, self).get_context_data(**kwargs)

        repo = 'pisilinux-1.0'
        component_dict = {}
        package_count = Package.objects.count()

        for component_item in Component.objects.all():
            component_key = component_item.component.split('.')[0]

            if component_key not in component_dict:
                component_dict[component_key] = {
                    'component': component_key,
                    'url': '/%s/packages/%s' % (repo, component_key),
                    'summary': ''}

        recently_updated_packages = Package.objects.all().order_by('-source__updated_at')[:12]


        sorted_component_dict = OrderedDict(sorted(component_dict.items(), key=lambda t: t[0]))

        context['repo'] = repo
        context['components'] = sorted_component_dict.values()
        context['component_name'] = ''
        context['package_count'] = package_count
        context['recently_updated_packages'] = recently_updated_packages

        # print context
        return context