from django.shortcuts import render, get_object_or_404
from django.views.generic import View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from reservations.models import Reserva


class TrackingSearchView(View):
    template_name = 'tracking/search.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        codigo = request.POST.get('codigo', '').strip()
        if codigo:
            try:
                reserva = Reserva.objects.get(codigo_seguimiento=codigo)
                return render(request, 'tracking/detail.html', {'reserva': reserva})
            except Reserva.DoesNotExist:
                return render(request, self.template_name, {'error': 'Código de seguimiento no encontrado.'})
        return render(request, self.template_name, {'error': 'Por favor ingresa un código de seguimiento.'})


class TrackingDetailView(TemplateView):
    template_name = 'tracking/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        codigo = kwargs.get('codigo')
        reserva = get_object_or_404(Reserva, codigo_seguimiento=codigo)
        context['reserva'] = reserva
        return context


class MyReservationsView(LoginRequiredMixin, TemplateView):
    template_name = 'tracking/my_reservations.html'
    login_url = 'accounts:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reservas'] = Reserva.objects.filter(cliente=self.request.user).order_by('-created_at')
        return context
