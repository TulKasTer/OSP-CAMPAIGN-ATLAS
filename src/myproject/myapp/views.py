from django.shortcuts import render
from django.utils.dateparse import parse_date

from .models import Campaign


def campaigns(request):
    query = request.GET.get('q', '').strip()
    publisher = request.GET.get('publisher', '').strip()
    publisher_type = request.GET.get('publisher_type', '').strip()
    outcome = request.GET.get('outcome', '').strip()
    campaign_specificity = request.GET.get('campaign_specificity', '').strip()
    case_source_type = request.GET.get('case_source_type', '').strip()
    attack_classification = request.GET.get('attack_classification', '').strip()
    channel_transition = request.GET.get('channel_transition', '').strip()
    timing = request.GET.get('timing', '').strip()
    coder = request.GET.get('coder', '').strip()
    publication_date_from = request.GET.get('publication_date_from', '').strip()
    publication_date_to = request.GET.get('publication_date_to', '').strip()
    campaigns = Campaign.objects.all()

    if query:
        campaigns = campaigns.filter(
            campaign_id__icontains=query
        ) | Campaign.objects.filter(
            campaign_name__icontains=query
        ) | Campaign.objects.filter(
            publisher__icontains=query
        )

    if publisher:
        campaigns = campaigns.filter(publisher=publisher)
    if publisher_type:
        campaigns = campaigns.filter(publisher_type=publisher_type)
    if outcome:
        campaigns = campaigns.filter(outcome=outcome)
    if campaign_specificity:
        campaigns = campaigns.filter(campaign_specificity=campaign_specificity)
    if case_source_type:
        campaigns = campaigns.filter(case_source_type=case_source_type)
    if attack_classification:
        campaigns = campaigns.filter(
            attack_classification=attack_classification
        )
    if channel_transition:
        campaigns = campaigns.filter(channel_transition=channel_transition)
    if timing:
        campaigns = campaigns.filter(timing=timing)
    if coder:
        campaigns = campaigns.filter(coder=coder)

    date_from = parse_date(publication_date_from)
    date_to = parse_date(publication_date_to)
    if date_from:
        campaigns = campaigns.filter(publication_date__gte=date_from)
    if date_to:
        campaigns = campaigns.filter(publication_date__lte=date_to)

    filter_options = {
        'publishers': Campaign.objects.values_list(
            'publisher', flat=True
        ).distinct().order_by('publisher'),
        'publisher_types': Campaign.objects.values_list(
            'publisher_type', flat=True
        ).distinct().order_by('publisher_type'),
        'outcomes': Campaign.objects.values_list(
            'outcome', flat=True
        ).distinct().order_by('outcome'),
        'campaign_specificities': Campaign.objects.values_list(
            'campaign_specificity', flat=True
        ).distinct().order_by('campaign_specificity'),
        'case_source_types': Campaign.objects.values_list(
            'case_source_type', flat=True
        ).distinct().order_by('case_source_type'),
        'attack_classifications': Campaign.objects.values_list(
            'attack_classification', flat=True
        ).distinct().order_by('attack_classification'),
        'channel_transitions': Campaign.objects.values_list(
            'channel_transition', flat=True
        ).distinct().order_by('channel_transition'),
        'timings': Campaign.objects.values_list(
            'timing', flat=True
        ).distinct().order_by('timing'),
        'coders': Campaign.objects.values_list(
            'coder', flat=True
        ).distinct().order_by('coder'),
    }

    return render(
        request,
        'myapp/campaings.html',
        {
            'campaigns': campaigns,
            'query': query,
            'selected_publisher': publisher,
            'selected_publisher_type': publisher_type,
            'selected_outcome': outcome,
            'selected_campaign_specificity': campaign_specificity,
            'selected_case_source_type': case_source_type,
            'selected_attack_classification': attack_classification,
            'selected_channel_transition': channel_transition,
            'selected_timing': timing,
            'selected_coder': coder,
            'publication_date_from': publication_date_from,
            'publication_date_to': publication_date_to,
            **filter_options,
        },
    )
