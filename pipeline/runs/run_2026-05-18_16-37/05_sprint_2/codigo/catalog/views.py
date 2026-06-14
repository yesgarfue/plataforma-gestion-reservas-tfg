from django.shortcuts import render, get_object_or_404
from django.views import View
from django.db.models import Q
from .models import Barco, Categoria, Puerto, Fabricante

class BarcoListView(View):
    def get(self, request):
        barcos = Barco.objects.all()
        categorias = Categoria.objects.all()
        puertos = Puerto.objects.all()
        fabricantes = Fabricante.objects.all()

        # Búsqueda por nombre
        search = request.GET.get('search', '')
        if search:
            barcos = barcos.filter(Q(nombre__icontains=search))

        # Filtros
        categoria_id = request.GET.get('categoria')
        if categoria_id:
            barcos = barcos.filter(categoria_id=categoria_id)

        puerto_id = request.GET.get('puerto')
        if puerto_id:
            barcos = barcos.filter(puerto_id=puerto_id)

        fabricante_id = request.GET.get('fabricante')
        if fabricante_id:
            barcos = barcos.filter(fabricante_id=fabricante_id)

        precio_min = request.GET.get('precio_min')
        if precio_min:
            try:
                barcos = barcos.filter(precio_dia__gte=float(precio_min))
            except ValueError:
                pass

        precio_max = request.GET.get('precio_max')
        if precio_max:
            try:
                barcos = barcos.filter(precio_dia__lte=float(precio_max))
            except ValueError:
                pass

        capacidad_min = request.GET.get('capacidad_min')
        if capacidad_min:
            try:
                barcos = barcos.filter(capacidad__gte=int(capacidad_min))
            except ValueError:
                pass

        # Agrupar por categoría
        barcos_por_categoria = {}
        for barco in barcos:
            if barco.categoria.nombre not in barcos_por_categoria:
                barcos_por_categoria[barco.categoria.nombre] = []
            barcos_por_categoria[barco.categoria.nombre].append(barco)

        context = {
            'barcos': barcos,
            'barcos_por_categoria': barcos_por_categoria,
            'categorias': categorias,
            'puertos': puertos,
            'fabricantes': fabricantes,
            'search': search,
        }
        return render(request, 'catalog/list.html', context)

class BarcoDetailView(View):
    def get(self, request, id):
        barco = get_object_or_404(Barco, id=id)
        return render(request, 'catalog/detail.html', {'barco': barco})
