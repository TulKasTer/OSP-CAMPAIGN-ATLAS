"""Inter-rater reliability (Agreement Rate & Cohen's kappa) and schema validation service."""

from __future__ import annotations

import re
from typing import Any
from pydantic import ValidationError

from ..schemas.api import (
    DatasetAgreementRequest,
    DatasetAgreementResponse,
    FieldComparisonResult,
    LabelKappaMetric,
    RowAgreementRequest,
    RowAgreementResponse,
    ValidateRecordRequest,
    ValidateRecordResponse,
)
from ..schemas.campaign import CampaignRecord, ExclusionLogRecord
from ..schemas.common import (
    NOT_SPECIFIED_REPORT,
    PERSUASION_PRINCIPLES_TAXONOMY,
    PUBLISHER_TO_TYPE_MAP,
    TACTICS_TAXONOMY,
)
from ..schemas.report import ReportRecord

# Analytical variables compared for row-level Agreement Rate (excluding administrative metadata like IDs, dates, coder, agreement_rate)
CAMPAIGN_CLOSED_VARIABLES = (
    "publisher",
    "publisher_type",
    "case_source_type",
    "campaign_specificity",
    "attack_classification",
    "outcome",
    "channel_transition",
    "tactics",
    "persuasion_principles",
    "timing",
    "license",
)

CAMPAIGN_ALL_ANALYTICAL_VARIABLES = (
    "campaign_name",
    "publisher",
    "publisher_type",
    "publication_date",
    "case_source_type",
    "campaign_specificity",
    "attack_classification",
    "targeting_evidence",
    "outcome",
    "target",
    "channels",
    "channel_transition",
    "tactics",
    "role_attacker",
    "role_impersonated",
    "role_victim",
    "request",
    "pretext",
    "persuasion_principles",
    "timing",
    "impact",
    "license",
)

REPORT_CLOSED_VARIABLES = (
    "report_type",
    "period_report",
    "report_year",
    "geographic_scope",
    "publisher",
    "publisher_type",
    "data_source",
    "license",
)

REPORT_ALL_ANALYTICAL_VARIABLES = (
    "report_name",
    "report_type",
    "period_report",
    "report_year",
    "geographic_scope",
    "publisher",
    "publisher_type",
    "data_source",
    "incident_counts",
    "financial_loss",
    "license",
)


def _normalize_scalar(value: Any) -> str:
    """Normalize string values for deterministic comparison."""
    text = str(value if value is not None else "").strip().lower()
    text = re.sub(r"\s+", " ", text).rstrip(".")
    return text


def _normalize_attack_classification_base(value: str) -> str:
    """Normalize attack_classification to its base category (grouping Hybrid Campaign variants)."""
    norm = _normalize_scalar(value)
    if norm.startswith("hybrid campaign"):
        return "hybrid campaign - targeting and impersonation necessary"
    if norm.startswith("pure bec"):
        return "pure bec (impersonation + fraud)"
    if norm.startswith("pure spear phishing"):
        return "pure spear phishing (targeted lure + impersonation)"
    if "impersonation unnecessary" in norm:
        return "impersonation unnecessary (out of scope)"
    if "no target selection" in norm:
        return "no target selection (out of scope)"
    return norm


def _extract_hybrid_vector(value: str) -> str | None:
    """Extract the parenthesized vector from a Hybrid Campaign classification string."""
    norm = _normalize_scalar(value)
    if not norm.startswith("hybrid campaign"):
        return None
    matches = re.findall(r"\(([^)]+)\)", norm)
    if not matches:
        return ""
    return matches[-1].strip()


def _extract_field(record: dict[str, Any], variable: str) -> Any:
    """Extract a variable from a record, supporting nested `roles` in campaign records."""
    if variable in ("role_attacker", "role_impersonated", "role_victim"):
        roles = record.get("roles")
        if isinstance(roles, dict) and variable in roles:
            return roles.get(variable)
    return record.get(variable)


def _compare_values(variable: str, val_a: Any, val_b: Any) -> tuple[bool, float]:
    """Compare two variable values and return (exact_match, similarity_score)."""
    if isinstance(val_a, list) or isinstance(val_b, list):
        list_a = {_normalize_scalar(x) for x in (val_a if isinstance(val_a, list) else [val_a]) if str(x).strip()}
        list_b = {_normalize_scalar(x) for x in (val_b if isinstance(val_b, list) else [val_b]) if str(x).strip()}
        if list_a == list_b:
            return True, 1.0
        union = list_a | list_b
        intersection = list_a & list_b
        jaccard = len(intersection) / len(union) if union else 1.0
        return False, round(jaccard, 4)

    if variable == "attack_classification":
        base_a = _normalize_attack_classification_base(str(val_a or ""))
        base_b = _normalize_attack_classification_base(str(val_b or ""))
        matched = base_a == base_b
        return matched, 1.0 if matched else 0.0

    norm_a = _normalize_scalar(val_a)
    norm_b = _normalize_scalar(val_b)
    matched = norm_a == norm_b
    return matched, 1.0 if matched else 0.0


def compute_row_agreement(request: RowAgreementRequest) -> RowAgreementResponse:
    """Compute row-level percentage agreement between two independent codings per DATASET SCHEMA V2.1."""
    if request.record_type == "campaign":
        variables = (
            CAMPAIGN_CLOSED_VARIABLES
            if request.compare_only_closed_variables
            else CAMPAIGN_ALL_ANALYTICAL_VARIABLES
        )
    else:
        variables = (
            REPORT_CLOSED_VARIABLES
            if request.compare_only_closed_variables
            else REPORT_ALL_ANALYTICAL_VARIABLES
        )

    comparisons: list[FieldComparisonResult] = []
    matched_count = 0

    for var in variables:
        val_a = _extract_field(request.coder_a, var)
        val_b = _extract_field(request.coder_b, var)
        matched, score = _compare_values(var, val_a, val_b)
        if matched:
            matched_count += 1
        comparisons.append(
            FieldComparisonResult(
                variable=var,
                coder_a_value=val_a,
                coder_b_value=val_b,
                matched=matched,
                similarity_score=score,
            )
        )

    total = len(variables)
    pct = round((matched_count / total) * 100.0, 2) if total > 0 else 0.0
    rounded_int = round(pct)

    return RowAgreementResponse(
        record_type=request.record_type,
        agreement_rate=f"{rounded_int}%",
        agreement_percentage=pct,
        matched_variables=matched_count,
        total_variables_compared=total,
        meets_protocol_threshold=pct >= 80.0,
        comparisons=comparisons,
    )


def _cohens_kappa_multiclass(labels_a: list[str], labels_b: list[str]) -> tuple[float, float]:
    """Compute observed proportion of agreement (p_o) and Cohen's kappa (κ) for nominal categories."""
    n = len(labels_a)
    if n == 0 or len(labels_b) != n:
        return 0.0, 0.0

    agreements = sum(1 for a, b in zip(labels_a, labels_b) if a == b)
    p_o = agreements / n

    categories = set(labels_a) | set(labels_b)
    p_e = 0.0
    for cat in categories:
        prob_a = sum(1 for a in labels_a if a == cat) / n
        prob_b = sum(1 for b in labels_b if b == cat) / n
        p_e += prob_a * prob_b

    if abs(1.0 - p_e) < 1e-12:
        return round(p_o * 100.0, 2), 1.0 if p_o == 1.0 else 0.0

    kappa = (p_o - p_e) / (1.0 - p_e)
    return round(p_o * 100.0, 2), round(kappa, 4)


def _compute_binary_label_kappa(
    target_label: str,
    lists_a: list[list[str]],
    lists_b: list[list[str]],
    min_frequency: int,
) -> LabelKappaMetric:
    """Compute binary present/absent Cohen's kappa for a single taxonomy label across the sample."""
    norm_target = _normalize_scalar(target_label)

    def has_label(items: list[str]) -> str:
        for item in items:
            norm_item = _normalize_scalar(item)
            if norm_target == "other (specify)" and norm_item.startswith("other (specify)"):
                return "present"
            if norm_item == norm_target:
                return "present"
        return "absent"

    binary_a = [has_label(lst) for lst in lists_a]
    binary_b = [has_label(lst) for lst in lists_b]

    occ_a = sum(1 for x in binary_a if x == "present")
    occ_b = sum(1 for x in binary_b if x == "present")
    total_occ = max(occ_a, occ_b)

    pct_agreement, kappa = _cohens_kappa_multiclass(binary_a, binary_b)

    # Registered Protocol V1 page 10:
    # "Labels that appear fewer than [5] times in the samples are reported with % agreement only."
    if total_occ < min_frequency:
        return LabelKappaMetric(
            name=target_label,
            occurrences_coder_a=occ_a,
            occurrences_coder_b=occ_b,
            percent_agreement=pct_agreement,
            cohens_kappa=None,
            meets_criterion=pct_agreement >= 80.0,
            note=f"Label frequency ({total_occ}) < {min_frequency}; reported with % agreement only per Registered Protocol V1.",
        )

    return LabelKappaMetric(
        name=target_label,
        occurrences_coder_a=occ_a,
        occurrences_coder_b=occ_b,
        percent_agreement=pct_agreement,
        cohens_kappa=kappa,
        meets_criterion=kappa >= 0.60,
    )


def compute_dataset_agreement(request: DatasetAgreementRequest) -> DatasetAgreementResponse:
    """Compute full inter-rater reliability metrics (Cohen's κ & % agreement) per Registered Protocol V1."""
    # Pair records by campaign_id if available, otherwise pair positionally
    b_by_id = {
        str(r.get("campaign_id")).strip(): r
        for r in request.coder_b_campaigns
        if r.get("campaign_id")
    }
    pairs: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for idx, rec_a in enumerate(request.coder_a_campaigns):
        cid = str(rec_a.get("campaign_id", "")).strip()
        if cid and cid in b_by_id:
            pairs.append((rec_a, b_by_id[cid]))
        elif idx < len(request.coder_b_campaigns):
            pairs.append((rec_a, request.coder_b_campaigns[idx]))

    if not pairs:
        raise ValueError("No matching campaign pairs found between coder_a_campaigns and coder_b_campaigns.")

    row_results = [
        compute_row_agreement(
            RowAgreementRequest(record_type="campaign", coder_a=a, coder_b=b)
        )
        for a, b in pairs
    ]
    mean_row_pct = round(
        sum(r.agreement_percentage for r in row_results) / len(row_results), 2
    )

    # 1. attack_classification (Cohen's kappa and % agreement, κ >= 0.60)
    ac_a = [_normalize_attack_classification_base(str(a.get("attack_classification", ""))) for a, _ in pairs]
    ac_b = [_normalize_attack_classification_base(str(b.get("attack_classification", ""))) for _, b in pairs]
    ac_pct, ac_kappa = _cohens_kappa_multiclass(ac_a, ac_b)
    attack_classification_metric = LabelKappaMetric(
        name="attack_classification",
        occurrences_coder_a=len(ac_a),
        occurrences_coder_b=len(ac_b),
        percent_agreement=ac_pct,
        cohens_kappa=ac_kappa,
        meets_criterion=ac_kappa >= 0.60,
    )

    # 2. Hybrid other vector (% agreement after normalizing vector names, >= 80%)
    hybrid_pairs: list[tuple[str, str]] = []
    for a, b in pairs:
        vec_a = _extract_hybrid_vector(str(a.get("attack_classification", "")))
        vec_b = _extract_hybrid_vector(str(b.get("attack_classification", "")))
        if vec_a is not None and vec_b is not None:
            hybrid_pairs.append((vec_a, vec_b))

    hybrid_agreement_pct: float | None = None
    if hybrid_pairs:
        matches = sum(1 for va, vb in hybrid_pairs if _normalize_scalar(va) == _normalize_scalar(vb))
        hybrid_agreement_pct = round((matches / len(hybrid_pairs)) * 100.0, 2)

    # 3. targeting_evidence (Cohen's kappa on presence/absence of explicit evidence, plus % agreement)
    def has_targeting_evidence(record: dict[str, Any]) -> str:
        val = _normalize_scalar(record.get("targeting_evidence", ""))
        if not val or val == _normalize_scalar(NOT_SPECIFIED_REPORT):
            return "absent"
        return "present"

    te_a = [has_targeting_evidence(a) for a, _ in pairs]
    te_b = [has_targeting_evidence(b) for _, b in pairs]
    te_pct, te_kappa = _cohens_kappa_multiclass(te_a, te_b)
    targeting_evidence_metric = LabelKappaMetric(
        name="targeting_evidence (presence/absence)",
        occurrences_coder_a=sum(1 for x in te_a if x == "present"),
        occurrences_coder_b=sum(1 for x in te_b if x == "present"),
        percent_agreement=te_pct,
        cohens_kappa=te_kappa,
        meets_criterion=te_kappa >= 0.60,
    )

    # 4. persuasion_principles per label (Cohen's kappa per label, κ >= 0.60)
    pp_lists_a = [a.get("persuasion_principles") or [] for a, _ in pairs]
    pp_lists_b = [b.get("persuasion_principles") or [] for _, b in pairs]
    pp_metrics = [
        _compute_binary_label_kappa(label, pp_lists_a, pp_lists_b, request.min_label_frequency)
        for label in PERSUASION_PRINCIPLES_TAXONOMY
    ]

    # 5. tactics per label (Cohen's kappa per label, κ >= 0.60)
    tac_lists_a = [a.get("tactics") or [] for a, _ in pairs]
    tac_lists_b = [b.get("tactics") or [] for _, b in pairs]
    tactics_metrics = [
        _compute_binary_label_kappa(label, tac_lists_a, tac_lists_b, request.min_label_frequency)
        for label in TACTICS_TAXONOMY
    ]

    return DatasetAgreementResponse(
        sample_size=len(pairs),
        mean_row_agreement_percentage=mean_row_pct,
        attack_classification=attack_classification_metric,
        targeting_evidence_presence=targeting_evidence_metric,
        hybrid_other_vector_agreement_percentage=hybrid_agreement_pct,
        persuasion_principles_per_label=pp_metrics,
        tactics_per_label=tactics_metrics,
        row_results=row_results,
    )


def validate_atlas_record(request: ValidateRecordRequest) -> ValidateRecordResponse:
    """Validate a Campaign, Report, or Exclusion Log payload against FREEZE CODING SCHEME V2.1 rules."""
    errors: list[str] = []
    warnings: list[str] = []
    payload = request.payload

    try:
        if request.record_type == "campaign":
            # Check Publisher -> Publisher Type consistency before normalization
            pub = str(payload.get("publisher", "")).strip()
            pub_type = str(payload.get("publisher_type", "")).strip()
            expected_type = PUBLISHER_TO_TYPE_MAP.get(pub.lower().rstrip("."))
            if expected_type and pub_type and pub_type.lower() != expected_type.lower():
                warnings.append(
                    f"publisher_type '{pub_type}' did not match Publisher '{pub}' rule ('{expected_type}'); auto-corrected."
                )

            # Check Decision Rule #11 (agreement_rate must be N/A unless Dual coded)
            coder = str(payload.get("coder", "")).strip()
            agr = str(payload.get("agreement_rate", "")).strip()
            if coder.lower() != "dual coded" and agr and agr != "N/A":
                warnings.append(
                    f"Decision Rule #11: agreement_rate was '{agr}' while coder is '{coder}'; reset to 'N/A'."
                )

            # Check MITRE T1598.003 rule on tactics
            tactics = [str(t) for t in (payload.get("tactics") or [])]
            has_fake_login = any("fake login" in t.lower() for t in tactics)
            has_aitm = any("aitm" in t.lower() or "adversary-in-the-middle" in t.lower() for t in tactics)
            if has_fake_login and not has_aitm:
                warnings.append(
                    "Note (MITRE T1598.003): 'Fake login / credential-collection page' is present without 'Adversary-in-the-middle (AiTM)'. Verify whether MFA bypass or session-cookie capture occurred."
                )

            record = CampaignRecord.model_validate(payload)
            return ValidateRecordResponse(
                valid=True,
                record_type="campaign",
                errors=errors,
                warnings=warnings,
                normalized_payload=record.model_dump(),
            )

        if request.record_type == "report":
            record = ReportRecord.model_validate(payload)
            return ValidateRecordResponse(
                valid=True,
                record_type="report",
                errors=errors,
                warnings=warnings,
                normalized_payload=record.model_dump(),
            )

        record = ExclusionLogRecord.model_validate(payload)
        return ValidateRecordResponse(
            valid=True,
            record_type="exclusion_log",
            errors=errors,
            warnings=warnings,
            normalized_payload=record.model_dump(),
        )

    except ValidationError as exc:
        for err in exc.errors():
            loc = ".".join(str(part) for part in err.get("loc", []))
            errors.append(f"{loc}: {err.get('msg')}")
        return ValidateRecordResponse(
            valid=False,
            record_type=request.record_type,
            errors=errors,
            warnings=warnings,
            normalized_payload=None,
        )
