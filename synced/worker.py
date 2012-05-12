from functions import *

import inspect
import sys
import re


class Worker:
  # forward_by_title: require fetch:title in source , fetch:title , post in target
  # forward_by_date: require fetch:date in source , fetch:date , post in target
  # sync_by_title_date: require fetch:[title,date] in source , fetch:[date,title] ,post, edit in target
  _modeSync = ["forward_by_title","forward_by_date","sync_by_title_date"]
  source = None
  target = None
  mode = None
  moduleSource = None
  moduleTarget = None
  _mapModeRequiredAction = {
    "forward_by_title":("fetch","fetch,post"),
    "forward_by_date":("fetch","fetch,post"),
    "sync_by_title_date":("fetch","fetch,post,edit")
  }
  def __init__(self,mode,source,target):
    self.mode = mode
    self.source = source
    self.target = target

  def getRequiredParamsFromFunction(self,func):
    code = "".join(inspect.getsourcelines(func)[0])
    matched_params = re.findall("require_params\(.+?\[(.*?)].*?\)",code)
    if not matched_params:
      return []
    return [x.strip('"') for x in matched_params[0].split(",")]

  def checkService(self,params,actions_required):

    service = params["service"]
    try:
      module = getattr(__import__("synced.%s" % service),service)
      if not module: return None
    except Exception as e:
      print "Load service '%s' error." % service
      print e
      return None
    # check if the service provides action we require
    if len(set(actions_required)-set(module.__all__)) > 0:
      print "More Actions require for the '%s' than it provides" % service
      print "Need %s" % ",".list(set(actions_required)-set(module.__all__))
      return None
    ret = module
    # check if we have enough params to run the actions in service
    for action in actions_required:
      func = getattr(module,action)
      params_required = self.getRequiredParamsFromFunction(func)
      params_not_given = set(params_required) - set(params)
      if len(params_not_given):
        print "Error: required parameters for '%s' not found:" % service ,
        print ",".join( params_not_given )
        ret = None

    
    return ret

  def check(self):
    """
    check configuration
    """
    if self.mode not in self._modeSync:
      print "sync mode '%s' not found" % self.mode
      return None
    actions_required_source,actions_required_target = self._mapModeRequiredAction[self.mode]
    actions_required_source = actions_required_source.split(",")
    actions_required_target = actions_required_target.split(",")

    mod_source = self.checkService(self.source,actions_required_source)
    mod_target = self.checkService(self.target,actions_required_target)

    if not mod_source or not mod_target:
      return False
    else:
      self.moduleSource = mod_source
      self.moduleTarget = mod_target
      return True

  def buildTargetParams(self,item):
    """
    use config and item from source to build target params for post/edit
    """
    params = {}
    for key in self.target:
      value = self.target[key]
      for kitem in item:
        kvalue = item[kitem]
        value = value.replace("{%s}" % kitem,kvalue)
      params[key] = value
    return params

  def forward_by_title(self):
    fetch_source = getattr(self.moduleSource,"fetch")
    enhance_source = None
    if "enhance" in self.moduleSource.__all__:
      enhance_source = getattr(self.moduleSource,"enhance")
    fetch_target = getattr(self.moduleTarget,"fetch")
    post_target = getattr(self.moduleTarget,"post")
    items_source = fetch_source(self.source)
    items_target = fetch_target(self.target)
    # to limit items to post , the forward_by_title will run under control
    items_source = items_source[:len(items_target)/2]
    items_source.reverse()
    titles_target = [x["title"] for x in items_target]
    for item in items_source:
      if item["title"] not in titles_target:
        if enhance_source:
          item = enhance_source(item)
        params_target = self.buildTargetParams(item)
        retPost = post_target(params_target)
        print "POST:",item["title"]
        print "RETURN:",retPost
        
    return True

  def run(self):
    """
    run the sync worker
    """
    if not self.check():
      print "------ config error ------"
      return None

    print "RUN %s: %s -> %s" % (self.mode,self.source["service"],self.target["service"])


    func = getattr(self,self.mode)
    if not func:
      print "Error: function '%s' not found" % self.mode
      return False

    return func()
    