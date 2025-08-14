import json
from datetime import datetime
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .forms import PredictionForm
from .models import PredictionHistory
from .services import OpenMeteoClient


class IndexView(FormView):
    template_name = 'prediction/index.html'
    form_class = PredictionForm
    success_url = reverse_lazy('prediction:index')

    def form_valid(self, form):
        location = form.cleaned_data['location']
        day = form.cleaned_data['date']

        geo = OpenMeteoClient.geocode(location)
        if not geo:
            context = self.get_context_data(form=form, error='Location not found')
            return self.render_to_response(context)

        prob, payload = OpenMeteoClient.daily_rain_probability(geo['lat'], geo['lon'], day)

        history = PredictionHistory.objects.create(
            user=self.request.user if self.request.user.is_authenticated else None,
            location=f"{geo['name']}, {geo.get('country', '')}".strip(', '),
            date=day,
            rain_chance=prob if prob is not None else None,
            raw_payload=payload or {},
        )

        context = self.get_context_data(
            form=self.form_class(),
            result={'probability': prob, 'geo': geo, 'date': day},
            history=history
        )
        return self.render_to_response(context)


class HistoryView(ListView):
    model = PredictionHistory
    template_name = 'prediction/history.html'
    context_object_name = 'items'
    paginate_by = 20

    def get_queryset(self):
        return PredictionHistory.objects.filter(user=self.request.user)


@method_decorator(csrf_exempt, name='dispatch')
class PredictAPIView(View):
    """
    JSON API endpoint:
    POST -> { location: str, date: 'YYYY-MM-DD' } returns rain probability
    GET  -> Health check
    """

    def get(self, request, *args, **kwargs):
        return JsonResponse({
            "status": "ok",
            "message": "Use POST with JSON body {location, date} to get predictions."
        })

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            location = data.get('location')
            date_str = data.get('date')

            if not location or not date_str:
                return JsonResponse({'error': 'Missing location or date'}, status=400)

            day = datetime.strptime(date_str, '%Y-%m-%d').date()

            geo = OpenMeteoClient.geocode(location)
            if not geo:
                return JsonResponse({'error': 'Location not found'}, status=404)

            prob, payload = OpenMeteoClient.daily_rain_probability(
                geo['lat'], geo['lon'], day
            )

            PredictionHistory.objects.create(
                user=None,
                location=f"{geo['name']}, {geo.get('country', '')}".strip(', '),
                date=day,
                rain_chance=prob,
                raw_payload=payload or {},
            )

            return JsonResponse({
                'location': geo['name'],
                'country': geo.get('country'),
                'date': day.isoformat(),
                'rain_chance_percent': prob,
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)