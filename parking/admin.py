from django.contrib import admin
from .models import (
    ParkingModel,
    ParkingSpotModel,
    ReservationModel,
    AvailabilityModel,
)

class ParkingSpotAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "parking",
        "number",
        "owner",
        "occupied",
    )
    list_display_links = (
        "id",
        "parking",
        "number",
        "owner",
        "occupied",
    )
    list_filter = ("parking", "number", "owner", "occupied")
    search_fields = ("parking", "number", "owner", "occupied")
    ordering = ("parking", "number", "owner", "occupied")


class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ("id", "parking_spot", "available_from", "available_to", "cost_per_hour")
    list_display_links = ("id", "parking_spot", "available_from", "available_to", "cost_per_hour")
    list_filter = ("id", "parking_spot", "available_from", "available_to", "cost_per_hour")
    search_fields = ("id", "parking_spot", "available_from", "available_to", "cost_per_hour")
    ordering = ("id", "parking_spot", "available_from", "available_to", "cost_per_hour")


class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "parking_spot",
        "reserved_by",
        "started_at",
        "valid_until",
    )
    list_display_links = (
        "id",
        "parking_spot",
        "reserved_by",
        "started_at",
        "valid_until",
    )
    list_filter = ("reserved_by", "started_at", "valid_until")
    search_fields = ("id", "parking", "reserved_by", "started_at", "valid_until")
    ordering = ("reserved_by", "started_at", "valid_until")



admin.site.register(ParkingModel)
admin.site.register(ParkingSpotModel, ParkingSpotAdmin)
admin.site.register(ReservationModel, ReservationAdmin)
admin.site.register(AvailabilityModel, AvailabilityAdmin)
