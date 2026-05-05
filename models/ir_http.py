from odoo import models
from odoo.http import request
from werkzeug.utils import redirect
from werkzeug.urls import url_encode
import os

class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    @classmethod
    def _dispatch(cls, endpoint):
        key = os.environ.get('DISABLE_DEBUG_KEY')
        httprequest = request.httprequest

        if 'debug' in httprequest.args:
            debug_value = httprequest.args.get('debug')

            if key and debug_value == key:
                request.session.debug = '1'
                return super()._dispatch(endpoint)

            request.session.debug = ''
            args = httprequest.args.to_dict(flat=True)
            args.pop('debug', None)
            query = url_encode(args)
            new_url = httprequest.path + (('?' + query) if query else '')
            return redirect(new_url, code=302)

        return super()._dispatch(endpoint)