from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Barco, Categoria, Puerto, Fabricante
from django.core.paginator import Paginator
from datetime import datetime, timedelta


class HomeView(View):
    def get(self, request):
        barcos = Barco.objects.filter(activo=True).select_related('categoria', 'puerto', 'fabricante')
        categorias = Categoria.objects.all()
        puertos = Puerto.objects.all()
        fabricantes = Fabricante.objects.all()
        
        # Búsqueda por nombre
        search_query = request.GET.get('search', '')
        if search_query:
            barcos = barcos.filter(Q(nombre__icontains=search_query))
        
        # Filtro por categoría
        categoria_id = request.GET.get('categoria')
        if categoria_id:
            barcos = barcos.filter(categoria_id=categoria_id)
        
        # Filtro por puerto
        puerto_id = request.GET.get('puerto')
        if puerto_id:
            barcos = barcos.filter(puerto_id=puerto_id)
        
        # Filtro por fabricante
        fabricante_id = request.GET.get('fabricante')
        if fabricante_id:
            barcos = barcos.filter(fabricante_id=fabricante_id)
        
        # Filtro por precio
        precio_min = request.GET.get('precio_min')
        precio_max = request.GET.get('precio_max')
        if precio_min:
            try:
                barcos = barcos.filter(precio_dia__gte=float(precio_min))
            except (ValueError, TypeError):
                pass
        if precio_max:
            try:
                barcos = barcos.filter(precio_dia__lte=float(precio_max))
            except (ValueError, TypeError):
                pass
        
        # Filtro por capacidad
        capacidad_min = request.GET.get('capacidad_min')
        if capacidad_min:
            try:
                barcos = barcos.filter(capacidad__gte=int(capacidad_min))
            except (ValueError, TypeError):
                pass
        
        # Filtro por rango de fechas (solo marca disponibilidad)
        fecha_inicio_str = request.GET.get('fecha_inicio')
        fecha_fin_str = request.GET.get('fecha_fin')
        
        # Agrupar por categoría
        barcos_por_categoria = {}
        for barco in barcos:
            cat_nombre = barco.categoria.nombre
            if cat_nombre not in barcos_por_categoria:
                barcos_por_categoria[cat_nombre] = []
            barcos_por_categoria[cat_nombre].append(barco)
        
        context = {
            'barcos': barcos,
            'barcos_por_categoria': barcos_por_categoria,
            'categorias': categorias,
            'puertos': puertos,
            'fabricantes': fabricantes,
            'search_query': search_query,
            'categoria_id': categoria_id,
            'puerto_id': puerto_id,
            'fabricante_id': fabricante_id,
            'precio_min': precio_min,
            'precio_max': precio_max,
            'capacidad_min': capacidad_min,
            'fecha_inicio': fecha_inicio_str,
            'fecha_fin': fecha_fin_str,
        }
        return render(request, 'catalog/home.html', context)


class BarcoListView(ListView):
    model = Barco
    template_name = 'catalog/list.html'
    context_object_name = 'barcos'
    paginate_by = 12

    def get_queryset(self):
        queryset = Barco.objects.filter(activo=True).select_related('categoria', 'puerto', 'fabricante')
        
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(Q(nombre__icontains=search_query))
        
        categoria_id = self.request.GET.get('categoria')
        if categoria_id:
            queryset = queryset.filter(categoria_id=categoria_id)
        
        puerto_id = self.request.GET.get('puerto')
        if puerto_id:
            queryset = queryset.filter(puerto_id=puerto_id)
        
        fabricante_id = self.request.GET.get('fabricante')
        if fabricante_id:
            queryset = queryset.filter(fabricante_id=fabricante_id)
        
        precio_min = self.request.GET.get('precio_min')
        if precio_min:
            try:
                queryset = queryset.filter(precio_dia__gte=float(precio_min))
            except (ValueError, TypeError):
                pass
        
        precio_max = self.request.GET.get('precio_max')
        if precio_max:
            try:
                queryset = queryset.filter(precio_dia__lte=float(precio_max))
            except (ValueError, TypeError):
                pass
        
        capacidad_min = self.request.GET.get('capacidad_min')
        if capacidad_min:
            try:
                queryset = queryset.filter(capacidad__gte=int(capacidad_min))
            except (ValueError, TypeError):
                pass
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        context['puertos'] = Puerto.objects.all()
        context['fabricantes'] = Fabricante.objects.all()
        context['search_query'] = self.request.GET.get('search', '')
        context['categoria_id'] = self.request.GET.get('categoria')
        context['puerto_id'] = self.request.GET.get('puerto')
        context['fabricante_id'] = self.request.GET.get('fabricante')
        context['precio_min'] = self.request.GET.get('precio_min')
        context['precio_max'] = self.request.GET.get('precio_max')
        context['capacidad_min'] = self.request.GET.get('capacidad_min')
        return context


class BarcoDetailView(DetailView):
    model = Barco
    template_name = 'catalog/detail.html'
    context_object_name = 'barco'
    pk_url_kwarg = 'id'

    def get_queryset(self):
        return Barco.objects.filter(activo=True).select_related('categoria', 'puerto', 'fabricante')
