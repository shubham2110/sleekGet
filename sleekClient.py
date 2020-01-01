#CONFIGURE HERE

clientID='basis@jabb.im'
clientPass='21101991'
serverhost='jabb.im'
logfile='log.txt'



from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout
import threading
import ssl
import time
from flask import Flask
#from quart import Quart
from flask import request
import json
import asyncio
app = Flask(__name__)
import time
from browser3 import browser


	


class EchoBot(ClientXMPP):	
	def __init__(self, jid, password):
		self.conn=ClientXMPP.__init__(self, jid, password, handlefunction=self.message )
		self.add_event_handler("session_start", self.session_start)
		self.add_event_handler("message", self.message)
		self.add_event_handler("ssl_invalid_cert", self.discard)
		self.mids=[]
		print("Setup Done")

	def discard(self, event, cert, direct):
		return
	def session_start(self, event):
		self.send_presence()
		self.get_roster()
	
	

	def message(self, msg):		
		if msg['id'] in self.mids :
			return
		#print(msg['id'], self.mids)
		if(len(self.mids) > 10):
			self.mids.clear()
		self.mids.append(msg['id'])
		body={}
		try:
			user=str(msg.getFrom()).split('/')[0]
		except Exception as e:
			f=open(logfile, 'a')
			f.write(e)
			f.close()

		#if msg['type'] in ('chat', 'normal'):
		#	msg.reply("Thanks for sending\n%(body)s" % msg).send()
		
		body['uid']=user.split('@')[0]
		#print(msg,msg['id'])	
		message1=str(msg['body'])
		body['message']=message1
		
		body['timestamp']=str(time.time())
		a=browser()

		payload=a.dicttoJson(body)
		#print(payload)
		headers={"Content-Type":"application/json"}
		#a.post_request(self.boturl, header=headers, data=message)
		#print("Came here ECHO BOT")
		#res=a.post_request(url=boturl, headers=headers, data=payload)
		res=a.get_request(url="www.google.com/"+message1)
		msg.reply(res).send()
		#print(res)	
	
	def connect_process(self):
		self.connect()
		self.process()
		print("Server Started")

	def connect_processt(self):
		t1=threading.Thread(target=self.connect_process)
		t1.daemon = True
		#print()
		t1.start()
	#def send_message(self, url, uid, message):
		

	
class sendMessageClass(ClientXMPP):
	def __init__(self, jid, password, mto, mbody):
		ClientXMPP.__init__(self, jid, password)
		self.mto=mto
		self.mbody=mbody
		self.add_event_handler("session_start", self.start)
		self.add_event_handler("ssl_invalid_cert", self.discard)
		#f=open('log.txt', 'a')
		#f.write(mbody)
		#f.close()
	
	def discard(self, event, cert, direct):
		return
	def start(self, event):
		self.send_presence()
		self.get_roster()
		self.send_message(mto=self.mto, mbody=self.mbody, mtype='chat')
		self.disconnect(wait=True)
	async def processme(self):
		self.connect()
		self.process()
		#f=open('log.txt', 'a')
		#f.write("Message send")
		#f.close()
		

#boturl="http://127.0.0.1:5001/sendMessage"
#clientID='alexuidian1@jabb.im'
#serverhost="jabb.im"
#clientPass='21101991'
	

if __name__ == "__main__": 
	echobot=EchoBot(clientID, clientPass)
	echobot.boturl=boturl
	echobot.serverhost=serverhost
	echobot.connect_process()
	#app.run(host='0.0.0.0', port='5001', debug=True, use_reloader=False )
	#t1=threading.Thread(target=echobot.connect_process)
	#t1.start()
