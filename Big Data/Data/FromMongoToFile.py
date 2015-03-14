# -*- coding: utf-8 -*-
from pymongo import MongoClient

#Module récupérant les données d'une base MongoDB et les écrivant sous un format CSV dans des fichiers
#Un fichier pour le text des tweets "Text.file"
#Un fichier pour les autres informations (dates, lang...) "Info.file"

#Separateur pour le csv
SEPARATOR = ' '

#Base MongoDb
MONGO_DATABASE_NAME = 'twitter_db3'
MONGO_COLLECTION_NAME = 'twitter_collection3'
#Nom des fichiers
NOM_FICHIER_TEXT = '/home/alexis/Bureau/Text.file'
NOM_FICHIER_INFO = '/home/alexis/Bureau/Info.file'

#Function pour écrire dans un fichier depuis une base MongoDB
def WriteCSVFileFromMongo(collection):
    fichiertext = open(NOM_FICHIER_TEXT, "w")
    fichierInfo = open(NOM_FICHIER_INFO, "w")
    for obj in collection.find({'text':{'$exists' : True}}):
        if obj:
            write_in_text_file = str(obj['text'])+'\n'
            write_in_other_text_file = SEPARATOR+str(sum(obj['nbwords']))+SEPARATOR+str(len(obj['hashtag']))+SEPARATOR+str(obj['horary'])+SEPARATOR+str(obj['day'])+SEPARATOR+str(obj['daynumber'])+SEPARATOR+str(obj['month'])+SEPARATOR+str(obj['year'])+SEPARATOR+str(obj['favorite_count'])+SEPARATOR+str(obj['retweeted'])+SEPARATOR+str(obj['favorited'])+SEPARATOR+str(obj['user_activity'])+'\n'
            #print str(obj['_id'])+SEPARATOR+str(obj['id'])
            fichiertext.write(write_in_text_file)
            fichierInfo.write(write_in_other_text_file)
    fichiertext.close()


#On se connecte à la base MongoDB
client = MongoClient('localhost', 27017)
db = client[MONGO_DATABASE_NAME ]
collection = db[MONGO_COLLECTION_NAME]
#On écrit dans les fichiers
WriteCSVFileFromMongo(collection)
