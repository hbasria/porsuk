from django.utils.translation import ugettext as _
from django.views.generic.base import TemplateView
from apps.porsuk.models import Package, Component
from django.core.paginator import Paginator

class IndexView(TemplateView):
    title = _("Site Index")
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        repo = '1.0'
        components = []
        component_dict = {}
        package_count = Package.objects.count()

        for component_item in Component.objects.all():
            component_key = component_item.component.split('.')[0]

            if component_key not in component_dict:
                components.append({
                'component': component_key.title(),
                'url': '/%s/components/%s' % (repo, component_key),
                'summary': '...'
            })

            component_dict[component_key] = {}

        context['repo'] = repo
        context['components'] = components
        context['package_count'] = package_count
        return context