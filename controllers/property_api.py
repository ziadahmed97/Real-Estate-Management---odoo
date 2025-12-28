import json
import math
from urllib.parse import parse_qs
from odoo import http
from odoo.http import request

def valid_response(data,status,pagination_info):
    response_body = {
        "data" : data,
        "message" : "successful"
    }
    if pagination_info:
        response_body['pagination_info']=pagination_info
    return request.make_json_response(response_body, status=status)
def invalid_response(error,status):
    response_body = {
        "error" : error
    }
    return request.make_json_response(response_body, status=status)
def valid_response_json(data):
    return{
        [{'message':'property created successfully'}]
}
class PropertyApi(http.Controller):
    # @http.route("/v1/property",methods=["POST"],type="http",auth="none",csrf=False)
    # def post_property(self):
    #     args = request.httprequest.data.decode()
    #     vals = json.loads(args)
    #     if not vals.get('name'):
    #         return request.make_json_response({
    #             "error": "name is required"
    #         }, status=400)
    #     try:
    #         res = request.env['property'].sudo().create(vals)
    #         if res:
    #             return request.make_json_response({
    #                 "message": "property has been created successfully",
    #                 "id": res.id,
    #                 "name": res.name
    #             }, status=201)
    #     except Exception as error:
    #         return request.make_json_response({
    #             "error": error
    #         }, status=400)
    @http.route("/v1/property", methods=["POST"], type="http", auth="none", csrf=False)
    def post_property(self):
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        # if not vals.get('name'):
        #     return request.make_json_response({
        #         "error": "name is required"
        #     }, status=400)
        try:
            # res = request.env['property'].sudo().create(vals)
            cr = request.env.cr
            columns=','.join(vals.keys())
            values = ','.join(["%s"]*len(vals))
            query=f'''Insert INTO property ({columns}) VALUES ({values}) RETURNING id, name, postcode'''
            cr.execute(query,tuple(vals.values()))
            res = cr.fetchone()
            print(res)
            if res:
                return request.make_json_response({
                    "message": "property has been created successfully",
                    "id": res[0],
                    "name": res[1],
                    "postcode" : res[2]
                }, status=201)
        except Exception as error:
            return request.make_json_response({
                "error": error
            }, status=400)

    @http.route("/v1/property/json", methods=["POST"], type="json", auth="none", csrf=False)
    def post_property_json(self):
            args = request.httprequest.data.decode()
            vals=json.loads(args)
            if not vals.get('name'):
                return {
                    "error" : "name is required"
                }
            try:
                res = request.env['property'].sudo().create(vals)
                if res:
                    return [{
                    "message": "property has been created successfully"
                    }]
            except Exception as error:
                return {
                    "error": error
                }

    @http.route("/v1/property/<int:property_id>",methods=["PUT"],type="http",auth="none",csrf=False)
    def update_property(self,property_id):
        try:
            property_id = request.env['property'].sudo().search([('id','=',property_id)])
            if not property_id:
                return request.make_json_response({
                    "error": "ID does not exist!"
                }, status=400)
            args = request.httprequest.data.decode()
            vals = json.loads(args)
            property_id.write(vals)
            return request.make_json_response({
                "message": "property has been created successfully",
                "id": property_id.id,
                "name": property_id.name,
                "bedrooms":property_id.bedrooms
            }, status=201)
        except Exception as error:
            return request.make_json_response({
                "error": error
            }, status=400)

    @http.route("/v1/property/<int:property_id>", methods=["GET"], type="http", auth="none", csrf=False)
    def get_property(self,property_id):
        try:
            property_id = request.env['property'].sudo().search([('id','=',property_id)])
            if not property_id:
                return invalid_response( "ID does not exist!", status=400)
            return valid_response({
                "id": property_id.id,
                "name": property_id.name,
                "description":property_id.description,
                "bedrooms":property_id.bedrooms
            }, status=200)
        except Exception as error:
            return invalid_response(error, status=400)

    @http.route("/v1/property/<int:property_id>", methods=["DELETE"], type="http", auth="none", csrf=False)
    def delete_property(self,property_id):
        try:
            property_id = request.env['property'].sudo().search([('id','=',property_id)])
            if not property_id:
                return request.make_json_response({
                    "error": "ID does not exist!"
                }, status=400)
            property_id.unlink()
            return request.make_json_response({
                "message" : "property has been deleted successfully"
            }, status=200)
        except Exception as error:
            return request.make_json_response({
                "error" : error
            },status=400)
    @http.route("/v1/properties",methods=["GET"],type="http",auth="none",csrf=False)
    def get_all_property_records(self):
        try:
            parms = parse_qs(request.httprequest.query_string.decode('utf-8'))
            property_domain=[]
            page  = offset = None
            limit = 5
            if parms:
                if parms.get('page'):
                    page = int(parms.get('page')[0])
                if parms.get('limit'):
                    limit= int(parms.get('limit')[0])
            if page:
                offset = (page * limit) - limit
            if parms.get('state'):
                property_domain += [('state','=',parms.get('state')[0])]
            property_ids = request.env['property'].sudo().search([])
            # property_ids = request.env['property'].sudo().search(property_domain,limit=limit,offset=offset,order='id desc')
            property_count = request.env['property'].sudo().search_count(property_domain)
            if not property_ids :
                return request.make_json_response(
                    {
                        "error" : "there are no records!"
                    }
                ,status=400)
            return valid_response([{
                "id": property_id.id,
                "name": property_id.name,
                "description": property_id.description,
                "bedrooms": property_id.bedrooms
            } for property_id in property_ids],pagination_info={
                'page': page if page else 1,
                'limit': limit,
                'pages' : math.ceil(property_count/limit) if limit else 1,
                'count':property_count
            }, status=200)

        except Exception as error:
            return invalid_response(error,status=400)