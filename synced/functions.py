import sys
import os
import pickle

def require_params(params,list_needs=None):
  if list_needs is None:
    list_needs = []
  for key in list_needs:
    if key not in params:
      print key,"not found in params"
      sys.exit()

_cache_path = "cache"

def cache_load(cate,key):
  key = hash(key)
  path = "%s/%s/%s" % (_cache_path ,cate,key)
  if not os.path.exists(path):
    return None
  else:
    return pickle.load(open(path))
  
def cache_save(cate,key,value):
  key = hash(key)
  path = "%s/%s/%s" % (_cache_path,cate,key)
  folder = "%s/%s" % (_cache_path,cate)
  if not os.path.exists(folder):
    os.makedirs(folder)
  pickle.dump(value,open(path,"w"))

def cache_exists(cate,key):
  key = hash(key)
  path = "%s/%s/%s" % (_cache_path,cate,key)
  return os.path.exists(path)

def minidom_node_text(node):
  for node in node.childNodes:
    if node.nodeType in [node.TEXT_NODE, node.COMMENT_NODE,node.CDATA_SECTION_NODE]:
      return node.data
  return 'UNKNOWN'

def search_package_at(path):
  sys.path.append(path)

__all__ = ['require_params','cache_load','cache_save','cache_exists','minidom_node_text','search_package_at']