# -*- coding: utf-8 -*-

import pyodbc
import re
import fuzzywuzzy
from fuzzywuzzy import fuzz
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

#database connection data
driver= '{ODBC Driver 17 for SQL Server}'

#check for exact matches of insults in a text
def insult_exact_match(text, dictionary):
    iemcounter=0

    for word in dictionary:
        if re.search(rf'\b({word})\b', text) != None :
           iemcounter = iemcounter + 1

    return iemcounter


with pyodbc.connect('DRIVER='+driver+';Server=(LocalDb)\MSSQLLocalDB;Integrated Security=true;Database=bullyingdb;') as conn:
    with conn.cursor() as cursor:
        cursor.execute("select * from finalcomments30up") 
        all_comments = cursor.fetchall()


#feed the insultmatch table
for current_comment in all_comments:

    word1="http:"
    word2="https:"
    word3="www"

    if re.search(rf'({word1})', str(current_comment)) != None :
        linkp=1
    elif re.search(rf'({word2})', str(current_comment)) != None :
        linkp=1
    elif re.search(rf'({word3})', str(current_comment)) != None :
        linkp=1
    else:
        linkp=0

  
    with conn.cursor() as cursor:
        cursor.execute("insert into linkpresence values (" + str(linkp) + "," + str(current_comment.commentid) + ")")



