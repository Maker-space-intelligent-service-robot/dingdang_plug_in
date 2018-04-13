# -*- coding: utf-8-*-

import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import sys 
import logging
import json
import os
import time

reload(sys)
sys.setdefaultencoding('utf8')

WORDS = ["TIANQI"]
SLUG = "realtimetq"

#def get_topic(text):
#    home_dir = os.path.expandvars('$HOME')
#    location = home_dir + '/pi/.dingdang/action.json'
#    f = open(location).read()
#    fjson = json.loads(f)
#    topic = None
#    for key in fjson.keys():
#        if text in fjson[key]:
#            topic = key
#    return topic

def handle(text, mic, profile, wxbot=None):
    
    logger = logging.getLogger(__name__)
    
    if(SLUG not in profile ) or ('host'not in profile[SLUG]) or ('port' not in profile[SLUG]) or ('topic_s' not in profile[SLUG]) or ('message' not in profile[SLUG]):
        mic.say("配置有误", cache=True)
        return
    
    host = profile[SLUG]['host']
    port = profile[SLUG]['port']
    topic_s = profile[SLUG]['topic_s']
    topic_p = profile[SLUG]['topic_p']
    message = profile[SLUG]['message']
    
    #text = text.split("，")[0]
    #topic_p = get_topic(text)
    
    #if topic_p == None:
    #    return
    
    try:
        mic.say("实时天气指令已发出", cache=True)
        mqtt_contro(host, port, topic_s, topic_p, text, mic)
    except Exception as e:
        logger.error(e)
        mic.say('抱歉，mqtt存在错误，指令不能发出', cache=True)
        return

def isValid(text):
    return any(word in text for word in [u"气象站",u"天气",u"气温"])
    

class mqtt_contro(object):
    
    def __init__(self, host, port, topic_s, topic_p, message, mic):
        self._logger = logging.getLogger(__name__)
        self.host = host
        self.port = port
        self.topic_s = topic_s
        self.topic_p = topic_p
        self.message = message
        self.mic = mic
        self.mqttc = mqtt.Client()
        self.mqttc.on_message = self.on_message
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_publish = self.on_publish
        if self.host and self.topic_p:
            publish.single(self.topic_p, payload=self.message, qos=1, hostname=self.host, port=self.port)
        if self.port and self.topic_s :
            self.mqttc.connect(self.host, self.port, 5)
            self.mqttc.subscribe(topic_s, 0)
            self.mqttc.loop_start()
            
    def on_connect(self, mqttc, obj, flags, rc):
        if rc == 0:
            pass
        else:
            print("error connect")
            
    def on_publish(self, mqttc, obj, mid):
        self.mic.say("hi")
        self.mic.say(str(mid))
        self.mic.say("hello")
            
    def on_message(self, mqttc, obj, message):
        if message.payload:
            self.mqttc.loop_stop()
            self.mqttc.disconnect()
            self.mic.say( str(message.payload) )
        else:
            time.sleep(5)
            self.mqttc.loop_stop()
            self.mqttc.disconnect()
            self.mic.say( 'run time error', cache=True )
#
#






















