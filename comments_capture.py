import praw
import requests
import json
import pyodbc
import re

def deEmojify(text):

    noemojitext = re.sub(r'[^\w|\s|\d|\n|\r|\t|ç|\'|\"|1|!|¹|2|@|²|3|#|³|4|$|£|5|%|¢|6|¨|¬|7|&|8|9|\(|0|\)|]|`|´|\[|{|ª|\]|}|º|~|\^|<|>|°|§|à|á|ã|â|ä|é|è|ê|ë|í|ì|î|ï|ó|ò|ô|õ|ö|ú|ù|û|ü|\*|\\|\||\/|,|\.|:|;|\?|\+|-|_|=]', ' ', text)

    #noemojitext = str(noemojitext)
    
    return noemojitext


 
driver= '{ODBC Driver 17 for SQL Server}'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'
}

reddit = praw.Reddit(
    user_agent="Comment Extraction (by u/bolhaassassina)",
    client_id="", #OMMITED
    client_secret="", #OMMITED
)

file = open(r"filteredsubredditsmanual.txt", "r", encoding="utf-8-sig")

for line in file:
    postPermalinkList = []

    subreddit_name = line.replace("\n","")

    subreddit_url = "https://reddit.com/r/" + subreddit_name + "/top.json?t=year&count=25"

    json_data = json.loads(requests.get(subreddit_url, headers=headers).text)

    i=0
    for postlink in json_data["data"]["children"]:
        print(str(postlink["data"]["permalink"]))
        postPermalinkList = postPermalinkList + [str(postlink["data"]["permalink"])]
        i=i+1
        if i==10:
            break
    
    
    for postHead in postPermalinkList:
        post_url = "https://reddit.com" + str(postHead)

        submission = reddit.submission(url=post_url)

        submission.comments.replace_more(limit=None)
        

        for top_level_comment in submission.comments.list():
            
            try:
                author = str(top_level_comment.author.name)
            
                current_comment = temp = deEmojify(str(top_level_comment.body))
                with pyodbc.connect('DRIVER='+driver+';Server=(LocalDb)\MSSQLLocalDB;Integrated Security=true;Database=bullyingdb;') as conn:
                    with conn.cursor() as cursor:
                        cursor.execute("insert into comments_raw_data values ('" + current_comment + "','" + subreddit_name + "', '" + author + "')")  
            
                print(str(top_level_comment.body))
                print(str(temp))
                            
            except:
                continue


            
        

