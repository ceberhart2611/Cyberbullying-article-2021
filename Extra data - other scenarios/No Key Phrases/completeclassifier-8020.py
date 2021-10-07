# -*- coding: utf-8 -*-

from itertools import count
import pyodbc
from sklearn.naive_bayes import GaussianNB
from imblearn.over_sampling import SMOTE 
from sklearn import svm

#database connection data
driver= '{ODBC Driver 17 for SQL Server}'

model_feature_list = []
model_labels = []

with pyodbc.connect('DRIVER='+driver+';Server=(LocalDb)\MSSQLLocalDB;Integrated Security=true;Database=bullyingdb;') as conn:
    with conn.cursor() as cursor:
        cursor.execute("select distinct(A.commentid), doc_positive_confidence, doc_neutral_confidence, doc_negative_confidence, linkpresence, doccursing, docgeneral, doccontext, docsexlang, manual_judgement from LR_allfeatures A join manualjudgement M on A.commentid = M.commentid join above30_8020 N on A.commentid = N.commentid where recordtype = 'training'")
        model_records = cursor.fetchall()

#false = 0 ; true = 1

for record in model_records:
    feature_tup = (float(record.doc_positive_confidence), float(record.doc_neutral_confidence), float(record.doc_negative_confidence), int(record.doccursing), int(record.docgeneral), int(record.doccontext), int(record.linkpresence),  int(record.docsexlang))
    if record.manual_judgement == 'T' or record.manual_judgement == 't':
        label = 1
    else:
        label = 0
    
    model_feature_list.append(feature_tup)
    model_labels.append(label)

oversample = SMOTE()
model_feature_list , model_labels = oversample.fit_resample(model_feature_list, model_labels)

print ("TOTAL =" + str(len(model_labels)))
print ("TOTAL TRUE =" + str(model_labels.count(1)))
print ("TOTAL FALSE =" + str(model_labels.count(0)))




model = svm.SVC(kernel='linear')

model.fit(model_feature_list, model_labels)

with conn.cursor() as cursor:
        cursor.execute("select distinct(A.commentid), doc_positive_confidence, doc_neutral_confidence, doc_negative_confidence, linkpresence, doccursing, docgeneral, doccontext, docsexlang, manual_judgement from LR_allfeatures A join manualjudgement M on A.commentid = M.commentid join above30_8020 N on A.commentid = N.commentid where recordtype = 'testing'")
        test_records = cursor.fetchall()
        
for trecord in test_records:
    rtup = (float(trecord.doc_positive_confidence), float(trecord.doc_neutral_confidence), float(trecord.doc_negative_confidence), int(trecord.doccursing), int(trecord.docgeneral), int(trecord.doccontext), int(trecord.linkpresence), int(trecord.docsexlang))
    
    prediction = model.predict([rtup])

    if prediction[0] == 0:
        jud = 'F'
    elif prediction[0] == 1:
        jud = 'T'
    else:
        jud = 'error'

    with conn.cursor() as cursor:
        cursor.execute("insert into resNKP_8020 values (" + str(trecord.commentid) + ", NULL, '" + str(jud) + "')")

model = GaussianNB()

model.fit(model_feature_list, model_labels)

with conn.cursor() as cursor:
        cursor.execute("select distinct(A.commentid), doc_positive_confidence, doc_neutral_confidence, doc_negative_confidence, linkpresence, doccursing, docgeneral, doccontext, docsexlang, manual_judgement from LR_allfeatures A join manualjudgement M on A.commentid = M.commentid join above30_8020 N on A.commentid = N.commentid where recordtype = 'testing'")
        test_records = cursor.fetchall()
        
for trecord in test_records:
    rtup = (float(trecord.doc_positive_confidence), float(trecord.doc_neutral_confidence), float(trecord.doc_negative_confidence), int(trecord.doccursing), int(trecord.docgeneral), int(trecord.doccontext), int(trecord.linkpresence), int(trecord.docsexlang))
    
    prediction = model.predict([rtup])

    if prediction[0] == 0:
        jud = 'F'
    elif prediction[0] == 1:
        jud = 'T'
    else:
        jud = 'error'

    with conn.cursor() as cursor:
        cursor.execute("update resNKP_8020 set NBjudg = '" + str(jud) + "' where commentid = " + str(trecord.commentid) )
