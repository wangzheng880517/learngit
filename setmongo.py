from pymongo import MongoClient
class GetMonogdb():
    def __init__(self,ip,port):
        self.ip=ip
        self.port=port
    def get_dbs(self,db):
        client= MongoClient(self.ip,self.port)
        dbs=client[db]
        return dbs

    def get_collect(self,db,collect):
        dbs=self.get_dbs(db)
        bss=dbs[collect]
        return bss
    def find_all(self,dbss,collects,condition=None):
        data=[]
        collect=self.get_collect(dbss,collects)
        for i in collect.find(condition):
            yield i
            data.append(i)


if __name__ == '__main__':
    moge=GetMonogdb("10.10.5.189",27017)
    db=moge.find_all("CLI-mini_task","Device",{'mip':'10.10.10.16'})
    for i in db:
        print i["mip"]

