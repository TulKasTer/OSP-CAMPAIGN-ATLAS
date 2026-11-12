from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from myapp.services.atlas_import import (
    default_campaigns_path,
    default_reports_path,
    import_campaigns,
    import_reports,
)


class Command(BaseCommand):
    help = "Import campaigns and reports from the Atlas JSON datasets."

    def add_arguments(self, parser):
        parser.add_argument("--campaigns-file", type=Path, default=default_campaigns_path())
        parser.add_argument("--reports-file", type=Path, default=default_reports_path())

    def handle(self, *args, **options):
        try:
            campaigns = import_campaigns(options["campaigns_file"])
            reports = import_reports(options["reports_file"])
        except (OSError, ValueError) as error:
            raise CommandError(str(error)) from error

        self.stdout.write(
            self.style.SUCCESS(
                f"Imported {campaigns} campaigns and {reports} reports."
            )
        )
