from django.utils.translation import ugettext as _
from django.views.generic.base import TemplateView
from apps.porsuk.models import Package, Component


class IndexView(TemplateView):
    title = _("Site Index")
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        from collections import OrderedDict

        context = super(IndexView, self).get_context_data(**kwargs)

        repo = 'core'
        component_dict = {}
        total_packages = Package.objects.all().count()

        components = Component.objects.filter(repo__name=repo)

        for component_item in components:
            component_key = component_item.component.split('.')[0]

            if component_key not in component_dict:
                component_dict[component_key] = {
                    'component': component_key,
                    'url': '/%s/packages/%s' % (repo, component_key),
                    'summary': ''}

        sorted_component_dict = OrderedDict(sorted(component_dict.items(), key=lambda t: t[0]))

        recently_updated_packages = Package.objects.filter(source__repo__name=repo).order_by('-source__updated_at')[:12]
        forgotten_packages = Package.objects.filter(source__repo__name=repo).order_by('source__updated_at')[:12]

        context['repo'] = repo
        context['components'] = sorted_component_dict.values()
        context['component_name'] = ''
        context['total_packages'] = total_packages
        context['recently_updated_packages'] = recently_updated_packages
        context['forgotten_packages'] = forgotten_packages

        # print context
        return context