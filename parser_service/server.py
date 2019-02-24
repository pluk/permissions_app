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


app = web.Application()
app.add_routes(routes)

web.run_app(app, host='0.0.0.0', port=80)