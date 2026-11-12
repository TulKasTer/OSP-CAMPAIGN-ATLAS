from django.contrib import admin
from .models import Campaign, Report


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('campaign_id', 'campaign_name', 'publisher', 'publication_date')
    search_fields = ('campaign_id', 'campaign_name', 'publisher', 'target')
    list_filter = ('publisher_type', 'outcome', 'coder')


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('report_id', 'report_name', 'publisher', 'report_year')
    search_fields = ('report_id', 'report_name', 'publisher')
    list_filter = ('publisher_type', 'report_type', 'report_year', 'coder')
