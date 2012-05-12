# -*- coding: utf-8 -*-
# config
PATH_DOWNLOAD = '/Volumes/DATA/Musics'
# lib
import urllib2,os

req = urllib2.Request('https://www.evernote.com/shard/s26/enweb/notestore/ext')
headers = """
Accept:*/*
Accept-Charset:utf-8;q=0.7,*;q=0.3
Connection:keep-alive
Content-Length:281
Content-Type:text/x-gwt-rpc; charset=UTF-8
Host:www.evernote.com
Origin:https://www.evernote.com
Referer:https://www.evernote.com/pub/zomux/anotemydiary
User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.168 Safari/535.19
X-GWT-Module-Base:https://www.evernote.com/webclient/
X-GWT-Permutation:07A691FEB4974CBE730695941D648E9D
"""
for line in headers.split('\n'):
  if line.count(":") is 0 : continue
  k,v = line.split(":",1)
  req.add_header(k, v)
#req.set_proxy('125.90.196.153:3128','http')
data = "7|0|9|https://www.evernote.com/webclient/|81CBA6C43.DC8EF1165D418D79E66409|com.evernote.web.shared.GWTNoteStoreExtensions|getHtmlNoteContent|java.lang.String/2004016611|java.util.List||1b529e01-8e40-4e39-9194-96842b61697e|java.util.ArrayList/4159755760|1|2|3|4|4|5|5|6|5|7|8|9|0|0|"

furl = urllib2.urlopen(req,data,60)

print furl.read()

  