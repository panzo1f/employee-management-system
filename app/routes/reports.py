from flask import Blueprint, Response, render_template

from app.services.report_pdf_service import ReportPDFService
from app.services.report_service import ReportService


reports_bp = Blueprint(
    "reports",
    __name__,
    url_prefix="/reports",
)


@reports_bp.route("/")
def index():
    report_data = ReportService.get_dashboard_data()

    return render_template(
        "reports/index.html",
        report_data=report_data,
    )


@reports_bp.route("/export")
def export():
    report_data = ReportService.get_dashboard_data()

    summary = report_data["summary"]
    status = report_data["employee_status"]
    departments = report_data["employees_by_department"]
    positions = report_data["employees_by_position"]
    activity = report_data["system_activity"]

    lines = [
        "NovaHR - Reports",
        "",
        "Summary",
        "Metric,Value",
        f"Total Employees,{summary['total_employees']}",
        f"Active Employees,{summary['active_employees']}",
        f"Departments,{summary['total_departments']}",
        f"Users,{summary['total_users']}",
        "",
        "Employee Status",
        "Status,Count",
        f"Active,{status['active']}",
        f"Inactive,{status['inactive']}",
        "",
        "Employees by Department",
        "Department,Employees",
    ]

    for department in departments:
        name = str(
            department["name"]
        ).replace('"', '""')

        lines.append(
            f'"{name}",{department["count"]}'
        )

    lines.extend([
        "",
        "Employees by Position",
        "Position,Employees",
    ])

    for position in positions:
        name = str(
            position["position"]
        ).replace('"', '""')

        lines.append(
            f'"{name}",{position["count"]}'
        )

    lines.extend([
        "",
        "System Activity",
        "Action,Count",
        f"Created,{activity['created']}",
        f"Updated,{activity['updated']}",
        f"Deleted,{activity['deleted']}",
    ])

    csv_content = "\n".join(lines)

    return Response(
        csv_content,
        mimetype="text/csv",
        headers={
            "Content-Disposition": (
                "attachment; "
                "filename=novahr-report.csv"
            )
        },
    )


@reports_bp.route("/export/pdf")
def export_pdf():
    pdf = ReportPDFService.generate()

    return Response(
        pdf.getvalue(),
        mimetype="application/pdf",
        headers={
            "Content-Disposition": (
                "attachment; "
                "filename=novahr-report.pdf"
            )
        },
    )
