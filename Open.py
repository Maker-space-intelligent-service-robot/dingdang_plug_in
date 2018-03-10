# -*- coding: utf-8-*-
# 这是语音开门插件，当语音命令说出“芝麻开门”时，通过MQTT发送命令到8266上面，实现开门
# 
# WORDS是一个关键词列表，用户存储这个插件的指令关键词（的拼音）
# 与关键词有关的还有 isValid 函数，该函数用于判断用户输入的指令是否要用这个插件来处理。
# 如果 isValid 返回结果为 true ，handle 函数就会被调用，以处理指令。

# 引入库
import paho.mqtt.publish as publish
import paho.mqtt.client as client
import sys 
import logging
import json

reload(sys)
sys.setdefaultencoding('utf8')

WORDS = ["ZHIMAKAIMEN"]

# text 是STT识别到的用户指令
def isValid(text):
    return any(word in text for word in [u"芝麻开门"]) 

# SLUG 是该插件的标识符，它主要用作在 profile.yml 中标识该插件的配置头。
# 如果在profile.xml中添加该插件的设置，就应该以 “open” 字段为开头写配置信息
# open:
#   host：'mqtt代理器的地址'
#   port:'端口号'
#   topic_p：'订阅的主题'
#   message: '发送的消息'

SLUG = "open"

# mic是麦克风和喇叭模块，通过调用mic.say()函数来让喇叭说话
# profile是用户配置信息，它是一个字典，记录了 ~/.dingdang/profile.yml 的全部内容；
def handle(text,mic,profile,wxbot=None):
    if(SLUG not in profile ) or ('host'not in profile[SLUG]) or ('port' not in profile[SLUG]) or ('topic_p' not in profile[SLUG]) or ('message' not in profile[SLUG]):
        mic.say("配置有误",cache=True)
        return
    host = profile[SLUG]['host']
    port = profile[SLUG]['port']    
    topic_p = profile[SLUG]['topic_p']
    msg = profile[SLUG]['message']
# 因为是偶尔需要发布消息，所以不需要mqtt broker 保持连线，这里采用single方法
# public a message then disconnect

    # if broker asks user/password
    auth = {'username':"",'password':""}
    
    # if broker asks client ID 
    client_id=""
    try:
        publish.single(topic_p,msg,qos=1,hostname=host,port=port)
        # publish.single(topic_p,msg,qos = 1,hostname=host,port=port,auth=auth,client_id=client_id)
        mic.say("开门指令已发出",cache=True)
    except Exception,e:
        logger.error(e)
        mic.say('抱歉，mqtt存在错误，指令不能发出')
        

    
