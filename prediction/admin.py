from django.contrib import admin
from .models import PredictionHistory

@admin.register(PredictionHistory)
class PredictionHistoryAdmin(admin.ModelAdmin):
    list_display = ("user", "location", "date", "rain_chance", "created_at")
    search_fields = ("user__username", "location")
    list_filter = ("date", "created_at")
