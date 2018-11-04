from __future__ import absolute_import
from __future__ import print_function

import logging

import django

from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.signals import user_logged_out
from django.contrib.auth.signals import user_login_failed
from django.dispatch import receiver

from pwdtk.auth_backends import MHPwdPolicyBackend


logger = logging.getLogger(__name__)
logger.debug("Imp backend2 sigs")  # for debugging dj 1.8 -> 1.11

NOT_SET = object()

get_backend = MHPwdPolicyBackend.get_backend


@receiver(user_login_failed)
def handle_loginfailed(sender, credentials, **kwargs):
    if not isinstance(credentials, dict) or 'username' not in credentials:
        return
    username = credentials['username']
    print("LOGIN_FAILED for", username, "KWARGS", kwargs)
    get_backend().handle_failed_login(username)


@receiver(user_logged_in)
def handle_login(sender, **kwargs):
    if 'request' not in kwargs:
        return
    user = getattr(kwargs['request'], 'user',  NOT_SET)
    if user is NOT_SET:
        logger.debug("login without username")
        return
    print("LOGIN as %s" % user.username)
    get_backend().clear_failed_logins(user=user)


if django.VERSION >= (2, 2):
    @receiver(user_logged_out)
    def handle_logout(sender, **kwargs):
        print("LOGOUT", kwargs)
