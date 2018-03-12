# -*- coding: utf-8 
# 需要安装psycopg2
# 这个是寻找工具位置的插件，首先从数据库中获得工具的坐标，然后将其通过mqtt将其发送出去，控制灯进行闪烁
# 在/home/pi/.dingdang下建立一个tool.json文件，用来存放所有的工具名称
#文件里面的内容格式为：
#{"tool":["锤子","手锯"]}
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import psycopg2
import logging
import json
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')

WORDS = ["ZAINALI"]
SLUG = "findTool"

#配置
# findTool:
#    host:''
#    port:''
#    topic:''
#    dataHost:''
#    dataPort:''
#    database:''  //数据库的名称
#    user:'postgres'
#    pw:''   //密码

#从命令中获取工具词
def get_tool(text):
	home_dir = os.path.expandvars('$HOME')
	location = home_dir + '/.dingdang/tool.json'
	f = open(location).read()
	fjson = json.loads(f)
	tool = None
	for value in fjson.values():
		if word in text for word in value:
			tool = word
	return tool

def isValid(text):
    tool = get_tool(text)
	return tool!=None

def connectPostgreSQL(database,user,pw,host,port,tool):
	try:
		conn = psycopg2.connect(database=database,user = user,password=pw,host = host,port = port)
	except:
		mic.say("数据库连接失败，请稍后再试")
	cursor = conn.cursor()
	# 这里是数据库查询语句????
	cursor.execute("")
	row = cursor.fetchall()
	room = row[0]
	location = row[1]
	mic.say('%s 在房间 %s' % tool,room, cache=True)
	conn.close()
	return location

def handle(text,mic,profile,wxbot=None):
	logger = logging.getLogger(__name__)
	if (SLUG not in profile)or(not profile[SLUG].has_key('host'))or(not profile[SLUG].has_key('port'))or(not profile[SLUG].has_key('topic'))or(not profile[SLUG].has_key('dataPort'))or(not profile[SLUG].has_key('dataHost'))or(not profile[SLUG].has_key('database'))or(not profile[SLUG].has_key('user'))or(not profile[SLUG].has_key('pw')):
		mic.say("主人，配置有误", cache=True)
		return
	host = profile[SLUG]['host']
	port = profile[SLUG]['port']
	topic = profile[SLUG]['topic']
	dataHost = profile[SLUG]['dataHost']
	dataPort = profile[SLUG]['dataPort']
	database = profile[SLUG]['database']
	user = profile[SLUG]['user']
	pw = profile[SLUG]['pw']
	# 获取命令中的工具
	tool = get_tool(text)
	# 从数据库中查到该工具的位置
	location = connectPostgreSQL(database,user,pw,dataHost,dataPort,tool)
	#消息的格式还需要调试,数字
	msg=location
	try:
        publish.single(topic,msg,qos=1,hostname=host,port=port)
        # publish.single(topic_p,msg,qos = 1,hostname=host,port=port,auth=auth,client_id=client_id)
        mic.say("灯光已提示",cache=True)
    except Exception,e:
        logger.error(e)
        mic.say('抱歉，mqtt存在错误，指令不能发出')
	















