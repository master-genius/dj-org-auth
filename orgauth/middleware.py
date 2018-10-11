from .authuser import *
import time
import os
import hashlib
import random
import json

class OrgAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.sess_path = '/tmp/'

    def __call__(self, request):
        orgsessid_flag = 0
        """ user_data = {
            'is_login' : False,
            'org_role' : '',
            'org_id' : '',
            'member_id' : '',
            'user_id' : '',
            'login_time' : 0
        }
        request.orguser = user_data """
        set_user_field(request, False)

        if 'ORGSESSID' in request.COOKIES.keys():
            orgsessid_flag = 1
            cookie = request.COOKIES['ORGSESSID']
            fd = open(self.sess_path+ 'sess_'+cookie, 'r')
            udata = fd.readlines()
            fd.close()
            request.orguser = json.loads(''.join(udata))
        
        response = self.get_response(request)

        if orgsessid_flag == 0:
            sess_key = str(time.time()) + str(random.random())
            m = hashlib.md5()
            m.update(bytes(sess_key, 'utf8'))
            sessid = m.hexdigest()
            strsessid = str(sessid)
            response['Set-Cookie'] = 'ORGSESSID=' + strsessid + ';path=/'

            sess_file = 'sess_' + strsessid
            fd = open(self.sess_path + sess_file, 'w+')
            
            fd.write(json.dumps(request.orguser))
            fd.close()
        response['Access-Control-Allow-Origin'] = "*"
        return response


