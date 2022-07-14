from pytwitter import Api
from cryptography.x509 import load_pem_x509_certificate
import pprint 
import sqlalchemy as db
import pandas as pd

consumer_keys = "Consumer Keys"
consumer_secret = "Consumer Secrets"
access_token = "Access Token"
access_secret = "Access Secret"


api = Api(consumer_key = consumer_keys, consumer_secret = consumer_secret, access_token = access_token, access_secret = access_secret)

#Getting information about a user
user = input('Enter the username of the person whose information you want to find: ')

response = api.get_user(username = user)
user_id = response.data.id

#Getting user following 
#Create a function that gets a certain number of user's following and returns a dictionary with the information
def following(user_id):
    following = api.get_following(user_id = user_id, max_results = 20)

    following_dict = {}

    list_userid = []
    list_names = []
    list_usernames = []

    for user in following.data:
        list_userid.append(user.id)
        list_names.append(user.name)
        list_usernames.append(user.username)
      #following_dict[user.id] = user.name
      #following_dict[] = user.username

    following_dict['user_id'] = list_userid
    following_dict['names'] = list_names
    following_dict['username'] = list_usernames

    return following_dict

#Getting user followers
#Create a function that takes in a user id, creates a dictionary with the user's followers 
def followers(user_id):
    followers = api.get_followers(user_id = user_id)

    followers_dict = {}

    userid = []
    names = []
    usernames = []

    for user in followers.data:
        userid.append(user.id)
        names.append(user.name)
        usernames.append(user.username)

    followers_dict['user_id'] = user_id
    followers_dict['names'] = names
    followers_dict['username'] = usernames

    return followers_dict

#Create a function that creates a dictionary of a user's mentions
def mentions(user_id):
    mentions = api.get_mentions(user_id= user_id)

    mentions_dict = {}

    id = []
    tweets = []

    for mention in mentions.data:
        id.append(mention.id)
        tweets.append(mention.text)

    mentions_dict['id'] = id
    mentions_dict['text'] = tweets

    return mentions_dict

#Reverse chronological home timeline
#Create a function that enables you to retrieve user Tweet timeline endpoint provides access to Tweets published by a specific Twitter account.
def timeline(user_id):
    timeline = api.get_timelines(user_id= user_id)

    timeline_dict = {}

    id = []
    tweets = []

    for line in timeline.data:
        id.append(line.id)
        tweets.append(line.text)

    timeline_dict['id'] = id
    timeline_dict['text'] = tweets

    return timeline_dict

#creating the database
engine = db.create_engine('sqlite:///Twitter.db')

#creating the dataframes
Following_data = pd.DataFrame.from_dict(following(user_id))
Followers_data = pd.DataFrame.from_dict(followers(user_id))
Mentions_data = pd.DataFrame.from_dict(mentions(user_id))
HomeTimeline_data = pd.DataFrame.from_dict(timeline(user_id))

#inserting the following dataframe as a table
Following_data.to_sql('Following', con=engine, if_exists='replace', index=False)
query_result = engine.execute("SELECT * FROM Following;").fetchall()
df = pd.DataFrame(query_result)
df.columns = ['ID', 'NAME', 'USERNAME']

#inserting the followers dataframe as a table
Followers_data.to_sql('Followers', con=engine, if_exists='replace', index=False)
result = engine.execute("SELECT * FROM Followers;").fetchall()
fw = pd.DataFrame(result)
fw.columns = ['ID', 'NAME', 'USERNAME']

#inserting the mentions dataframe as a table
Mentions_data.to_sql('Mentions', con=engine, if_exists='replace', index=False)
r = engine.execute("SELECT * FROM Mentions;").fetchall()
m = pd.DataFrame(r)
m.columns = ['ID', 'TEXT']

#inserting the timeline dataframe as a table
HomeTimeline_data.to_sql('HomeTimeline', con=engine, if_exists='replace', index=False)
r = engine.execute("SELECT * FROM HomeTimeline;").fetchall()
t = pd.DataFrame(r)
t.columns = ['ID', 'TEXT']
#print(t)

#print(df)
#print(fw)
#print(m)

def main():
  print("What information would you like to retrieve for this user? ")
  prompt = input("Enter 1 for following, 2 for followers, 3 for mentions, 4 for timeline: ")

  if prompt == '1':
    print(df)
  elif prompt == '2':
    print(fw)
  elif prompt == '3':
    print(m)
  elif prompt == '4':
    print(t)
  else:
    print("Invalid input \n ")

main()
