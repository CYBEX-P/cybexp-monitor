#!/usr/bin/env python3 

# temporary so i dont have to install tahoe

import sys 
sys.path.append("../tahoe0.7")


from tahoe import Instance
from tahoe.identity import IdentityBackend

from loadconfig import get_identity_backend #, get_apiconfig


import time, pymongo, sys, datetime, subprocess

import markdown_gen
import os

# import argparse
# import logging
# import pdb
# import signal
# import time
# import sys


# Logging
##logging.basicConfig(filename = 'input.log') 
# logging.basicConfig(
#    level=logging.ERROR,
#    format='%(asctime)s %(levelname)s %(filename)s:%(lineno)s' \
#    ' - %(funcName)() --  %(message)s'
#    )


check_interval = 30

_BACKEND = get_identity_backend()


##def send_signals(_ALL_THREAD, sig):
##    for _, thread in _ALL_THREAD:
##        thread.signal_handler(sig)
##
##
##def signal_handler(sig, frame):
##    global _ALL_THREAD, _NUM_EXIT_ATTEMPT, _PLUGINS_TO_RUN
##    
##    logging.info(f"handled signal {sig}, {frame}")
##    
##    if sig in [signal.SIGINT, signal.SIGTERM]:
##        logging.info(f"# EXIT Attempt: {_NUM_EXIT_ATTEMPT}")
##        _NUM_EXIT_ATTEMPT +=1
##        
##        if _NUM_EXIT_ATTEMPT < 2:
##            signal_to_send = signal.SIGTERM
##        else:
##            signal_to_send = signal.SIGKILL
##
##        try:
##            send_signals(_ALL_THREAD, signal_to_send)
##        except:
##            pass
##    elif sig == signal.SIGUSR1:
##        logging.info("restarting all input...")
##        send_signals(_ALL_THREAD, signal.SIGTERM)
##        time.sleep(1)
##        _ALL_THREAD = run_input_plugins(_PLUGINS_TO_RUN) 
##        logging.info("successfully restarted all input.")



def run(command):
   outp = subprocess.run(command.split())
   return outp

def smash(dat):
   try:
      for k in dat.keys():
         if isinstance(dat[k], list) and len(dat[k]) == 1:
            dat[k] = dat[k][0]
   except:
      pass
   return dat


STATUS_DOC = ''
def clear_status():
   global STATUS_DOC
   STATUS_DOC = ""

def create_status_bioler():
   global STATUS_DOC
   title = markdown_gen.make_title("Input Status")
   table_head = markdown_gen.create_table_header(["Name", "Status"], 2)

   STATUS_DOC = STATUS_DOC + title + table_head
def add_status(name, badge, online=None):
   global STATUS_DOC

   if online:
      print("status: {}\t\tname: {}".format(online,name))

   row = markdown_gen.create_table_row([name,badge])

   STATUS_DOC = STATUS_DOC+row

def publish_status():
   global STATUS_DOC
   with open("README.md", "w") as f:
      f.write(STATUS_DOC)

   run("git commit -am '.'")
   run("git push")





def auto_color(dat):
   if dat == True:
      return "green"
   elif dat == False:
      return "red"
   else:
      return "blue"

def bool2online(b):
   if b == True:
      return "online"
   elif b == False:
      return "offline"
   else:
      return b



configs = list()
def update_configs():
   global configs, all_plugin, _BACKEND
   configs = list()
   # print([c for c in _BACKEND.find({})])
   for input_config in _BACKEND.get_config(all_plugin):
      data = smash(input_config["data"])
      hash_ = input_config["_hash"]

      temp = {"hash": hash_}
      temp.update(data)

      print(temp)
      configs.append(temp)

if __name__ == "__main__":

   # Instance._backend = _BACKEND

   all_plugin = _BACKEND.get_all_plugin()
       

       
#    signal.signal(signal.SIGINT, signal_handler) 
##    signal.signal(signal.SIGTERM, signal_handler) 
##    signal.signal(signal.SIGUSR1, signal_handler) 



   try:
      os.chdir("status")

      last_check = time.time()
      status_log = dict()
      while True:
         update_configs()
         
         with pymongo.MongoClient("mongodb://localhost:27017") as client:

            new_records_cursor = client.cache_db.file_entries.find({"timestamp": { "$gt": last_check } })
            query_time = time.time()

            
            new_hashes = [ a["config_hash"] for a in new_records_cursor if "config_hash" in a]
            
            new_hashes = list(set(new_hashes))

            
            clear_status()
            create_status_bioler()
            for conf in configs:
               name = conf["name"]
               badge_name = "status"

               try:
                  online = conf["hash"] in new_hashes
               except:
                  online = False

               if "seconds_between_fetches" in conf:
                  badge_name = "last seen"
                  if online:
                     online = datetime.datetime.fromtimestamp(query_time)
                     status_log[conf["hash"]] = online
                  else:
                     try:
                        online = status_log[conf["hash"]]
                     except:
                        online = False
                        status_log[conf["hash"]] = online

                  # TODO this gets oewritten next interval if second between faetches is bigger than recheck interval 

               status_badge = markdown_gen.make_badge(badge_name,bool2online(online), auto_color(online), cache_seconds=check_interval)

               add_status(name,status_badge)




            publish_status()
            last_check = query_time

         time.sleep(check_interval)



      # connect to cache
      # fetch all since last connection (last_check = time.time())
      # filter based on the above configs
      # for every config 
      #   create metrics
      #   add to global metrics

      # post metrics

         # plugin_name = input_config['data']['plugin'][0]
         # try:
         #    Plugin = _NAME_TO_PLUGIN_MAP[plugin_name] 
         #    thread =  Plugin(input_config, api_config)
         #    thread.start()
         #    _ALL_THREAD.append((input_config, thread))
         # except:
         #    logging.error("Fail to run thread({plugin_name}).")

         # return _ALL_THREAD
   except KeyboardInterrupt:
      sys.exit(0)