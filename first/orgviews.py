import json
from django.shortcuts import render
from django.views import View
from django.http.response import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.middleware import csrf
from django.db.utils import IntegrityError
import time
from .models import *
import os
from orgauth.authuser import *
from orgauth.mixins import *

def api_test(req):
    host_str = req.get_host()
    host = host_str
    if ':' in host_str:
        host = host_str.split(':')[0]

    return render(req, 'api_test.html', {'host':host})


class OrgRootView(View):
    def __init__(self,):
        pass

    def dispatch(self, req, *args, **argv):
        ret = super().dispatch(req, *args, **argv)
        return ret

    def get(self, req):
        pass

    def post(self, req):
        pass


class OrgBindPlatView(OrgLoginRequiredMixin,OrgRootView):
    def dispatch(self, req, *args, **argv):
        ret = super(OrgBindPlatView, self).dispatch(req, *args, **argv)
        return ret

    def get(self, req, org_id):
        return JsonResponse({
            'csrftoken':csrf.get_token(req)
        })

    def post(self, req, org_id):
        username = req.POST['username']
        passwd = req.POST['passwd']
        u = authenticate(req, username=username, password=passwd)
        if u is None:
            return JsonResponse({
                'status' : -1,
                'errval' : 'auth failed'
            })
        
        ret_info = {'status':0, 'info':'success'}
        has_bind = 1
        try:
            ob = OrgBind.objects.get(plat_id=u.id, org_id=org_id, member_id=req.orguser['member_id'])
        except OrgBind.DoesNotExist:
            has_bind = 0
        if has_bind:
            return JsonResponse({
                'status' : -1,
                'errval' : 'has bind'
            })
            
        try:
            b = OrgBind(
                plat_id = u.id,
                org_id =  org_id,
                member_id = req.orguser['member_id'],
            )
            b.save()
        except ValueError as e:
            print(e)
            ret_info = {'status':-1, 'errval':'bind failed'}
        except TypeError as e:
            print(e)
            ret_info = {'status':-1, 'errval':'bad data'}
        except IntegrityError as e:
            print(e)
            ret_info = {'status':-1, 'errval':'disabled to bind more'}

        return JsonResponse(ret_info)


class OrgLoginView(OrgRootView):
    def dispatch(self, req, *args, **argv):
        if req.orguser['is_login']:
            return JsonResponse({
                'status':-1,
                'errval':'already login'
            })
        ret = super().dispatch(req, *args, **argv)
        return ret

    def get(self, req, org_id):
        token_text = json.dumps({
            'csrftoken':csrf.get_token(req)
        })
        return HttpResponse(token_text+"\n")

    def post(self, req, org_id):
        print(org_id)
        username = req.POST['username']
        passwd = req.POST['passwd']
        org_id = org_id

        u = org_auth(org_id, username, passwd)
        if u:
            org_login(req, u)
            return JsonResponse({'status':0, 'info':'success'})
        else:
            return JsonResponse({'status':-1, 'errval':'failed'})

class OrgAddMemberView(OrgLoginRequiredMixin, OrgRootView):
    def dispatch(self, req, *args, **argv):
        ret = super(OrgAddMemberView, self).dispatch(req, *args, **argv)
        return ret

    def get(self, req, org_id):
        return JsonResponse({
            'csrftoken':csrf.get_token(req)
        })

    def post(self, req, org_id):
        user = {
            'member_id' : req.POST['username'],
            'passwd' : req.POST['passwd'],
            'org_role' : req.POST['org_role'],
            'org_id' : org_id
        }
        if org_add_user(req, user):
            return JsonResponse({
                'status':0,
                'info':'success'
            })
        else:
            return JsonResponse({
                'status':-1,
                'info':'Error: register failed'
            })



def org_user_logout(req, org_id):
    if org_logout(req, org_id):
        return JsonResponse({'status':0, 'info':'ok'})
    else:
        return JsonResponse({'status':-1, 'errval':'logout error'})

