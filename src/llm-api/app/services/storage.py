"""Persistence service for saving LLM-coded campaigns, reports, exclusion logs, and source metadata."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Literal

from ..config import (
    EXCLUSION_LOG_FILE,
    INTERIM_HUMAN_CODED_DIR,
    INTERIM_LLM_CAMPAIGNS_DIR,
    INTERIM_LLM_REPORTS_DIR,
    RAW_CAMPAIGNS_DIR,
    RAW_REPORTS_DIR,
)
from ..schemas.campaign import CampaignRecord, ExclusionLogRecord
from ..schemas.common import SourceMetadata
from ..schemas.report import ReportRecord


def slugify_name(value: str, fallback: str = "entry") -> str:
    """Create a filesystem-safe lowercase slug."""
    slug = re.sub(r"[^a-z0-9]+", "-", (value or "").lower()).strip("-")
    return slug[:64] if slug else fallback


class AtlasStorageService:
    """Manages reading/writing JSON files in `data/interim/llm-coded`, `data/raw`, and `logs`."""

    @staticmethod
    def next_campaign_id() -> str:
        """Generate the next sequential CMP-XXXX identifier across interim datasets."""
        max_num = 0
        candidate_files = [
            INTERIM_HUMAN_CODED_DIR / "campaigns" / "campaigns-dataset.json",
            INTERIM_LLM_CAMPAIGNS_DIR / "campaigns-dataset.json",
        ]
        for file_path in candidate_files:
            if file_path.is_file():
                try:
                    data = json.loads(file_path.read_text(encoding="utf-8"))
                    for item in data.get("campaigns", []):
                        cid = str(item.get("campaign_id", ""))
                        match = re.search(r"CMP-(\d+)", cid)
                        if match:
                            max_num = max(max_num, int(match.group(1)))
                except (OSError, ValueError, json.JSONDecodeError):
                    continue
        return f"CMP-{max_num + 1:04d}"

    @staticmethod
    def next_report_id() -> str:
        """Generate the next sequential REP-XXXX identifier across interim datasets."""
        max_num = 0
        candidate_files = [
            INTERIM_HUMAN_CODED_DIR / "reports" / "reports-dataset.json",
            INTERIM_LLM_REPORTS_DIR / "reports-dataset.json",
        ]
        for file_path in candidate_files:
            if file_path.is_file():
                try:
                    data = json.loads(file_path.read_text(encoding="utf-8"))
                    for item in data.get("reports", []):
                        rid = str(item.get("report_id", ""))
                        match = re.search(r"(?:REP|RPT)-(\d+)", rid)
                        if match:
                            max_num = max(max_num, int(match.group(1)))
                except (OSError, ValueError, json.JSONDecodeError):
                    continue
        return f"REP-{max_num + 1:04d}"

    @staticmethod
    def next_excluded_id() -> str:
        """Generate the next sequential EXC-XXXX identifier across exclusion logs."""
        max_num = 0
        candidate_files = [
            INTERIM_HUMAN_CODED_DIR / "campaigns" / "exclusion-log.json",
            INTERIM_LLM_CAMPAIGNS_DIR / "exclusion-log.json",
        ]
        for file_path in candidate_files:
            if file_path.is_file():
                try:
                    data = json.loads(file_path.read_text(encoding="utf-8"))
                    for item in data.get("exclusion_log", []):
                        eid = str(item.get("excluded_id", ""))
                        match = re.search(r"EXC-(\d+)", eid)
                        if match:
                            max_num = max(max_num, int(match.group(1)))
                except (OSError, ValueError, json.JSONDecodeError):
                    continue
        return f"EXC-{max_num + 1:04d}"

    @classmethod
    def save_campaign(
        cls,
        campaign: CampaignRecord,
        folder_slug: str | None = None,
    ) -> list[str]:
        """Save individual campaign JSON and upsert into `data/interim/llm-coded/campaigns/campaigns-dataset.json`."""
        slug = slugify_name(folder_slug or campaign.campaign_id or campaign.campaign_name, "campaign")
        campaign_dir = INTERIM_LLM_CAMPAIGNS_DIR / slug
        campaign_dir.mkdir(parents=True, exist_ok=True)

        individual_file = campaign_dir / f"{slug}.json"
        payload = campaign.model_dump()
        individual_file.write_text(
            json.dumps(payload, indent=4, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

        dataset_file = INTERIM_LLM_CAMPAIGNS_DIR / "campaigns-dataset.json"
        cls._upsert_list_dataset(
            dataset_file=dataset_file,
            root_key="campaigns",
            id_key="campaign_id",
            record=payload,
        )
        return [str(individual_file), str(dataset_file)]

    @classmethod
    def save_report(
        cls,
        report: ReportRecord,
        folder_slug: str | None = None,
    ) -> list[str]:
        """Save individual report JSON and upsert into `data/interim/llm-coded/reports/reports-dataset.json`."""
        slug = slugify_name(folder_slug or report.report_id or report.report_name, "report")
        report_dir = INTERIM_LLM_REPORTS_DIR / slug
        report_dir.mkdir(parents=True, exist_ok=True)

        individual_file = report_dir / f"{slug}.json"
        payload = report.model_dump()
        individual_file.write_text(
            json.dumps(payload, indent=4, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

        dataset_file = INTERIM_LLM_REPORTS_DIR / "reports-dataset.json"
        cls._upsert_list_dataset(
            dataset_file=dataset_file,
            root_key="reports",
            id_key="report_id",
            record=payload,
        )
        return [str(individual_file), str(dataset_file)]

    @classmethod
    def save_exclusion_log(cls, entry: ExclusionLogRecord) -> list[str]:
        """Save exclusion log entry to `data/interim/llm-coded/campaigns/exclusion-log.json` and `logs/exclusion-log.log`."""
        INTERIM_LLM_CAMPAIGNS_DIR.mkdir(parents=True, exist_ok=True)
        exclusion_json_file = INTERIM_LLM_CAMPAIGNS_DIR / "exclusion-log.json"
        payload = entry.model_dump()

        cls._upsert_list_dataset(
            dataset_file=exclusion_json_file,
            root_key="exclusion_log",
            id_key="excluded_id",
            record=payload,
        )

        EXCLUSION_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        log_line = (
            f"[{entry.exclusion_date}] {entry.excluded_id} | {entry.rule_triggered} | "
            f"Publisher: {entry.publisher} | Campaign: {entry.campaign_name} | "
            f"URL: {entry.information_website} | Evaluator: {entry.evaluator} | "
            f"Reason: {entry.exclusion_reason}\n"
        )
        with EXCLUSION_LOG_FILE.open("a", encoding="utf-8") as log_f:
            log_f.write(log_line)

        return [str(exclusion_json_file), str(EXCLUSION_LOG_FILE)]

    @classmethod
    def save_source_metadata(
        cls,
        metadata: SourceMetadata,
        target_type: Literal["campaigns", "reports"] = "campaigns",
        folder_slug: str | None = None,
    ) -> list[str]:
        """Save source metadata JSON and weblink TXT to `data/raw/<target_type>/`."""
        base_dir = RAW_CAMPAIGNS_DIR if target_type == "campaigns" else RAW_REPORTS_DIR
        slug = slugify_name(folder_slug or metadata.title, "source")
        target_dir = base_dir / slug
        target_dir.mkdir(parents=True, exist_ok=True)

        metadata_file = target_dir / f"{slug}-metadata.json"
        weblink_file = target_dir / f"{slug}-weblink.txt"

        payload = metadata.model_dump()
        metadata_file.write_text(
            json.dumps(payload, indent=4, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        weblink_file.write_text(metadata.url + "\n", encoding="utf-8")
        return [str(metadata_file), str(weblink_file)]

    @staticmethod
    def _upsert_list_dataset(
        dataset_file: Path,
        root_key: str,
        id_key: str,
        record: dict,
    ) -> None:
        """Insert or update a record inside a `{root_key: [...]}` JSON file."""
        dataset_file.parent.mkdir(parents=True, exist_ok=True)
        records: list[dict] = []
        if dataset_file.is_file():
            try:
                existing = json.loads(dataset_file.read_text(encoding="utf-8"))
                if isinstance(existing.get(root_key), list):
                    records = existing[root_key]
            except (OSError, ValueError, json.JSONDecodeError):
                records = []

        record_id = record.get(id_key)
        updated = False
        for idx, item in enumerate(records):
            if item.get(id_key) == record_id:
                records[idx] = record
                updated = True
                break
        if not updated:
            records.append(record)

        dataset_file.write_text(
            json.dumps({root_key: records}, indent=4, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
