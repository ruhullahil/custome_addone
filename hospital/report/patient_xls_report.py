from odoo import models

class PartnerXlsx(models.AbstractModel):
    _name = 'report.hospital.patient_card_id_xls'
    _inherit = 'report.odoo_report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, line):
        c = 0
        for lines in line:
            c += 1
            format1 = workbook.add_format({'font_size': 14, 'align': 'vcenter', 'bold': True})
            format2 = workbook.add_format({'font_size': 10, 'align': 'vcenter', })
            sheet = workbook.add_worksheet('Patient Card %s' % (c))
            sheet.set_column(3, 3, 50)
            sheet.set_column(2, 2, 30)
            sheet.write(2, 2, 'Name', format1)
            sheet.write(2, 3, lines.name, format2)
            sheet.write(3, 2, 'Date of Bath', format1)
            sheet.write(3, 3, lines.date_of_bath, format2)