from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Flowable,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from app.services.report_service import ReportService


class ChartFlowable(Flowable):

    def __init__(
        self,
        width,
        height,
        chart_type,
        data,
    ):
        Flowable.__init__(self)

        self.width = width
        self.height = height
        self.chart_type = chart_type
        self.data = data

    def wrap(self, available_width, available_height):
        return self.width, self.height

    def draw(self):
        if self.chart_type == "donut":
            self._draw_donut()

        elif self.chart_type == "department":
            self._draw_bars(
                label_key="name"
            )

        elif self.chart_type == "position":
            self._draw_bars(
                label_key="position"
            )

        elif self.chart_type == "hiring":
            self._draw_hiring()

    def _draw_donut(self):

        canvas = self.canv

        active = self.data.get(
            "active",
            0,
        )

        inactive = self.data.get(
            "inactive",
            0,
        )

        total = active + inactive

        center_x = self.width / 2
        center_y = self.height / 2

        radius = 27 * mm

        if total == 0:

            canvas.setFillColor(
                colors.HexColor("#dee2e6")
            )

            canvas.circle(
                center_x,
                center_y,
                radius,
                stroke=0,
                fill=1,
            )

        else:

            active_angle = (
                active / total
            ) * 360

            canvas.setFillColor(
                colors.HexColor("#198754")
            )

            canvas.wedge(
                center_x - radius,
                center_y - radius,
                center_x + radius,
                center_y + radius,
                0,
                active_angle,
                stroke=0,
                fill=1,
            )

            canvas.setFillColor(
                colors.HexColor("#6c757d")
            )

            canvas.wedge(
                center_x - radius,
                center_y - radius,
                center_x + radius,
                center_y + radius,
                active_angle,
                360 - active_angle,
                stroke=0,
                fill=1,
            )

            # Centro branco
            canvas.setFillColor(
                colors.white
            )

            canvas.circle(
                center_x,
                center_y,
                radius * 0.58,
                stroke=0,
                fill=1,
            )

            # Número total
            canvas.setFillColor(
                colors.HexColor("#212529")
            )

            canvas.setFont(
                "Helvetica-Bold",
                16,
            )

            canvas.drawCentredString(
                center_x,
                center_y - 5,
                str(total),
            )

        # Legenda

        legend_y = 10 * mm

        canvas.setFont(
            "Helvetica",
            8,
        )

        # Active

        canvas.setFillColor(
            colors.HexColor("#198754")
        )

        canvas.circle(
            center_x - 35 * mm,
            legend_y,
            2.2,
            stroke=0,
            fill=1,
        )

        canvas.setFillColor(
            colors.HexColor("#212529")
        )

        canvas.drawString(
            center_x - 31 * mm,
            legend_y - 3,
            f"Active ({active})",
        )

        # Inactive

        canvas.setFillColor(
            colors.HexColor("#6c757d")
        )

        canvas.circle(
            center_x + 20 * mm,
            legend_y,
            2.2,
            stroke=0,
            fill=1,
        )

        canvas.setFillColor(
            colors.HexColor("#212529")
        )

        canvas.drawString(
            center_x + 24 * mm,
            legend_y - 3,
            f"Inactive ({inactive})",
        )

    def _draw_bars(self, label_key):

        canvas = self.canv

        items = self.data or []

        if not items:

            canvas.setFillColor(
                colors.HexColor("#6c757d")
            )

            canvas.setFont(
                "Helvetica",
                9,
            )

            canvas.drawString(
                10 * mm,
                self.height / 2,
                "No data available.",
            )

            return

        max_value = max(
            float(item["count"])
            for item in items
        )

        if max_value <= 0:
            max_value = 1

        left = 50 * mm
        right = 15 * mm

        top = self.height - 8 * mm

        available_width = (
            self.width
            - left
            - right
        )

        row_height = min(
            12 * mm,
            (
                self.height - 12 * mm
            ) / max(len(items), 1),
        )

        canvas.setFont(
            "Helvetica",
            7.5,
        )

        for index, item in enumerate(items):

            y = (
                top
                - (
                    index + 1
                ) * row_height
            )

            label = str(
                item[label_key]
            )

            value = float(
                item["count"]
            )

            # Label

            canvas.setFillColor(
                colors.HexColor("#212529")
            )

            canvas.drawRightString(
                left - 5 * mm,
                y + 3,
                label[:28],
            )

            # Background

            canvas.setFillColor(
                colors.HexColor("#e9ecef")
            )

            canvas.roundRect(
                left,
                y,
                available_width,
                7,
                2,
                stroke=0,
                fill=1,
            )

            # Bar

            bar_width = (
                available_width
                * value
                / max_value
            )

            canvas.setFillColor(
                colors.HexColor("#0d6efd")
            )

            canvas.roundRect(
                left,
                y,
                bar_width,
                7,
                2,
                stroke=0,
                fill=1,
            )

            # Value

            canvas.setFillColor(
                colors.HexColor("#212529")
            )

            canvas.setFont(
                "Helvetica-Bold",
                7,
            )

            canvas.drawString(
                left
                + available_width
                + 3 * mm,
                y + 1,
                str(int(value)),
            )

    def _draw_hiring(self):

        canvas = self.canv

        items = self.data or []

        if not items:

            canvas.setFillColor(
                colors.HexColor("#6c757d")
            )

            canvas.setFont(
                "Helvetica",
                9,
            )

            canvas.drawString(
                10 * mm,
                self.height / 2,
                "No hiring data available.",
            )

            return

        left = 15 * mm
        bottom = 15 * mm

        chart_width = (
            self.width
            - 25 * mm
        )

        chart_height = (
            self.height
            - 30 * mm
        )

        values = [
            float(item["count"])
            for item in items
        ]

        max_value = max(values)

        if max_value <= 0:
            max_value = 1

        # Eixos

        canvas.setStrokeColor(
            colors.HexColor("#dee2e6")
        )

        canvas.setLineWidth(0.6)

        canvas.line(
            left,
            bottom,
            left,
            bottom + chart_height,
        )

        canvas.line(
            left,
            bottom,
            left + chart_width,
            bottom,
        )

        points = []

        for index, item in enumerate(items):

            if len(items) == 1:

                x = (
                    left
                    + chart_width / 2
                )

            else:

                x = (
                    left
                    + (
                        index
                        / (len(items) - 1)
                    )
                    * chart_width
                )

            y = (
                bottom
                + (
                    float(item["count"])
                    / max_value
                )
                * chart_height
            )

            points.append(
                (x, y)
            )

        # Linha

        if len(points) > 1:

            canvas.setStrokeColor(
                colors.HexColor("#0d6efd")
            )

            canvas.setLineWidth(2)

            path = canvas.beginPath()

            path.moveTo(
                points[0][0],
                points[0][1],
            )

            for x, y in points[1:]:

                path.lineTo(
                    x,
                    y,
                )

            canvas.drawPath(path)

        # Pontos

        for index, point in enumerate(points):

            x, y = point

            canvas.setFillColor(
                colors.HexColor("#0d6efd")
            )

            canvas.circle(
                x,
                y,
                2.5,
                stroke=0,
                fill=1,
            )

            canvas.setFillColor(
                colors.HexColor("#212529")
            )

            canvas.setFont(
                "Helvetica",
                6.5,
            )

            item = items[index]

            label = (
                f"{int(item['month']):02d}/"
                f"{item['year']}"
            )

            canvas.drawCentredString(
                x,
                bottom - 9,
                label,
            )

            canvas.setFont(
                "Helvetica-Bold",
                6.5,
            )

            canvas.drawCentredString(
                x,
                y + 6,
                str(
                    int(
                        item["count"]
                    )
                ),
            )


class ReportPDFService:

    PRIMARY = colors.HexColor("#0d6efd")
    SUCCESS = colors.HexColor("#198754")
    MUTED = colors.HexColor("#6c757d")
    DARK = colors.HexColor("#212529")
    LIGHT = colors.HexColor("#f8f9fa")
    BORDER = colors.HexColor("#dee2e6")

    @staticmethod
    def _draw_footer(
        canvas_obj,
        document,
    ):

        canvas_obj.saveState()

        width, _ = A4

        canvas_obj.setStrokeColor(
            ReportPDFService.BORDER
        )

        canvas_obj.line(
            15 * mm,
            12 * mm,
            width - 15 * mm,
            12 * mm,
        )

        canvas_obj.setFont(
            "Helvetica",
            7,
        )

        canvas_obj.setFillColor(
            ReportPDFService.MUTED
        )

        canvas_obj.drawString(
            15 * mm,
            7 * mm,
            "NovaHR — Employee Management System",
        )

        canvas_obj.drawRightString(
            width - 15 * mm,
            7 * mm,
            f"Page {document.page}",
        )

        canvas_obj.restoreState()

    @staticmethod
    def generate():

        report_data = (
            ReportService.get_dashboard_data()
        )

        buffer = BytesIO()

        document = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=15 * mm,
            leftMargin=15 * mm,
            topMargin=15 * mm,
            bottomMargin=18 * mm,
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
            textColor=ReportPDFService.MUTED,
            spaceAfter=14,
        )

        section_style = ParagraphStyle(
            "SectionTitle",
            parent=styles["Heading2"],
            fontSize=12,
            leading=15,
            textColor=ReportPDFService.DARK,
            spaceAfter=8,
        )

        normal_style = ParagraphStyle(
            "ReportNormal",
            parent=styles["Normal"],
            fontSize=8,
            leading=11,
        )

        story = []

        # HEADER

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

        # KPI

        summary = report_data["summary"]

        kpi_data = [
            [
                Paragraph(
                    "<b>Total Employees</b><br/>"
                    f"<font size='18'>"
                    f"{summary['total_employees']}"
                    "</font>",
                    normal_style,
                ),
                Paragraph(
                    "<b>Active</b><br/>"
                    f"<font size='18'>"
                    f"{summary['active_employees']}"
                    "</font>",
                    normal_style,
                ),
                Paragraph(
                    "<b>Departments</b><br/>"
                    f"<font size='18'>"
                    f"{summary['total_departments']}"
                    "</font>",
                    normal_style,
                ),
                Paragraph(
                    "<b>Users</b><br/>"
                    f"<font size='18'>"
                    f"{summary['total_users']}"
                    "</font>",
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
                        ReportPDFService.LIGHT,
                    ),
                    (
                        "BOX",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        ReportPDFService.BORDER,
                    ),
                    (
                        "INNERGRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        ReportPDFService.BORDER,
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "MIDDLE",
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
                ]
            )
        )

        story.append(kpi_table)

        story.append(
            Spacer(1, 12)
        )

        # STATUS

        story.append(
            Paragraph(
                "Employee Status",
                section_style,
            )
        )

        story.append(
            ChartFlowable(
                170 * mm,
                65 * mm,
                "donut",
                report_data[
                    "employee_status"
                ],
            )
        )

        story.append(
            Spacer(1, 12)
        )

        # DEPARTMENT

        story.append(
            Paragraph(
                "Employees by Department",
                section_style,
            )
        )

        departments = report_data[
            "employees_by_department"
        ]

        department_height = max(
            45 * mm,
            len(departments) * 11 * mm,
        )

        story.append(
            ChartFlowable(
                170 * mm,
                department_height,
                "department",
                departments,
            )
        )

        story.append(
            Spacer(1, 12)
        )

        # HIRING TREND

        story.append(
            Paragraph(
                "Employee Hiring Trend",
                section_style,
            )
        )

        story.append(
            ChartFlowable(
                170 * mm,
                65 * mm,
                "hiring",
                report_data[
                    "hiring_trend"
                ],
            )
        )

        story.append(
            Spacer(1, 12)
        )

        # POSITION

        story.append(
            Paragraph(
                "Employees by Position",
                section_style,
            )
        )

        positions = report_data[
            "employees_by_position"
        ]

        position_height = max(
            45 * mm,
            len(positions) * 11 * mm,
        )

        story.append(
            ChartFlowable(
                170 * mm,
                position_height,
                "position",
                positions,
            )
        )

        story.append(
            Spacer(1, 12)
        )

        # ACTIVITY

        story.append(
            Paragraph(
                "System Activity",
                section_style,
            )
        )

        activity = report_data[
            "system_activity"
        ]

        activity_rows = [
            [
                "Action",
                "Count",
            ],
            [
                "Created",
                str(
                    activity["created"]
                ),
            ],
            [
                "Updated",
                str(
                    activity["updated"]
                ),
            ],
            [
                "Deleted",
                str(
                    activity["deleted"]
                ),
            ],
        ]

        activity_table = Table(
            activity_rows,
            colWidths=[
                120 * mm,
                50 * mm,
            ],
        )

        activity_table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        ReportPDFService.DARK,
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
                        ReportPDFService.BORDER,
                    ),
                    (
                        "ALIGN",
                        (1, 1),
                        (1, -1),
                        "CENTER",
                    ),
                    (
                        "BACKGROUND",
                        (0, 1),
                        (-1, -1),
                        ReportPDFService.LIGHT,
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

        story.append(
            activity_table
        )

        document.build(
            story,
            onFirstPage=(
                ReportPDFService._draw_footer
            ),
            onLaterPages=(
                ReportPDFService._draw_footer
            ),
        )

        buffer.seek(0)

        return buffer
