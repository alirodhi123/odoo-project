# -*- coding: utf-8 -*-
import functools
import base64
import json
import logging

from odoo import _
from odoo.http import Controller, route, request, Response
import copy


def webservice(f):
    @functools.wraps(f)
    def wrap(*args, **kw):
        try:
            return f(*args, **kw)
        except Exception, e:
            return Response(response=str(e), status=500)
    return wrap


class UploadDocument(Controller):

    @route('/plm_document_upload/isalive', type='http', auth='none', methods=['GET'], csrf=False)
    @webservice
    def isalive(self):
        return Response('True', status=200)

    @route('/plm_document_upload/login', type='http', auth='none', methods=['POST'], csrf=False)
    @webservice
    def login(self, login, password, db=None):
        if db and db != request.db:
            raise Exception(_("Could not select database '%s'") % db)
        uid = request.session.authenticate(request.db, login, password)
        if not uid:
            return Response(response="Wrong login/password", status=401)
        return Response(headers={
            'X-CSRF-TOKEN': request.csrf_token(),
        })

    @route('/plm_document_upload/upload', type='http', auth='user', methods=['POST'])
    @webservice
    def upload(self, mod_file=None, doc_id=False, filename='', **kw):
        logging.info('start upload %r' % (doc_id))
        if doc_id:
            logging.info('start json %r' % (doc_id))
            doc_id = json.loads(doc_id)
            logging.info('start write %r' % (doc_id))
            value1 = mod_file.stream.read()
            request.env['plm.document'].browse(doc_id).write(
                {'datas': base64.b64encode(value1),
                 'datas_fname': filename,
                 })
            logging.info('upload %r' % (doc_id))
            return Response('Upload succeeded', status=200)
        logging.info('no upload %r' % (doc_id))
        return Response('Failed upload', status=200)

    @route('/plm_document_upload/download', type='http', auth='user', methods=['GET'])
    @webservice
    def download(self, requestvals, **kw):
        logging.info('Request documents %r to download' % (requestvals))
        if not requestvals:
            logging.info('No file requests to download')
            return Response([], status=200)
        requestvals = json.loads(requestvals)
        plmDocEnv = request.env['plm.document']
        result = plmDocEnv.GetSomeFiles(requestvals)
        content = ''
        result2 = {}
        if result:
            # Content need to be passed as first argument, in the client tuple will be recomposed
            result2 = copy.deepcopy(list(result[0]))
            content = result2[2]
            result2[2] = ''
        return Response(content, headers={
            'result': [result2]
            })
#         return Response(headers={
#             'result': result,
#         }, status=200)
