#! /usr/bin/python
# -*- coding:utf8 -*-
import urllib2
import json
import hashlib
import time
import GeoIP
import MySQLdb

CMSAPPID  = "104"
CMSSLOTID = "4011"
CMSPUBLISHID = "51"
conn = MySQLdb.connect(host="localhost",user="root",passwd="1234",db="liebao",charset="utf8")
cursor = conn.cursor()
geoip = GeoIP.open("GeoIP.dat", GeoIP.GEOIP_STANDARD)
timestrimp = str(int(time.time()))
md5str = "%s%s%s"%(CMSPUBLISHID,"",timestrimp)
sign = hashlib.new("md5",md5str).hexdigest()
count = 0
args = []
country = []
filepath = '/home/jay/PycharmProjects/liebao_ad/ip.txt'
with open(filepath,'r') as f:
    for ip in f:
        ip = ip.strip()
        url = "http://rtb.adkmob.com/b/?version=1.0&publisherid=56&app_id=1101&slotid=1101100&timestamp="+timestrimp+"&platform=Android&osv=4.2&resolution=1280*720&dip=2.0&gaid=cfb69082-8db6-4abf-8f89-c48a982ed801&aid=f77568a4bbe6517e&client_ip="+ip+"&client_ua=Dalvik/2.1.0%20%28Linux%3B%20U%3B%20Android%205.0%3B%20Micromax%20A106%20Build/LRX21M%29&adn=1000&model=Micromax+A106&brand=Micromax&format=json&gender=M"
        req = urllib2.Request(url)
        req.add_header("X-CM-SIGN",sign)
        req.add_header("User-Agent", "Mozilla/5.020%(Linux;20%U;20%Android20%4.1.1;20%en­us;20%MI20%220%Build/JRO03L)20%AppleWebKit/534.3020%(KHTML,20%like20%Gecko)Version/4.020%Mobile")
        urlfile = urllib2.urlopen(req)
        html = urlfile.read()
        values = json.loads(html)
        ads = values['ads']
        country_code = geoip.country_code_by_addr(ip)
        if ads and country_code not in country:
            count_rate = 0
            country.append(country_code)
            for ad in ads:
                try:
                    count_rate = count_rate + 1
                    pkg = ad['pkg']
                    code = country_code+'(%d)'% count_rate
                    link = "https://play.google.com/store/apps/details?id="+pkg
                    args.append((pkg, code, link))
                    count = count + 1
                    print count, ip, pkg, code, link
                except Exception, e:
                    print e
print len(country)
sql = "delete from ad"
cursor.execute(sql)
sql = "insert into ad(pkg,code,link) values(%s,%s,%s)"
cursor.executemany(sql, args)
cursor.close()
conn.commit()
conn.close()

