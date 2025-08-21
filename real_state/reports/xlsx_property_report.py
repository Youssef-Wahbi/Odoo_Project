import io
import xlsxwriter
from odoo import http, models
from odoo.http import request
from odoo.exceptions import UserError


class XlsxPropertyReport(http.Controller):

    @http.route('/property/excel/report', type='http', auth="user")
    def download_property_excel_report(self, **kwargs):
        """Download Excel report for selected properties"""
        property_ids = kwargs.get('property_ids', '')
        
        if not property_ids:
            return "No properties selected"
        
        # Convert string of IDs to list
        if isinstance(property_ids, str):
            property_ids = [int(pid) for pid in property_ids.split(',') if pid.isdigit()]
        
        # Get properties
        properties = request.env['property'].sudo().browse(property_ids)
        
        if not properties:
            return "No valid properties found"
        
        # Generate Excel
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Properties')

        # Styles
        header_format = workbook.add_format({
            'bold': True, 
            'bg_color': '#4F81BD', 
            'font_color': 'white',
            'border': 1,
            'align': 'center'
        })
        data_format = workbook.add_format({
            'border': 1, 
            'align': 'left'
        })
        price_format = workbook.add_format({
            'num_format': '$#,##0.00', 
            'border': 1, 
            'align': 'center'
        })
        date_format = workbook.add_format({
            'num_format': 'yyyy-mm-dd',
            'border': 1,
            'align': 'center'
        })

        # Headers
        headers = [
            ('ID', 'id'),
            ('Name', 'name'),
            ('Reference', 'ref'),
            ('Description', 'description'),
            ('State', 'state'),
            ('Expected Price', 'expected_price'),
            ('Selling Price', 'selling_price'),
            ('Bedrooms', 'bedrooms'),
            ('Living Area', 'living_area'),
            ('Garden', 'garden'),
            ('Garden Area', 'garden_area'),
            ('Postcode', 'postcode'),
            ('Expected Selling Date', 'expected_selling_date'),
            ('Owner', 'owner_id.name'),
            ('Create Time', 'create_time')
        ]
        
        for col_num, (header, _) in enumerate(headers):
            worksheet.write(0, col_num, header, header_format)
            worksheet.set_column(col_num, col_num, 15)

        # Data
        row_num = 1
        for prop in properties:
            for col_num, (_, field) in enumerate(headers):
                value = self._get_field_value(prop, field)
                
                # Apply specific formatting
                if field in ['expected_price', 'selling_price']:
                    worksheet.write(row_num, col_num, value, price_format)
                elif field in ['expected_selling_date', 'create_time'] and value:
                    worksheet.write(row_num, col_num, value, date_format)
                else:
                    worksheet.write(row_num, col_num, value, data_format)
            row_num += 1

        workbook.close()
        output.seek(0)

        return request.make_response(
            output.read(),
            headers=[
                ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                ('Content-Disposition', f'attachment; filename="properties_report_{len(properties)}_items.xlsx"')
            ]
        )
    
    def _get_field_value(self, property, field):
        """Get formatted value for a field"""
        if '.' in field:  # Related field like 'owner_id.name'
            obj = property
            for part in field.split('.'):
                obj = getattr(obj, part, None)
                if not obj:
                    return ''
            value = obj
        else:
            value = getattr(property, field, '')
        
        # Format specific fields
        if field == 'garden':
            return 'Yes' if value else 'No'
        elif field == 'expected_selling_date' and value:
            return value
        elif field == 'create_time' and value:
            return value
        elif field in ['expected_price', 'selling_price', 'bedrooms', 'living_area', 'garden_area']:
            return value or 0
        else:
            return value or ''


class Property(models.Model):
    _inherit = 'property'
    
    def generate_excel_report(self):
        """Generate Excel report for selected properties"""
        if not self:
            raise UserError("Please select at least one property to generate the report.")
        
        # Create URL with property IDs
        property_ids = ','.join(str(prop.id) for prop in self)
        url = f'/property/excel/report?property_ids={property_ids}'
        
        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'self',
        }
