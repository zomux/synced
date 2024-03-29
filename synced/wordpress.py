
import json
import re
from xml.dom import minidom

from synced import http
from synced.functions import *


from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import posts
from wordpress_xmlrpc.methods import taxonomies
import xml

def fetch(params):
  require_params(params,["xmlrpc_url","username","password"])
  wp = Client(params["xmlrpc_url"], params["username"], params["password"])
  if not wp:
    return None
  args = {"numberposts":20,"post_status":"publish"}
  
  if "categories" in params:
    args["categories"] = params["categories"]
  
  wpposts = wp.call(posts.GetPosts(args))
  if not wpposts:
    return None
  list_items = []
  for wppost in wpposts:
    list_items.append({"id":wppost.id,"title":wppost.title,
                       "content":wppost.content,"date":wppost.date_modified,
                       "link":wppost.link,"obj":wppost})
  return list_items
  
def enhance(item):
  #require_params(item,["id","server_no"])
  return item

def post(params):
  require_params(params,["xmlrpc_url","username","password","title","content","categories"])

  wp = Client(params["xmlrpc_url"], params["username"], params["password"])
  if not wp:
    return None

  post = WordPressPost()
  post.title = params["title"]
  post.content = params["content"]
  post.post_status = "publish"
  for cate in params["categories"].split(","):
    wpterms = wp.call(taxonomies.GetTerms('category', {"search":cate}))
    for wpterm in wpterms:
      if wpterm.name == cate:
        post.terms.append(wpterm)
  try:
    post.id = wp.call(posts.NewPost(post))
  except xml.parsers.expat.ExpatError:
    pass
  return True

def edit(params):
  require_params(params,["xmlrpc_url","username","password","item","content"])
  item = params["item"]
  if "obj" not in item:
    print "[Wordpress] not found obj in item"
  post = item["obj"]
  if "title" in params:
    post.title = params["title"]
  if "content" in params:
    post.content = params["content"]

  wp = Client(params["xmlrpc_url"], params["username"], params["password"])
  if not wp:
    return None
    
  return wp.call(posts.EditPost(post.id,post))
  


__all__ = ["post","fetch","edit"]

