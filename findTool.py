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

WORDS = ["DUBANGXIAN"]
SLUG = "findTool"

def isValid(text):
    # tool = get_tool(text)
    
    return any(word in text for word in [u"杜邦线",u"钳子"])
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
		for word in text:
                    if word in value:
                        tool = word
                        return tool
	return tool



def connectPostgreSQL(database,user,pw,host,port,tool,mic,logger):
	try:
		conn = psycopg2.connect(database=database,user = user,password=pw,host = host,port = port)
	except:
		mic.say("数据库连接失败，请稍后再试")
	cursor = conn.cursor()
	# 这里是数据库查询语句????
	tool = tool.split("，")[0]
	cursor.execute("SELECT roomid,goodlocation FROM goods WHERE goodsname= %s ;",(tool,))
	#logger.error(tool)
	rows = cursor.fetchall()
	#logger.error(rows)
	location='1'
	for i in rows:
            #logger.error(i)
            room = i[0]
            location = i[1]
            responds = u'%s房间：' % room
	    mic.say(responds, cache=True)
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
	tool = text
	logger.error(type(tool))
	# mic.say(type(tool),cache=True)
	# 从数据库中查到该工具的位置
	station = connectPostgreSQL(database,user,pw,dataHost,dataPort,tool,mic,logger)
	logger.error(station)
	#消息的格式还需要调试,数字
	msg=station
	try:
            publish.single(topic,msg,qos=1,hostname=host,port=port)
        # publish.single(topic_p,msg,qos = 1,hostname=host,port=port,auth=auth,client_id=client_id)
            mic.say("灯光已提示",cache=True)
        except Exception,e:
            logger.error(e)
            mic.say('抱歉，mqtt存在错误，指令不能发出')
	















