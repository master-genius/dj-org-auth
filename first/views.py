from django.shortcuts import render
from django.views import View
from django.http.response import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.middleware import csrf
import time
from .models import *
import os
from orgauth.authuser import *
from orgauth.models import *

class RootView(View):
    def dispatch(self, req, *args, **argv):    
        ret = super(RootView, self).dispatch(req, *args, **argv)
        return ret

    def get(self, req):
        pass

    def post(self, req):
        pass


class LoginView(RootView):
    def dispatch(self, req, *args, **argv):
        ret = super(LoginView, self).dispatch(req, *args, **argv)
        return ret

    def get(self, req):
        return JsonResponse({
            'csrftoken':csrf.get_token(req)
        })

    def post(self, req):
        username = req.POST['username']
        passwd = req.POST['passwd']
        u = authenticate(req, username=username, password=passwd)
        if u is not None:
            req.session['orgbind'] = False
            try:
                bind_list = OrgBind.objects.filter(plat_id = u.id).values()
                #print(bind_list)
                bind_dict = {}
                org_midlist = []
                for b in bind_list:
                    org_midlist.append(b['member_id'])
                
                org_list = OrgUserAuth.objects.filter(member_id__in=org_midlist)
                print(org_midlist,org_list)
                for g in org_list.values():
                    bind_dict[ g['org_id'] ] = g
                
                req.session['orgbind'] = bind_dict
            except OrgBind.DoesNotExist:
                pass
            except OrgUserAuth.DoesNotExist:
                pass

            login(req, u)
            return JsonResponse({
                'status':0,
                'info':'success',
            })
        else:
            return JsonResponse({
                'status':1,
                'errval':'login failed'
            })


class RegisterView(RootView):
    def dispatch(self, req, *args, **argv):
        ret = super(RegisterView, self).dispatch(req, *args, **argv)
        return ret

    def get(self, req):
        return JsonResponse({
            'csrftoken':csrf.get_token(req)
        })

    def post(self, req):
        username = req.POST['username']
        passwd = req.POST['passwd']
        user_email = req.POST['email']
        try:
            user = User.objects.create_user(username, user_email, passwd)
            user.save()
            return JsonResponse({
                'status':0,
                'info':'success'
            })
        except ValueError as e:
            return JsonResponse({
                'status':-1,
                'errval':'register failed'
            })

def user_logout(req):
    logout(req)
    return JsonResponse({'status':0, 'info':'ok'})

