from django.db import models


class Campaign(models.Model):
    campaign_id = models.CharField(max_length=32, primary_key=True)
    campaign_name = models.CharField(max_length=500)
    publisher = models.CharField(max_length=255)
    publisher_type = models.CharField(max_length=100)
    publication_date = models.DateField()
    case_source_type = models.CharField(max_length=100)
    campaign_specificity = models.CharField(max_length=100)
    attack_classification = models.CharField(max_length=500)
    targeting_evidence = models.TextField()
    outcome = models.CharField(max_length=255)
    target = models.TextField()
    channels = models.TextField()
    channel_transition = models.CharField(max_length=150)
    tactics = models.JSONField(default=list)
    role_attacker = models.TextField()
    role_impersonated = models.TextField()
    role_victim = models.TextField()
    request = models.TextField()
    pretext = models.TextField()
    persuasion_principles = models.JSONField(default=list)
    timing = models.CharField(max_length=150)
    impact = models.TextField()
    information_website = models.URLField(max_length=1000)
    coding_date = models.DateTimeField()
    coder = models.CharField(max_length=100)
    license = models.TextField()
    note_on_ambiguity = models.TextField(blank=True)
    agreement_rate = models.CharField(max_length=20, blank=True)

    class Meta:
        ordering = ['campaign_id']

    def __str__(self):
        return f'{self.campaign_id} - {self.campaign_name}'


class Report(models.Model):
    report_id = models.CharField(max_length=32, primary_key=True)
    report_name = models.CharField(max_length=500)
    report_type = models.CharField(max_length=100)
    period_report = models.CharField(max_length=100)
    report_year = models.PositiveIntegerField()
    geographic_scope = models.CharField(max_length=150)
    publisher = models.CharField(max_length=255)
    publisher_type = models.CharField(max_length=100)
    data_source = models.TextField()
    incident_counts = models.TextField()
    financial_loss = models.TextField()
    information_website = models.URLField(max_length=1000)
    coding_date = models.DateTimeField()
    coder = models.CharField(max_length=100)
    license = models.TextField()
    note_on_ambiguity = models.TextField(blank=True)
    agreement_rate = models.CharField(max_length=20, blank=True)

    class Meta:
        ordering = ['-report_year', 'report_id']

    def __str__(self):
        return f'{self.report_id} - {self.report_name}'
