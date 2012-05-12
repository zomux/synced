# -*- coding: utf-8 -*-

import urllib2,os

def post(url,head="",data=""):
  req = urllib2.Request(url)
  for line in head.split('\n'):
    if line.count(":") is 0 : continue
    k,v = line.split(":",1)
    req.add_header(k, v)

  furl = urllib2.urlopen(req,data,60)
  if not furl: return None

  return furl.read()

def get(url,head=""):
  req = urllib2.Request(url)
  for line in head.split('\n'):
    if line.count(":") is 0 : continue
    k,v = line.split(":",1)
    req.add_header(k, v)

  furl = urllib2.urlopen(req,None,60)
  if not furl: return None

  return furl.read()
  
__all__ = ['post','get']