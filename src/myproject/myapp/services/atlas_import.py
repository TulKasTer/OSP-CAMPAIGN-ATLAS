import json
from datetime import date, datetime
from pathlib import Path
from typing import Any

from django.conf import settings
from django.db import transaction
from django.utils import timezone
from django.utils.dateparse import parse_date, parse_datetime

from myapp.models import Campaign, Report


def default_campaigns_path() -> Path:
    return (
        settings.BASE_DIR.parent.parent
        / "data"
        / "interim"
        / "human-coded"
        / "campaigns"
        / "campaigns-dataset.json"
    )


def default_reports_path() -> Path:
    return (
        settings.BASE_DIR.parent.parent
        / "data"
        / "interim"
        / "human-coded"
        / "reports"
        / "reports-dataset.json"
    )


def import_campaigns(path: Path) -> int:
    records = _load_records(path, "campaigns")
    imported = 0

    with transaction.atomic():
        for record in records:
            campaign_id = _required(record, "campaign_id")
            roles = record.get("roles") or {}
            Campaign.objects.update_or_create(
                campaign_id=campaign_id,
                defaults={
                    "campaign_name": _required(record, "campaign_name"),
                    "publisher": _required(record, "publisher"),
                    "publisher_type": _required(record, "publisher_type"),
                    "publication_date": _required_date(record, "publication_date"),
                    "case_source_type": _required(record, "case_source_type"),
                    "campaign_specificity": _required(record, "campaign_specificity"),
                    "attack_classification": _required(record, "attack_classification"),
                    "targeting_evidence": _required(record, "targeting_evidence"),
                    "outcome": _required(record, "outcome"),
                    "target": _required(record, "target"),
                    "channels": _required(record, "channels"),
                    "channel_transition": _required(record, "channel_transition"),
                    "tactics": record.get("tactics") or [],
                    "role_attacker": _required(roles, "role_attacker"),
                    "role_impersonated": _required(roles, "role_impersonated"),
                    "role_victim": _required(roles, "role_victim"),
                    "request": _required(record, "request"),
                    "pretext": _required(record, "pretext"),
                    "persuasion_principles": record.get("persuasion_principles") or [],
                    "timing": _required(record, "timing"),
                    "impact": _required(record, "impact"),
                    "information_website": _required(record, "information_website"),
                    "coding_date": _required_datetime(record, "coding_date"),
                    "coder": _required(record, "coder"),
                    "license": _required(record, "license"),
                    "note_on_ambiguity": record.get("note_on_ambiguity") or "",
                    "agreement_rate": record.get("agreement_rate") or "",
                },
            )
            imported += 1

    return imported


def import_reports(path: Path) -> int:
    records = _load_records(path, "reports")
    imported = 0

    with transaction.atomic():
        for record in records:
            report_id = _required(record, "report_id")
            Report.objects.update_or_create(
                report_id=report_id,
                defaults={
                    "report_name": _required(record, "report_name"),
                    "report_type": _required(record, "report_type"),
                    "period_report": _required(record, "period_report"),
                    "report_year": _required_integer(record, "report_year"),
                    "geographic_scope": _required(record, "geographic_scope"),
                    "publisher": _required(record, "publisher"),
                    "publisher_type": _required(record, "publisher_type"),
                    "data_source": _required(record, "data_source"),
                    "incident_counts": _required(record, "incident_counts"),
                    "financial_loss": _required(record, "financial_loss"),
                    "information_website": _required(record, "information_website"),
                    "coding_date": _required_datetime(record, "coding_date"),
                    "coder": _required(record, "coder"),
                    "license": _required(record, "license"),
                    "note_on_ambiguity": record.get("note_on_ambiguity") or "",
                    "agreement_rate": record.get("agreement_rate") or "",
                },
            )
            imported += 1

    return imported


def _load_records(path: Path, key: str) -> list[dict[str, Any]]:
    if not path.is_file():
        raise FileNotFoundError(f"JSON file not found: {path}")

    with path.open(encoding="utf-8") as file:
        payload = json.load(file)

    records = payload.get(key)
    if not isinstance(records, list):
        raise ValueError(f"{path} must contain a '{key}' list")
    if not all(isinstance(record, dict) for record in records):
        raise ValueError(f"All items in '{key}' must be JSON objects")
    return records


def _required(record: dict[str, Any], field: str) -> str:
    value = record.get(field)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Missing required field '{field}'")
    return value.strip()


def _required_date(record: dict[str, Any], field: str) -> date:
    value = parse_date(_required(record, field))
    if value is None:
        raise ValueError(f"Invalid date in '{field}'")
    return value


def _required_datetime(record: dict[str, Any], field: str) -> datetime:
    value = parse_datetime(_required(record, field))
    if value is None:
        raise ValueError(f"Invalid datetime in '{field}'")
    if timezone.is_naive(value):
        return timezone.make_aware(value, timezone.get_current_timezone())
    return value


def _required_integer(record: dict[str, Any], field: str) -> int:
    value = _required(record, field)
    try:
        return int(value)
    except ValueError as error:
        raise ValueError(f"Invalid integer in '{field}': {value}") from error
