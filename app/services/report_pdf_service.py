from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from app.services.report_service import ReportService


class ReportPDFService:

    @staticmethod
    def generate():
        report_data = ReportService.get_dashboard_data()

        buffer = BytesIO()

        document = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=15 * mm,
            leftMargin=15 * mm,
            topMargin=15 * mm,
            bottomMargin=15 * mm,
            title="NovaHR Reports",
            author="NovaHR",
        )

        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            "ReportTitle",
            parent=styles["Title"],
            fontSize=22,
            leading=26,
            alignment=TA_LEFT,
            spaceAfter=4,
        )

        subtitle_style = ParagraphStyle(
            "ReportSubtitle",
            parent=styles["Normal"],
            fontSize=9,
            textColor=colors.HexColor("#6c757d"),
            spaceAfter=14,
        )

        section_style = ParagraphStyle(
            "SectionTitle",
            parent=styles["Heading2"],
            fontSize=12,
            leading=15,
            spaceAfter=8,
        )

        normal_style = ParagraphStyle(
            "ReportNormal",
            parent=styles["Normal"],
            fontSize=8,
            leading=11,
        )

        story = []

        # --------------------------------------------------
        # HEADER
        # --------------------------------------------------

        story.append(
            Paragraph(
                "NovaHR",
                title_style,
            )
        )

        story.append(
            Paragraph(
                "Reports — Employee Management System",
                subtitle_style,
            )
        )

        # --------------------------------------------------
        # KPI CARDS
        # --------------------------------------------------

        summary = report_data["summary"]

        kpi_data = [
            [
                Paragraph(
                    "<b>Total Employees</b><br/>"
                    f"<font size='18'>{summary['total_employees']}</font>",
                    normal_style,
                ),
                Paragraph(
                    "<b>Active</b><br/>"
                    f"<font size='18'>{summary['active_employees']}</font>",
                    normal_style,
                ),
                Paragraph(
                    "<b>Departments</b><br/>"
                    f"<font size='18'>{summary['total_departments']}</font>",
                    normal_style,
                ),
                Paragraph(
                    "<b>Users</b><br/>"
                    f"<font size='18'>{summary['total_users']}</font>",
                    normal_style,
                ),
            ]
        ]

        kpi_table = Table(
            kpi_data,
            colWidths=[
                43 * mm,
                43 * mm,
                43 * mm,
                43 * mm,
            ],
        )

        kpi_table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, -1),
                        colors.HexColor("#f8f9fa"),
                    ),
                    (
                        "BOX",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.HexColor("#dee2e6"),
                    ),
                    (
                        "INNERGRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.HexColor("#dee2e6"),
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "MIDDLE",
                    ),
                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        10,
                    ),
                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        10,
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        10,
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        10,
                    ),
                ]
            )
        )

        story.append(kpi_table)
        story.append(Spacer(1, 12))

        # --------------------------------------------------
        # EMPLOYEE STATUS
        # --------------------------------------------------

        story.append(
            Paragraph(
                "Employee Status",
                section_style,
            )
        )

        status = report_data["employee_status"]

        active = status["active"]
        inactive = status["inactive"]
        total = active + inactive

        active_percentage = (
            active / total * 100
            if total
            else 0
        )

        inactive_percentage = (
            inactive / total * 100
            if total
            else 0
        )

        status_data = [
            ["Status", "Employees", "Percentage"],
            [
                "Active",
                str(active),
                f"{active_percentage:.1f}%",
            ],
            [
                "Inactive",
                str(inactive),
                f"{inactive_percentage:.1f}%",
            ],
        ]

        status_table = Table(
            status_data,
            colWidths=[
                70 * mm,
                45 * mm,
                45 * mm,
            ],
        )

        status_table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.HexColor("#212529"),
                    ),
                    (
                        "TEXTCOLOR",
                        (0, 0),
                        (-1, 0),
                        colors.white,
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.HexColor("#dee2e6"),
                    ),
                    (
                        "ALIGN",
                        (1, 1),
                        (-1, -1),
                        "CENTER",
                    ),
                    (
                        "BACKGROUND",
                        (0, 1),
                        (-1, 1),
                        colors.HexColor("#f8f9fa"),
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        7,
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        7,
                    ),
                ]
            )
        )

        story.append(status_table)
        story.append(Spacer(1, 12))

        # --------------------------------------------------
        # EMPLOYEES BY DEPARTMENT
        # --------------------------------------------------

        story.append(
            Paragraph(
                "Employees by Department",
                section_style,
            )
        )

        department_rows = [
            ["Department", "Employees"]
        ]

        for department in report_data[
            "employees_by_department"
        ]:
            department_rows.append(
                [
                    str(department["name"]),
                    str(department["count"]),
                ]
            )

        if len(department_rows) == 1:
            department_rows.append(
                ["No data available", "0"]
            )

        department_table = Table(
            department_rows,
            colWidths=[
                120 * mm,
                40 * mm,
            ],
        )

        department_table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.HexColor("#212529"),
                    ),
                    (
                        "TEXTCOLOR",
                        (0, 0),
                        (-1, 0),
                        colors.white,
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.HexColor("#dee2e6"),
                    ),
                    (
                        "ALIGN",
                        (1, 1),
                        (1, -1),
                        "CENTER",
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        6,
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        6,
                    ),
                ]
            )
        )

        story.append(department_table)
        story.append(Spacer(1, 12))

        # --------------------------------------------------
        # EMPLOYEES BY POSITION
        # --------------------------------------------------

        story.append(
            Paragraph(
                "Employees by Position",
                section_style,
            )
        )

        position_rows = [
            ["Position", "Employees"]
        ]

        for position in report_data[
            "employees_by_position"
        ]:
            position_rows.append(
                [
                    str(position["position"]),
                    str(position["count"]),
                ]
            )

        if len(position_rows) == 1:
            position_rows.append(
                ["No data available", "0"]
            )

        position_table = Table(
            position_rows,
            colWidths=[
                120 * mm,
                40 * mm,
            ],
        )

        position_table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.HexColor("#212529"),
                    ),
                    (
                        "TEXTCOLOR",
                        (0, 0),
                        (-1, 0),
                        colors.white,
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.HexColor("#dee2e6"),
                    ),
                    (
                        "ALIGN",
                        (1, 1),
                        (1, -1),
                        "CENTER",
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        6,
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        6,
                    ),
                ]
            )
        )

        story.append(position_table)
        story.append(Spacer(1, 12))

        # --------------------------------------------------
        # SYSTEM ACTIVITY
        # --------------------------------------------------

        story.append(
            Paragraph(
                "System Activity",
                section_style,
            )
        )

        activity = report_data["system_activity"]

        activity_rows = [
            ["Action", "Count"],
            ["Created", str(activity["created"])],
            ["Updated", str(activity["updated"])],
            ["Deleted", str(activity["deleted"])],
        ]

        activity_table = Table(
            activity_rows,
            colWidths=[
                120 * mm,
                40 * mm,
            ],
        )

        activity_table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.HexColor("#212529"),
                    ),
                    (
                        "TEXTCOLOR",
                        (0, 0),
                        (-1, 0),
                        colors.white,
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.HexColor("#dee2e6"),
                    ),
                    (
                        "ALIGN",
                        (1, 1),
                        (1, -1),
                        "CENTER",
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        6,
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        6,
                    ),
                ]
            )
        )

        story.append(activity_table)

        document.build(story)

        buffer.seek(0)

        return buffer
