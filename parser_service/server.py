#!/usr/bin/env python

from aiohttp import web
from permissions_service import PermissionsService

routes = web.RouteTableDef()

permissions_service = PermissionsService()

@routes.get('/permissions')
async def handle(request):
    app_id = request.query.get('appId')
    hl = request.query.get('hl') or 'en'

    if not app_id:
        raise web.HTTPBadRequest(reason='appId parameter is required')

    permissions = await permissions_service.get_permission(app_id, hl)

    if not permissions:
        await permissions_service.add_query(app_id, hl)
        raise web.HTTPNotFound()

    return web.json_response(
        {
            'app_id': app_id,
            'hl': hl,
            'permissions': permissions['permissions']
        }
    )

def set_cors_headers(request, response):
    response.headers['Access-Control-Allow-Origin'] = request.headers.get(
        'Origin', '*'
    )
    response.headers['Access-Control-Allow-Methods'] = 'GET,OPTIONS'

    return response


async def cors_factory (app, handler):
    async def cors_handler(request):
        if request.method == 'OPTIONS':
            response = web.Response(status=204)
            return set_cors_headers(request, response)

        response = await handler(request)
        return set_cors_headers(request, response)

    return cors_handler

app = web.Application(middlewares=[cors_factory])
app.add_routes(routes)

web.run_app(app, host='0.0.0.0', port=8080)