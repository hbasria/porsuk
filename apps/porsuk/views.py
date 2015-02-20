from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext as _
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from apps.porsuk.models import Component, Package, Repo, Source

class ComponentsView(ListView):
    title = _("Site Index")
    model = Package
    paginate_by = 30
    context_object_name = 'packages'
    template_name = 'index.html'

    def get_queryset(self):
        qs = super(ComponentsView, self).get_queryset()

        component_or_package = self.kwargs.get('component_or_package', 'system')
        components = Component.objects.filter(component__startswith=component_or_package)

        qs = qs.filter(source__component__in=components)
        return qs

    def get_context_data(self, **kwargs):
        context = super(ComponentsView, self).get_context_data(**kwargs)

        repo = get_object_or_404(Repo, name=self.kwargs.get('repo', '1.0'))
        component_or_package = self.kwargs.get('component_or_package', 'system')
        component_or_package_spl = component_or_package.split('.')
        components = Component.objects.filter(component__startswith=component_or_package)
        component_list = []
        component_dict = {}

        print component_or_package

        for component_item in components:
            l = len(component_or_package_spl)
            sl = len(component_item.component.split('.'))

            if sl > l:
                component_key = component_item.component.split('.')[l]

                if component_key not in component_dict:
                    component_list.append({
                        'component': component_key.title(),
                        'url': '/%s/components/%s.%s/' % (repo, '.'.join(component_or_package_spl), component_key),
                        'summary': '...'
                })

                component_dict[component_key] = {}

        context.update({
            'repo': repo,
            'components': component_list,
        })

        return context


class PackageView(DetailView):
    model = Package
    slug_field = 'slug'
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(PackageView, self).get_context_data(**kwargs)

        print context

        return context







def index(request, repo='1.1', component_or_package=None):
    repo = Repo.objects.filter(name=repo)
    repo = None if not repo else repo[0]

    components = None
    packages = None
    source = None
    package = None
    runtime_deps = None
    similar_packages = None
    q = request.GET.get('q', None)

    component = Component.objects.filter(component__contains=component_or_package)
    component = None if not component else component[0]

    if component:
        packages = Package.objects.filter(source__component=component)
    else:

        if q:
            packages = Package.objects.filter(name__contains=q)


        if request.path.startswith('/source/'):
            source = Source.objects.filter(name=component_or_package)
            source = None if not source else source[0]

        if not source:
            package = Package.objects.filter(name=component_or_package)
            package = None if not package else package[0]

        if package:
            runtime_deps = package.runtime_dep.all()
            similar_packages = Package.objects.filter(Q(source__name__iexact=package.name) | Q(source__description__iexact=package.name)).exclude(name=package.name)

        else:
            components = Component.objects.all()



    return render(request, 'index.html', {
        'repo': repo,
        'component': component,
        'source': source,
        'package': package,
        'components': components,
        'packages': packages,
        'similar_packages': similar_packages,
        'runtime_deps': runtime_deps,
    })



def packages(request, repo='1.1', component=None):

    repo = Repo.objects.filter(name=repo)
    if repo:
        repo = repo[0]

    component = Component.objects.filter(component=component)
    if component:
        component = component[0]



    packages = Package.objects.filter(source__component=component)

    return render(request, 'porsuk/index.html', {
        'repo': repo,
        'component': component,
        'packages': packages,
    })


def source_detail(request, repo='1.0', component=None, source=None):
    repo = Repo.objects.filter(name=repo)
    repo = None if not repo else repo[0]

    component = Component.objects.filter(component=component)
    component = None if not component else component[0]

    source = Source.objects.filter(name=source)
    source = None if not source else source[0]

    return render(request, 'porsuk/index.html', {
        'repo': repo,
        'component': component,
        'source': source,
    })


def package_detail(request, repo='1.1', component=None, package=None):
    repo = Repo.objects.filter(name=repo)
    repo = None if not repo else repo[0]

    component = Component.objects.filter(component=component)
    component = None if not component else component[0]

    package = Package.objects.filter(name=package)
    package = None if not package else package[0]
    runtime_deps = None

    if package:
        runtime_deps = package.runtime_dep.all()

    return render(request, 'porsuk/index.html', {
        'repo': repo,
        'component': component,
        'package': package,
        'runtime_deps': runtime_deps,
    })