from odoo import models
from odoo.http import request
from werkzeug.utils import redirect
from werkzeug.urls import url_encode

class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    @classmethod
    def _dispatch(cls, endpoint):
        httprequest = request.httprequest
        if 'debug' in httprequest.args:
            request.session.debug = ''
            args = httprequest.args.to_dict(flat=True)
            args.pop('debug', None)
            query = url_encode(args)
            new_url = httprequest.path + (('?' + query) if query else '')
            return redirect(new_url, code=302)
        return super()._dispatch(endpoint)