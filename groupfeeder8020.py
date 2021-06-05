# -*- coding: utf-8 -*-

import pyodbc
import re
import fuzzywuzzy
from fuzzywuzzy import fuzz
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

driver= '{ODBC Driver 17 for SQL Server}'

with pyodbc.connect('DRIVER='+driver+';Server=(LocalDb)\MSSQLLocalDB;Integrated Security=true;Database=bullyingdb;') as conn:
    with conn.cursor() as cursor:
        cursor.execute("select * from finalcomments30up order by len(comment)") 
        all_comments = cursor.fetchall()

i=1
for current_comment in all_comments:
    if i<3:
        with conn.cursor() as cursor:
            cursor.execute("insert into above30_8020 values (" + str(current_comment.commentid) + ", 'testing')")
        i=i+1
    elif i<10:
        with conn.cursor() as cursor:
            cursor.execute("insert into above30_8020 values (" + str(current_comment.commentid) + ", 'training')")
        i=i+1
    elif i==10:
        with conn.cursor() as cursor:
            cursor.execute("insert into above30_8020 values (" + str(current_comment.commentid) + ", 'training')")
        i=1

