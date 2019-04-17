#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2,ConfigParser,time,hashlib,json,os
class LawManService:
    def submitException(self,data={}):
      cf = ConfigParser.ConfigParser()
      current_dir = os.path.dirname(__file__)
      law_man = os.path.abspath(os.path.join(current_dir, "law_man.conf"))
      cf.read(law_man)
      url = '%s%s' % (cf.get("info", "host"),'/ocean/server_rill')
      data['timestamp']=int(time.time())
      data['appId']=cf.get("info", "appId")
      data['sign']=self.getSign(data['timestamp'],cf)
      submitContent = json.dumps(data)
      print(submitContent)
      header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',"Content-Type": "application/json;charset=utf-8","Content-Length":len(submitContent)}
      req = urllib2.Request(url=url,data=submitContent,headers=header_dict)
      res = urllib2.urlopen(req)
      res = res.read()
      print(res)

    def getSign(self,timestamp,cf):
      md5 = hashlib.md5()
      str = '%s%s%s%s' % (cf.get("info", "appId"),cf.get("info", "secret"),cf.get("info", "token"),timestamp)
      md5.update(str)
      return md5.hexdigest()
