#!/usr/bin/env python3  
#coding: utf-8  
import sys
import os
import json
import re
import uuid
import smtplib 
import urllib2
import platform
from email.mime.text import MIMEText  
from email.mime.image import MIMEImage  
from email.mime.multipart import MIMEMultipart  

def getip():
	try:
		myip = visit("http://www.ip138.com/ip2city.asp")
	except:
		try:
			myip = visit("http://www.whereismyip.com/")
		except:
			myip = "Without the public IP"
	return myip
	
def visit(url):
	opener = urllib2.urlopen(url)
	if url == opener.geturl():
		str = opener.read()
	return re.search('\d+\.\d+\.\d+\.\d+',str).group(0)
  
def get_ip_area(ip):  
	try:  
		apiurl = "http://ip.taobao.com/service/getIpInfo.php?ip=%s" %ip  
		content = urllib2.urlopen(apiurl).read()  
		data = json.loads(content)['data']  
		code = json.loads(content)['code']  
		if code == 0: 
			return (data['country_id'],data['area'],data['city'],data['region'])
		else:  
			print(data)  
	except Exception as ex:  
		print(ex)  
		
def get_mac_address(): 
	mac=uuid.UUID(int = uuid.getnode()).hex[-12:] 
	return ":".join([mac[e:e+2] for e in range(0,11,2)])

def emailsend(ip,mac):
	sender = 'dumingzhe@126.com'  
	receiver = 'dumingzhe@126.com'  
	subject = "chach De' chach" 
	smtpserver = 'smtp.126.com'  
	username = 'dumingzhe@126.com'  
	password = raw_input("Please input Password:")

	# Create message container - the correct MIME type is multipart/alternative.  
	msg = MIMEMultipart('mixed')  
	msg['Subject'] = "chach De' chach"

	(country_id, area, city, region) = get_ip_area(ip)
	
	localinfo = country_id.encode("utf-8") + area.encode("utf-8") + city.encode("utf-8") + region.encode("utf-8")
	  
	html = """
		<html>
			<h1>紧急备份</h1>
			<p>这是来自ELFSONG的紧急备份报告，请立刻保存硬拷贝！</p>
			<p>This is an emergency backup report from ELFSONG, which has legally binding. Please keep the hard copy right now! </p>
			<p>Public IP: %s</p>
			<p>Mac: %s</p>
			<p>platform：%s</p>
			<p>machine: %s</p>
			<p>node: %s</p>
			<p>localinfo:%s</p>
		</html>
		""" %(ip, mac,platform.platform(),platform.machine(),platform.node(),localinfo)  

	part1 = MIMEText(html, 'html','utf-8')  

	msg.attach(part1)  
 
	try:
		smtp = smtplib.SMTP()  
		smtp.connect(smtpserver)  
		smtp.ehlo()  
		smtp.starttls()
		smtp.ehlo()  
		smtp.set_debuglevel(1)  
		smtp.login(username, password)  
		smtp.sendmail(sender, receiver, msg.as_string())  
		smtp.quit() 
		print '发送成功'
	except Exception, e:  
		print str(e)
		
if __name__ == '__main__':  
	ip = getip()
	mac = get_mac_address()
	emailsend(ip,mac)
	 



	
