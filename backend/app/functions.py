 #!/usr/bin/python3


#################################################################################################################################################
#                                                    CLASSES CONTAINING ALL THE APP FUNCTIONS                                                                                                    #
#################################################################################################################################################


class DB:

    def __init__(self,Config):

        from math import floor
        from os import getcwd
        from os.path import join
        from json import loads, dumps, dump
        from datetime import timedelta, datetime, timezone 
        from pymongo import MongoClient , errors, ReturnDocument
        from urllib import parse
        from urllib.request import  urlopen 
        from bson.objectid import ObjectId  
       
      
        self.Config                         = Config
        self.getcwd                         = getcwd
        self.join                           = join 
        self.floor                      	= floor 
        self.loads                      	= loads
        self.dumps                      	= dumps
        self.dump                       	= dump  
        self.datetime                       = datetime
        self.ObjectId                       = ObjectId 
        self.server			                = Config.DB_SERVER
        self.port			                = Config.DB_PORT
        self.username                   	= parse.quote_plus(Config.DB_USERNAME)
        self.password                   	= parse.quote_plus(Config.DB_PASSWORD)
        self.remoteMongo                	= MongoClient
        self.ReturnDocument                 = ReturnDocument
        self.PyMongoError               	= errors.PyMongoError
        self.BulkWriteError             	= errors.BulkWriteError  
        self.tls                            = False # MUST SET TO TRUE IN PRODUCTION


    def __del__(self):
            # Delete class instance to free resources
            pass
 


    ####################
    # PROJECT FUNCTIONS  #
    ####################
    
    def addUpdate(self,data):
        '''ADD A NEW STORAGE LOCATION TO COLLECTION'''
        try:
            remotedb 	= self.remoteMongo('mongodb://%s:%s@%s:%s' % (self.username, self.password,self.server,self.port), tls=self.tls)
            result      = remotedb.ELET2415.station.insert_one(data)
        except Exception as e:
            msg = str(e)
            if "duplicate" not in msg:
                print("addUpdate error ",msg)
            return False
        else:                  
            return True
        
    def range(self,start,end):
        '''RETURNS A LIST OF OBJECTS. THAT FALLS WITHIN THE START AND END DATE RANGE'''
        try:
            remotedb 	= self.remoteMongo('mongodb://%s:%s@%s:%s' % (self.username, self.password,self.server,self.port), tls=self.tls)
            result      = list(remotedb.ELET2415.station.find({"timestamp":{"$gte":int(start),"$lte":int(end)}}, {"_id":0}).sort("timestamp",1))

        except Exception as e:
            msg = str(e)
            print("range error ",msg)            
        else:                  
            return result 

    def humidityMMAR(self,start, end):
        try:
            remotedb 	= self.remoteMongo('mongodb://%s:%s@%s:%s' % (self.username, self.password,self.server,self.port), tls=self.tls)
            result      = list(remotedb.ELET2415.station.aggregate([{'$match': {'timestamp': {'$gte': int(start), '$lte': int(end)}}}, {'$group': {'_id':0, 'humidity': {'$push': '$$ROOT.humidity'}}}, {'$project': {'max': {'$max': '$humidity'}, 'min': {'$min': '$humidity'}, 'avg': {'$avg': '$humidity'}, 'range': {'$subtract': [{'$max': '$humidity'}, {'$min': '$humidity'}]}}}]))

        except Exception as e:
            msg = str(e)
            print("humidityMMAR error ",msg)            
        else:                  
            return result
        
    def temperatureMMAR(self,start, end):
        try:
            remotedb 	= self.remoteMongo('mongodb://%s:%s@%s:%s' % (self.username, self.password,self.server,self.port), tls=self.tls)
            result      = list(remotedb.ELET2415.station.aggregate( [{ '$match': { 'timestamp': { '$gte': int(start), '$lte': int(end) } } }, { '$group': { '_id': 0, 'temperature': { '$push': '$$ROOT.temperature' } } }, { '$project': { 'max': { '$max': '$temperature' }, 'min': { '$min': '$temperature' }, 'avg': { '$avg': '$temperature' }, 'range': { '$subtract': [ { '$max': '$temperature' }, { '$min': '$temperature' } ] } } } ]))

        except Exception as e:
            msg = str(e)
            print("temperatureMMAR error ",msg)            
        else:                  
            return result
        
    def heatIndexMMAR(self,start, end):
        try:
            remotedb 	= self.remoteMongo('mongodb://%s:%s@%s:%s' % (self.username, self.password,self.server,self.port), tls=self.tls)
            result      = list(remotedb.ELET2415.station.aggregate( [{ '$match': { 'timestamp': { '$gte': int(start), '$lte': int(end) } } }, { '$group': { '_id': 0, 'heatindex': { '$push': '$$ROOT.heatindex' } } }, { '$project': { 'max': { '$max': '$heatindex' }, 'min': { '$min': '$heatindex' }, 'avg': { '$avg': '$heatindex' }, 'range': { '$subtract': [ { '$max': '$heatindex' }, { '$min': '$heatindex' } ] } } } ]))

        except Exception as e:
            msg = str(e)
            print("heatIndexMMAR error ",msg)            
        else:                  
            return result
    
    def pressureMMAR(self,start, end):
        try:
            remotedb 	= self.remoteMongo('mongodb://%s:%s@%s:%s' % (self.username, self.password,self.server,self.port), tls=self.tls)
            result      = list(remotedb.ELET2415.station.aggregate( [{ '$match': { 'timestamp': { '$gte': int(start), '$lte': int(end) } } }, { '$group': { '_id': 0, 'pressure': { '$push': '$$ROOT.pressure' } } }, { '$project': { 'max': { '$max': '$pressure' }, 'min': { '$min': '$pressure' }, 'avg': { '$avg': '$pressure' }, 'range': { '$subtract': [ { '$max': '$pressure' }, { '$min': '$pressure' } ] } } } ]))

        except Exception as e:
            msg = str(e)
            print("pressureMMAR error ",msg)            
        else:                  
            return result
        
    def altitudeMMAR(self,start, end):
        try:
            remotedb 	= self.remoteMongo('mongodb://%s:%s@%s:%s' % (self.username, self.password,self.server,self.port), tls=self.tls)
            result      = list(remotedb.ELET2415.station.aggregate( [{ '$match': { 'timestamp': { '$gte': int(start), '$lte': int(end) } } }, { '$group': { '_id': 0, 'altitude': { '$push': '$$ROOT.altitude' } } }, { '$project': { 'max': { '$max': '$altitude' }, 'min': { '$min': '$altitude' }, 'avg': { '$avg': '$altitude' }, 'range': { '$subtract': [ { '$max': '$altitude' }, { '$min': '$altitude' } ] } } } ]))

        except Exception as e:
            msg = str(e)
            print("altitudeMMAR error ",msg)            
        else:                  
            return result
        
    def moistureMMAR(self,start, end):
        try:
            remotedb 	= self.remoteMongo('mongodb://%s:%s@%s:%s' % (self.username, self.password,self.server,self.port), tls=self.tls)
            result      = list(remotedb.ELET2415.station.aggregate( [{ '$match': { 'timestamp': { '$gte': int(start), '$lte': int(end) } } }, { '$group': { '_id': 0, 'moisture': { '$push': '$$ROOT.moisture' } } }, { '$project': { 'max': { '$max': '$moisture' }, 'min': { '$min': '$moisture' }, 'avg': { '$avg': '$moisture' }, 'range': { '$subtract': [ { '$max': '$moisture' }, { '$min': '$moisture' } ] } } } ]))

        except Exception as e:
            msg = str(e)
            print("moistureMMAR error ",msg)            
        else:                  
            return result
        

def main():
    from config import Config
    from time import time, ctime, sleep
    from math import floor
    from datetime import datetime, timedelta
    one = DB(Config)
 
 
    start = time() 
    end = time()
    print(f"completed in: {end - start} seconds")
    
if __name__ == '__main__':
    main()


    
