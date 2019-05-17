#---------------------------------------------#
# Verifier - Discord/Unity Asset Verification #
# Created by isntance.id - http://instance.id #
# github.com/instance-id - system@instance.id #
#---------------------------------------------#
#  License subscription verification system   #

# import instance.instanceid as i
# from uuid import getnode as get_mac
# import threading
# import time
# import os
# import logging
# import asyncio
# import requests
# import platform
# import jsoncfg
#
# # <editor-fold desc="Logging definitions">
# from colorlog import ColoredFormatter
#
# log = logging.getLogger(__name__)
# LOG_LEVEL = logging.INFO
# LOGFORMAT = "  %(log_color)s%(levelname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s"
# logging.root.setLevel(LOG_LEVEL)
# formatter = ColoredFormatter(LOGFORMAT)
# stream = logging.StreamHandler()
# stream.setLevel(LOG_LEVEL)
# stream.setFormatter(formatter)
# log.setLevel(LOG_LEVEL)
# log.addHandler(stream)
# # </editor-fold>
#
# config = jsoncfg.load_config('config/license.json')
# loop = asyncio.get_event_loop()
# gatekeeper = 0
# run = True
#
# wcapi = 'software-api'
# check = 'check'
# activate = 'activation'
# product_id = 'verifier'
# version = "1.0.0"
# platform_info = platform.platform()
# license_key = config.licensekey()
# email = config.emailaddress()
# instance = get_mac()
#
#
# def v_switch(arg):
#     choices = {
#         201: "Active",
#         404: "Demo",
#         410: "Demo",
#     }
#     return choices.get(arg, "Received incorrect response type from server.")
#
#
# def lic_exist(key, email):
#     if len(key) > 2:
#         if len(email) > 2:
#             return True
#
#
# class Startup:
#     def __init__(self):
#         self.a = 1
#         self.b = 2
#
#     async def licactivate():
#         data = {'product_id': product_id,
#                 'platform': platform_info,
#                 'instance': instance,
#                 'license_key': license_key,
#                 'email': email,
#                 'request': activate,
#                 'wc-api': wcapi}
#
#         r = requests.post('https://instance.id/', data=data)
#         return r.json()
#
#     async def liccheck():
#         data = {'product_id': product_id,
#                 'platform': platform_info,
#                 'instance': instance,
#                 'license_key': license_key,
#                 'email': email,
#                 'request': check,
#                 'wc-api': wcapi}
#
#         r = requests.post('https://instance.id/',
#                           data=data)
#         data = r.json()
#
#         if data['remaining'] == 1:
#             result = await Startup.licactivate()
#             return 201
#         else:
#             if data['activations'][0]['instance'] == str(instance):
#                 if data['activations'][0]['isvalid'] == '1':
#                     return 201
#                 else:
#                     print('Subscription inactive. Please visit https://instance.id to acquire an active subscription.')
#                     return 410
#             else:
#                 print(
#                     'Verifier is already registered to another machine. Please contact support at https://instance.id/contact/')
#                 exit(1)
#
#     async def licensecheck():
#         exists = lic_exist(license_key, email)
#         if exists:
#             data = await Startup.liccheck()
#             global gatekeeper
#             gatekeeper = data
#             return
#         else:
#             print('License key missing. Please check license.json.')
#             exit(1)
#
#     async def check_run():
#         result = await Startup.licensecheck()
#         return result
#
#
# class Periodic:
#     def __init__(self, interval=3600):
#         self.interval = interval
#         self.thread = threading.Thread(target=self.periodic_check, args=())
#         self.thread.daemon = True
#         self.thread.start()
#
#     def periodic_check(self):
#         global run
#         while run:
#             data = {'product_id': product_id,
#                     'platform': platform_info,
#                     'instance': instance,
#                     'license_key': license_key,
#                     'email': email,
#                     'request': check,
#                     'wc-api': wcapi}
#
#             r = requests.post('https://instance.id/',
#                               data=data)
#             data = r.json()
#
#             if data['activations'][0]['instance'] == str(instance):
#                 if data['activations'][0]['isvalid'] == '1':
#                     time.sleep(self.interval)
#                     pass
#                 else:
#                     print('Subscription inactive. Please visit https://instance.id to acquire an active subscription.')
#                     os._exit(1)
#                     run = False
#             else:
#                 print(
#                     'Verifier is already registered to another machine. Please contact support at https://instance.id/contact/')
#                 exit(1)
#
#
# tasks = [asyncio.ensure_future(Startup.check_run())]
#

# Enable this section to use license verification
# def start():
#     global run
#     s = loop.run_until_complete(asyncio.wait(tasks))
#     f_result = v_switch(gatekeeper)
#     if f_result is 'Active':
#         r = Periodic()
#         i.InstanceId.start()
#     else:
#         print('License is not currently active.')
