
import json
import re
from xml.dom import minidom

from synced import http
from synced.functions import *

def fetch(params):
  # get rss url
  require_params(params,["shared_url"])
  if cache_exists("evernote",params["shared_url"]):
    rss_url,server_no = cache_load("evernote",params["shared_url"])
  else:
    response = http.get(params["shared_url"])
    if not response: return None

    matched = re.findall(r"href\=\"(.+\/(s\d+)\/.+rss\.jsp.+)\"",response)
    if len(matched) is 0:
      return None
    else:
      rss_url,server_no = matched[0]
      cache_save("evernote",params["shared_url"],matched[0])
  # get list
  response = http.get(rss_url)
  if not response: return None

  list_items = []

  xdoc = minidom.parseString(response)
  items = xdoc.getElementsByTagName("item")
  for item in items:
    title = minidom_node_text(item.getElementsByTagName("title")[0])
    link = minidom_node_text(item.getElementsByTagName("link")[0])
    description = minidom_node_text(item.getElementsByTagName("description")[0])
    pubDate = minidom_node_text(item.getElementsByTagName("pubDate")[0])
    guid = minidom_node_text(item.getElementsByTagName("guid")[0])
    id = guid.split("#n=")[1]
    list_items.append( {"id":id,"title":title,"link":link,"description":description,"date":pubDate,"server_no":server_no} )
  return list_items

def enhance(item):
  require_params(item,["id","server_no"])
  template_url = 'https://www.evernote.com/shard/%s/enweb/notestore/ext' % item["server_no"]
  template_headers = """
Accept:*/*
Accept-Charset:utf-8;q=0.7,*;q=0.3
Connection:keep-alive
Content-Length:281
Content-Type:text/x-gwt-rpc; charset=UTF-8
Host:www.evernote.com
Origin:https://www.evernote.com
User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.168 Safari/535.19
X-GWT-Module-Base:https://www.evernote.com/webclient/
X-GWT-Permutation:07A691FEB4974CBE730695941D648E9D
  """
  template_data = "7|0|9|https://www.evernote.com/webclient/|81CBA6C437DC8EF1165D418D79E66409|com.evernote.web.shared.GWTNoteStoreExtensions|getHtmlNoteContent|java.lang.String/2004016611|java.util.List||[id]|java.util.ArrayList/4159755760|1|2|3|4|4|5|5|6|5|7|8|9|0|0|"
  template_data = template_data.replace('[id]',item['id'])
  response = http.post(template_url,template_headers,template_data)
  if not response.startswith("//OK"):
    print "[Evernote]","Fetch Item Failed"
    print response
    return None
  response = response.replace("//OK","").strip().replace("\\x","\\u00")
  response = json.loads(response,encoding="utf-8")

  content = response[1][0]

  item['content'] = content

  return item



__all__ = ['fetch','enhance']