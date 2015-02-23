from collections import OrderedDict
from django.contrib.admin.views.main import ChangeList
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext as _
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from apps.porsuk.models import Component, Package, Repo, Source

ChangeList

class PackageListView(ListView):
    title = _("Packages")
    model = Package
    paginate_by = 30
    context_object_name = 'packages'
    template_name = 'packages.html'

    def get_queryset(self):
        qs = super(PackageListView, self).get_queryset()

        repo = self.kwargs.get('repo', None)
        component = self.kwargs.get('component', None)
        q = self.request.GET.get('q')
        components = Component.objects.filter(repo__name=repo)

        if component:
            components = components.filter(component__startswith=component)

        if q:
            qs = qs.filter(Q(name__icontains=q) |
                           Q(source__summary__icontains=q) |
                           Q(source__description__icontains=q))

        ordering = self.request.GET.get('o', '-source__updated_at')
        if ordering:
            qs = qs.order_by(ordering)

        qs = qs.filter(source__component__in=components)

        return qs

    def get_context_data(self, **kwargs):
        context = super(PackageListView, self).get_context_data(**kwargs)
        adjacent_pages = 3

        repo = self.kwargs.get('repo', None)
        component = self.kwargs.get('component', None)

        components = Component.objects.filter(repo__name=repo)

        if component:
            components = components.filter(component__startswith=component)

        component_dict = {}
        component_parts = []

        if component:
            component_parts = component.split('.')

        for component_item in components:
            component_item_parts = component_item.component.split('.')

            if len(component_item_parts) > len(component_parts):
                component_key = component_item.component.split('.')[len(component_parts)]

                if component_key not in component_dict:
                    component_dict[component_key] = {
                        'component': component_key,
                        'url': '/%s/packages/%s' % (repo, '.'.join(component_parts+[component_key])),
                        'summary': component_item.summary}

        sorted_components = OrderedDict(sorted(component_dict.items(), key=lambda t: t[0]))

        total_packages = Package.objects.filter(source__repo__name=repo).count()

        page_numbers = [n for n in \
                    range(context['page_obj'].number - adjacent_pages, context['page_obj'].number + adjacent_pages + 1) \
                    if n > 0 and n <= context['paginator'].num_pages]

        context.update({
            'repo': repo,
            'component': component,
            'components': sorted_components.values(),
            'q': self.request.GET.get('q'),
            'total_packages': total_packages,
            'page_numbers': page_numbers,
            'ordering': self.request.GET.get('o', None)
        })

        return context






class ComponentsView(ListView):
    title = _("Site Index")
    model = Package
    paginate_by = 30
    context_object_name = 'packages'
    template_name = 'index.html'

    def get_queryset(self):
        qs = super(ComponentsView, self).get_queryset()

        repo = self.kwargs.get('repo', '1.0')
        component_name = self.kwargs.get('component_name', None)
        components = Component.objects.filter(repo__name=repo)

        if component_name:
            components = components.filter(component__startswith=component_name)


        qs = qs.filter(source__component__in=components)

        return qs

    def get_context_data(self, **kwargs):
        context = super(ComponentsView, self).get_context_data(**kwargs)

        repo_name = get_object_or_404(Repo, name=self.kwargs.get('repo', '1.0'))

        component_name = self.kwargs.get('component_name', None)

        components = Component.objects.filter(repo__name=repo_name)

        if component_name:
            components = components.filter(component__startswith=component_name)
            component_spl = component_name.split('.')
        else:
            component_spl = []

        component_list = []
        component_dict = {}

        for component_item in components:
            l = len(component_spl)
            sl = len(component_item.component.split('.'))

            if sl > l:
                component_key = component_item.component.split('.')[l]

                if component_key not in component_dict:

                    summary = None

                    component_list.append({
                        'component': component_key.title(),
                        'url': '/%s/components/%s/' % (repo_name, '.'.join(component_spl+[component_key])),
                        'summary': component_item.summary
                })

                component_dict[component_key] = {}

        context.update({
            'repo': repo_name,
            'components': component_list,
            'component_name': component_name
        })

        return context


class PackageView(DetailView):
    model = Package
    slug_field = 'slug'
    template_name = 'packages.html'

    def get_queryset(self):
        qs = super(PackageView, self).get_queryset()

        repo = self.kwargs.get('repo', None)
        slug = self.kwargs.get('slug', None)

        self.kwargs['slug'] = '%s-%s'%(slug, repo)
        # components = Component.objects.filter(repo__name=repo)
        #
        # if component_name:
        #     components = components.filter(component__startswith=component_name)
        #
        #
        # qs = qs.filter(source__component__in=components)

        print self.kwargs

        return qs

    def get_context_data(self, **kwargs):
        context = super(PackageView, self).get_context_data(**kwargs)
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