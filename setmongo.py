from pymongo import MongoClient
class GetMonogdb():

    def __init__(
            self,
            ip,
            port,
            db,
            collect):
        self.ip=ip
        self.port=port
        self.db=db
        self.collect=collect

    def _conn_db(self):
        client= MongoClient(self.ip,self.port)
        return client[self.db]
    def _conn_collect(self):
        dbs=self._conn_db()
        collects=dbs[self.collect]
        return  collects
    def find_all(self,condition=None):
        data=[]
        datas=self._conn_collect().find(condition)
        for i in datas:
            yield i
            data.append(i)
    def insert_all(self,data):
        collect=self._conn_collect()
        collect.insert(data)

    def find_limits(self,limits):
        data=[]
        datas=self._conn_collect().find(limit=limits)
        for row in datas:
            data.append(row)
        return data



if __name__ == '__main__':
    moge=GetMonogdb("10.10.5.189",27017,"CLI-mini_task","Device")
    print moge.find_limits(5)
    #db=moge.find_all("CLI-mini_task","Device",{'mip':'10.10.10.16'})
    # for i in db:
    #     print i["mip"
    # for i in moge.find_all():
    #     print i
