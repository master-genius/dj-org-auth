from django.contrib.auth.mixins import *
from django.conf import settings
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.http.response import HttpResponse,JsonResponse
from .permtable import *


class OrgLoginRequiredMixin:

    def checkPerm(self, role, pathinfo):
        if role == 'orgadmin':
            return True

        apiname = pathinfo.split('/')[-1]

        if role in PERM_DEFAULT_ROLE:
            if PERM_TABLE[role] == '*':
                return True
            if apiname in PERM_TABLE[role]:
                return True
            return False
        else:
            return False

        return True

    def dispatch(self, req, *args, **argv):
        #print(req.orguser)
        #print(req.COOKIES['ORGSESSID'])
        if not req.orguser['is_login']:
            print(req.session['orgbind'])
            has_bind = False 
            if  req.session['orgbind']:
                has_bind = True
                if not argv['org_id'] in req.session['orgbind'].keys():
                    has_bind = False

            if not req.user.is_authenticated or has_bind==False:
                return JsonResponse({
                    'status'  : -1,
                    'errval' : 'not login'
                })
        else:
            orgu = req.orguser
            if not orgu['is_login']:
                orgu = req.session['orgbind'][argv['org_id']]
            elif req.orguser['org_id'] != argv['org_id']:
                return JsonResponse({
                    'status' : -1,
                    'errval' : 'org mismatching'
                })
            has_perm = self.checkPerm(orgu['org_role'], req.path_info)
            if not has_perm:
                return JsonResponse({
                        'status'  : -1,
                        'errval' : 'permission deny'
                    })

        return super(OrgLoginRequiredMixin,self).dispatch(req, *args, **argv)

