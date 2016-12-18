import Tweet
import nltk
import re
import os
import codecs
import simplejson as json

annotators = ['michael', 'meizhi', 'pragyan','abiral','karen', 'cameron']
save_dir = "/home/broseph/Dropbox/NYU Shanghai/2015-2016/Term2/Natural Language Processing/Mediated Campaigns/"
file_ids = ('Trump', 'Sanders', 'Clinton', 'Stein', 'Johnson')
target_ids = {'Trump': "Trump", 'Sanders': "Sanders", 'Clinton': "Clinton", 'Stein': "Stein", 'Johnson': "Johnson"}
group_ids = {'Trump': 0, 'Sanders': 1, 'Clinton': 2, 'Stein': 3, 'Johnson': 4}
userMap = {'HillaryClinton' :'Clinton','realDonaldTrump' :'Trump','SenSanders' :'Sanders','DrJillStein' :'Stein', 'GovGaryJohnson' :'Johnson'}

date = '2016-08-12'
userList = ['HillaryClinton','realDonaldTrump','SenSanders','DrJillStein', 'GovGaryJohnson']

pop_count = {'Trump': 0, 'Sanders': 0, 'Clinton': 0, 'Stein': 0, 'Johnson': 0}
max_pop = 0
min_pop = 50000000000000

links = []
sources = {}
nodes = []
for user in userList:
  infile = open(save_dir + date + '/' + '2016-08-12' + user + '.txt', 'r')
  for line in infile:
    tweet = Tweet.Tweet(json.loads(line.strip('\n')))
    sources[tweet.status_id()] = tweet.screen_name()

outfile = open(save_dir + '/Test/graphData.json', 'w')


for name in file_ids:
  infile = open(save_dir + '/Test/' + name + '.txt', 'r')
  rawtweet = ''
  for line in infile:
    rawtweet = rawtweet + line
    if '###\n' in line:
      tweet = rawtweet.strip('###\n')
      splitTweet = tweet.split('___')
      text, attitude, formality, affiliation, popularity, words, tweet_id = splitTweet
      pop_count[userMap[sources[tweet_id]]] += int(popularity)
      if max_pop < int(popularity):
        max_pop = int(popularity)
      if min_pop > int(popularity):
        min_pop = int(popularity)
      rawtweet = ''
      nodes.append({"id":text,"name":text,"text":text,"popularity":popularity,"group":group_ids[userMap[sources[tweet_id]]]})
      links.append({'source':target_ids[name],'target':text, "attitude":attitude})
      links.append({'source':text,"target":target_ids[userMap[sources[tweet_id]]], "attitude":attitude})

for name in file_ids:
  nodes.append({"id":target_ids[name],"name":name,"text":name,"popularity":pop_count[name],"group":group_ids[name]})

print(len(nodes))
print(max_pop)
print(min_pop)

json.dump({"nodes":nodes, "links":links}, outfile)


