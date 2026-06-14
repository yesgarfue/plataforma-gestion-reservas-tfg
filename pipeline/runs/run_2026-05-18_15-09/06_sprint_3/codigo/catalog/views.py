from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q
from datetime import datetime, timedelta
from .models import Barco, Categoria, Puerto, Fabricante


class BarcoListView(ListView):
    model = Barco
    template_name = 'catalog/list.html'
    context_object_name = 'barcos'
    paginate_by = 12

    def get_queryset(self):
        queryset = Barco.objects.all()
        
        # Búsqueda por nombre
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(Q(nombre__icontains=search) | Q(descripcion__icontains=search))
        
        # Filtro por categoría
        categoria_id = self.request.GET.get('categoria', '')
        if categoria_id:
            queryset = queryset.filter(categoria_id=categoria_id)
        
        # Filtro por puerto
        puerto_id = self.request.GET.get('puerto', '')
        if puerto_id:
            queryset = queryset.filter(puerto_id=puerto_id)
        
        # Filtro por fabricante
        fabricante_id = self.request.GET.get('fabricante', '')
        if fabricante_id:
            queryset = queryset.filter(fabricante_id=fabricante_id)
        
        # Filtro por precio
        precio_min = self.request.GET.get('precio_min', '')
        precio_max = self.request.GET.get('precio_max', '')
        if precio_min:
            try:
                queryset = queryset.filter(precio_dia__gte=float(precio_min))
            except ValueError:
                pass
        if precio_max:
            try:
                queryset = queryset.filter(precio_dia__lte=float(precio_max))
            except ValueError:
                pass
        
        # Filtro por capacidad
        capacidad_min = self.request.GET.get('capacidad_min', '')
        if capacidad_min:
            try:
                queryset = queryset.filter(capacidad__gte=int(capacidad_min))
            except ValueError:
                pass
        
        return queryset.order_by('nombre')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        context['puertos'] = Puerto.objects.all()
        context['fabricantes'] = Fabricante.objects.all()
        context['search'] = self.request.GET.get('search', '')
        context['categoria_id'] = self.request.GET.get('categoria', '')
        context['puerto_id'] = self.request.GET.get('puerto', '')
        context['fabricante_id'] = self.request.GET.get('fabricante', '')
        context['precio_min'] = self.request.GET.get('precio_min', '')
        context['precio_max'] = self.request.GET.get('precio_max', '')
        context['capacidad_min'] = self.request.GET.get('capacidad_min', '')
        return context


class BarcoDetailView(DetailView):
    model = Barco
    template_name = 'catalog/detail.html'
    context_object_name = 'barco'
    pk_url_kwarg = 'id'
