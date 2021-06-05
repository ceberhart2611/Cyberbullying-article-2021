# -*- coding: utf-8 -*-

import pyodbc
import re
import fuzzywuzzy
from fuzzywuzzy import fuzz
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

driver= '{ODBC Driver 17 for SQL Server}'

#remove all chars that are not letters a-z or ç 
def normalize_text(text):
    text = text.casefold()
    text = re.sub('[àáãâä]', 'a', text)
    text = re.sub('[éèêë]', 'e', text)
    text = re.sub('[íìîï]', 'i', text)
    text = re.sub('[óòôõö]', 'a', text)
    text = re.sub('[úùûü]', 'u', text)
    text = re.sub('[\'\"1!¹2@²3#³4$£5%¢6¨¬7&89(0)]`´[{ª]}º~^<>°§', '', text)
    text = re.sub('[*\\|/,.:;?+-_=\n]', ' ', text)
    text = re.sub(' * ', ' ', text)

    return text

#check for exact matches of insults in a text
def insult_exact_match(text, dictionary):
    iemcounter=0

    for word in dictionary:
        if re.search(rf'\b({word})\b', text) != None :
            #print(str(word))
        
            iemcounter = iemcounter + 1

    return iemcounter


with pyodbc.connect('DRIVER='+driver+';Server=(LocalDb)\MSSQLLocalDB;Integrated Security=true;Database=bullyingdb;') as conn:
    with conn.cursor() as cursor:
        cursor.execute("select F.commentid, comment, keyphrases from finalcomments30up F join commentkeyphrases C on F.commentid = C.commentid") 
        all_comments = cursor.fetchall()

generaldictionary = []
cursingdictionary = []
contextdictionary = []
sexlangdictionary = []

#get dictionary
with conn.cursor() as cursor:
        cursor.execute("SELECT distinct(insult) FROM LR_listofinsults where type = 'general'")
        for row in cursor.fetchall():
            text = str(row)
            text = text.replace('(\'', '')
            text = text.replace('\', )', '')
            generaldictionary.append(text)

with conn.cursor() as cursor:
        cursor.execute("SELECT distinct(insult) FROM LR_listofinsults where type = 'cursing'")
        for row in cursor.fetchall():
            text = str(row)
            text = text.replace('(\'', '')
            text = text.replace('\', )', '')
            cursingdictionary.append(text)

with conn.cursor() as cursor:
        cursor.execute("SELECT distinct(insult) FROM LR_listofinsults where type = 'context'")
        for row in cursor.fetchall():
            text = str(row)
            text = text.replace('(\'', '')
            text = text.replace('\', )', '')
            contextdictionary.append(text)

with conn.cursor() as cursor:
        cursor.execute("SELECT distinct(sexword) FROM LR_sexslang")
        for row in cursor.fetchall():
            text = str(row)
            text = text.replace('(\'', '')
            text = text.replace('\', )', '')
            sexlangdictionary.append(text)

#feed the insultmatch table
for current_comment in all_comments:
    converted_comment = normalize_text(current_comment.comment)
    

    doccursing = insult_exact_match(converted_comment, cursingdictionary)

    docgeneral = insult_exact_match(converted_comment, generaldictionary)

    doccontext = insult_exact_match(converted_comment, contextdictionary)
    docsexlang = insult_exact_match(converted_comment, sexlangdictionary)


    norm_kp = normalize_text(str(current_comment.keyphrases))
    kpcursing = insult_exact_match(norm_kp, cursingdictionary)
    kpgeneral = insult_exact_match(norm_kp, generaldictionary)
    kpcontext = insult_exact_match(norm_kp, contextdictionary)
    kpsexlang = insult_exact_match(norm_kp, sexlangdictionary)
    
    with conn.cursor() as cursor:
        cursor.execute("insert into LR_insultmatch values (" + str(current_comment.commentid) +
                        ", " + str(doccursing) +
                         ", " + str(docgeneral) +
                          ", " + str(doccontext) +
                           ", " + str(docsexlang) +
                           ", " + str(kpcursing) +
                         ", " + str(kpgeneral) +
                          ", " + str(kpcontext) +
                           ", " + str(kpsexlang) + ")")






