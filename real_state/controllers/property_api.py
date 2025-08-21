import json
from urllib.parse import parse_qs
from odoo import http
from odoo.http import request

class PropertyApi(http.Controller):

    def valid_response(self, message, data=None, status_code=200):
        """Helper method for valid responses"""
        response = {
            "message": message,
            "status": "success"
        }
        if data is not None:
            response["data"] = data
        return request.make_json_response(response, status=status_code)

    def invalid_response(self, message, status_code=400, data=None):
        """Helper method for invalid responses"""
        response = {
            "message": message,
            "status": "error"
        }
        if data is not None:
            response["data"] = data
        return request.make_json_response(response, status=status_code)

    @http.route('/test', auth='none', type='http', methods=['GET'], csrf=False)
    def test(self):
        return self.valid_response('API is working!')

    @http.route("/v1/property", auth='none', type='http', methods=['POST'], csrf=False)
    def post_property(self):
        try:
            args = request.httprequest.data.decode()
            vals = json.loads(args)
            print("11111111111111111111111111", vals)
            res = request.env['property'].sudo().create(vals)
            if res:
                return self.valid_response("Property has been created successfully", status_code=200)
            else:
                return self.invalid_response("Failed to create property", status_code=400)
        except Exception as error:
            return self.invalid_response(str(error), status_code=500)

    @http.route('/api/property/<int:property_id>', methods=['PUT'], type='http', auth='none', csrf=False)
    def update_property(self, property_id):
        try:
            property_record = request.env['property'].sudo().search([('id', '=', property_id)])

            if not property_record:
                return self.invalid_response("Property not found", status_code=404)

            args = request.httprequest.data.decode('utf-8')
            vals = json.loads(args)

            property_record.write(vals)
            request.env.cr.commit()

            data = {
                "id": property_record.id,
                "name": property_record.name,
                "description": property_record.description
            }
            return self.valid_response("Property has been updated successfully", data, status_code=200)
        except Exception as error:
            return self.invalid_response(str(error), status_code=500)

    @http.route('/api/property/<int:property_id>', methods=['GET'], type='http', auth='none', csrf=False)
    def get_property(self, property_id):
        try:
            property_record = request.env['property'].sudo().browse(property_id)

            if not property_record.exists():
                return self.invalid_response("ID does not exist!", status_code=400)

            data = {
                "id": property_record.id,
                "name": property_record.name,
                "ref": property_record.ref,
                "description": property_record.description,
                "bedrooms": property_record.bedrooms,
            }
            return self.valid_response("Property fetched successfully", data, status_code=200)

        except Exception as error:
            return self.invalid_response(str(error), status_code=400)

    @http.route('/api/property/<int:property_id>', methods=['DELETE'], type='http', auth='none', csrf=False)
    def delete_property(self, property_id):
        try:
            property_record = request.env['property'].sudo().search([('id', '=', property_id)])

            if not property_record:
                return self.invalid_response("Property not found", status_code=404)

            property_record.unlink()

            data = {"deleted_id": property_id}
            return self.valid_response("Property has been deleted successfully", data, status_code=200)

        except Exception as error:
            return self.invalid_response(str(error), status_code=500)

    @http.route('/v1/properties', methods=["GET"], type="http", auth="none", csrf=False)
    def get_property_list(self):
        try:
            params = parse_qs(request.httprequest.query_string.decode('utf-8'))
            print("Query Params:", params)

            property_domain = []

            if params.get('state'):
                property_domain.append(('state', '=', params.get('state')[0]))

            
            page = int(params.get('page', [1])[0]) if params.get('page') else 1
            limit = int(params.get('limit', [10])[0]) if params.get('limit') else 10
            
           
            offset = (page - 1) * limit

            
            total_count = request.env['property'].sudo().search_count(property_domain)
            
           
            property_ids = request.env['property'].sudo().search(
                property_domain, 
                limit=limit, 
                offset=offset
            )

            if not property_ids:
                return self.valid_response("No properties found", {
                    "properties": [],
                    "pagination": {
                        "page": page,
                        "limit": limit,
                        "total": total_count,
                        "pages": 0
                    }
                }, status_code=200)

            result = [{
                "id": rec.id,
                "name": rec.name,
                "description": rec.description,
                "state": rec.state
            } for rec in property_ids]

           
            total_pages = (total_count + limit - 1) // limit

            pagination_data = {
                "properties": result,
                "pagination": {
                    "page": page,
                    "limit": limit,
                    "total": total_count,
                    "pages": total_pages,
                    "has_next": page < total_pages,
                    "has_prev": page > 1
                }
            }

            return self.valid_response("Properties fetched successfully", pagination_data, status_code=200)
        except Exception as error:
            return self.invalid_response(str(error), status_code=500, data=[])