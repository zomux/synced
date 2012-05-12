import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from synced.functions import *
search_package_at("thirdparty")

import yaml

from synced.worker import Worker


if __name__ == "__main__":
  configs = yaml.load(open("config.yaml").read())
  for i,config in enumerate(configs):
    print "------ TASK %d ------" % (i+1)
    worker = Worker(config["mode"],config["source"],config["target"])
    worker.run()
  print "------ COMPLETED ------"



