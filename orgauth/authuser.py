from .models import *
import json
import time
import os
import hashlib

def set_user_field(req, user = False):
    req.orguser = {
        'is_login' : False,
        'org_id' : '',
        'member_id' : '',
        'login_time' : 0,
        'org_role' : '',
        'user_id' : 0
    }
    if user:
        req.orguser = {
            'is_login' : True,
            'org_id' : user.org_id,
            'member_id' : user.member_id,
            'login_time' : time.time(),
            'org_role' : user.org_role,
            'user_id' : user.id
        }
    


def hash_user_passwd(passwd):
    h = hashlib.sha256()
    h.update(bytes(passwd, 'utf8'))
    return h.hexdigest()

def org_add_user(req, user):
    try:
        ou = OrgUserAuth()
        
        ou.org_id = user['org_id']
        ou.member_id = user['member_id']
        ou.org_role = user['org_role']
        ou.passwd = hash_user_passwd(user['passwd'])

        ou.save()
    except ValueError as e:
        return False
    except TypeError as e:
        return False

    return True


def org_auth(org_id, username, passwd):
    hashpasswd = hash_user_passwd(passwd)
    try:
        u = OrgUserAuth.objects.get(org_id=org_id, member_id=username, passwd=hashpasswd)
        return u
    except OrgUserAuth.DoesNotExist:
        print(org_id,username, passwd)
        return False


def org_login(req, user):
    """ req.orguser = {
        'is_login' : True,
        'org_id' : user.org_id,
        'member_id' : user.member_id,
        'login_time' : time.time(),
        'org_role' : user.org_role,
        'user_id' : user.id
    } """
    set_user_field(req, user)
    try:
        sessid = req.COOKIES['ORGSESSID']
        fd = open('/tmp/sess_'+sessid, 'w+')
        fd.write(json.dumps(req.orguser))
        fd.close()
    except IOError as e:
        return False

    return True


def org_logout(req, org_id):
    if req.orguser['org_id'] != org_id:
        return False

    if not req.orguser['is_login']:
        return True
    try:
        sess_file = '/tmp/sess_' + req.COOKIES['ORGSESSID']
        fd = open(sess_file, 'w')
        set_user_field(req, False)
        fd.write(json.dumps(req.orguser))
        fd.close()
    except OSError as e:
        print(e)
        return False
    except IOError as e:
        print(e)
        return False
    return True

