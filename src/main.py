#!/usr/bin/python3
import sys, csv, re
import tweepy
import matplotlib.pyplot as plt
from textblob import TextBlob
import exception

## local credentials.py file
import credentials

consumer_key = credentials.consumer['key']
consumer_secret = credentials.consumer['secret']

access_token = credentials.access['token']
access_token_secret = credentials.access['secret']

class Analyze():
	def __init__(self):
		self.tweets = []
		self.tweetText = []

	def sentiment(self, num_search_terms, search_term):
		'''
		Select how many terms query (they are pulled based on recency)
		'''

		if consumer_key == 'ENTER':
			raise Exception('Need to input your own API tokens in the credentials.py file')

		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_token_secret)

		api = tweepy.API(auth)

		self.tweets = tweepy.Cursor(api.search, q=search_term, lang="en").items(num_search_terms)

		# Open/create a file to append data to
		csvFile = open('result.csv', 'a')

		# Use csv writer
		csvWriter = csv.writer(csvFile)

		polarity = 0
		positive = 0
		wpositive = 0
		spositive = 0
		negative = 0
		wnegative = 0
		snegative = 0
		neutral = 0

		for tweet in self.tweets:
			self.tweetText.append(self.cleanTweet(tweet.text).encode('utf-8'))
			# print (tweet.text.translate(non_bmp_map))    #print tweet's text
			analysis = TextBlob(tweet.text)
			# print(analysis.sentiment)  # print tweet's polarity
			polarity += analysis.sentiment.polarity  # adding up polarities to find the average later

			if (analysis.sentiment.polarity == 0):  # adding reaction of how people are reacting to find average later
				neutral += 1
			elif (analysis.sentiment.polarity > 0 and analysis.sentiment.polarity <= 0.3):
				wpositive += 1
			elif (analysis.sentiment.polarity > 0.3 and analysis.sentiment.polarity <= 0.6):
				positive += 1
			elif (analysis.sentiment.polarity > 0.6 and analysis.sentiment.polarity <= 1):
				spositive += 1
			elif (analysis.sentiment.polarity > -0.3 and analysis.sentiment.polarity <= 0):
				wnegative += 1
			elif (analysis.sentiment.polarity > -0.6 and analysis.sentiment.polarity <= -0.3):
				negative += 1
			elif (analysis.sentiment.polarity > -1 and analysis.sentiment.polarity <= -0.6):
				snegative += 1

		csvWriter.writerow(self.tweetText)
		csvFile.close()

		# finding average of how people are reacting
		positive = self.percentage(positive, num_search_terms)
		wpositive = self.percentage(wpositive, num_search_terms)
		spositive = self.percentage(spositive, num_search_terms)
		negative = self.percentage(negative, num_search_terms)
		wnegative = self.percentage(wnegative, num_search_terms)
		snegative = self.percentage(snegative, num_search_terms)
		neutral = self.percentage(neutral, num_search_terms)


		polarity = polarity / num_search_terms


		if (polarity == 0):
			print("Neutral")
		elif (polarity > 0 and polarity <= 0.3):
			print("Weakly Positive")
		elif (polarity > 0.3 and polarity <= 0.6):
			print("Positive")
		elif (polarity > 0.6 and polarity <= 1):
			print("Strongly Positive")
		elif (polarity > -0.3 and polarity <= 0):
			print("Weakly Negative")
		elif (polarity > -0.6 and polarity <= -0.3):
			print("Negative")
		elif (polarity > -1 and polarity <= -0.6):
			print("Strongly Negative")

		print()
		print("Report: ")
		print(str(positive) + "% people thought it was positive")
		print(str(wpositive) + "% people thought it was weakly positive")
		print(str(spositive) + "% people thought it was strongly positive")
		print(str(negative) + "% people thought it was negative")
		print(str(wnegative) + "% people thought it was weakly negative")
		print(str(snegative) + "% people thought it was strongly negative")
		print(str(neutral) + "% people thought it was neutral")

		self.plotPieChart(positive, wpositive, spositive, negative, wnegative, snegative, neutral, search_term,
		                  num_search_terms)

	def cleanTweet(self, tweet):
		# Remove Links, Special Characters etc from tweet
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())

	# function to calculate percentage
	def percentage(self, part, whole):
		temp = 100 * float(part) / float(whole)
		return format(temp, '.2f')

	def plotPieChart(self, positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm,
	                 noOfSearchTerms):
		labels = ['Positive [' + str(positive) + '%]', 'Weakly Positive [' + str(wpositive) + '%]',
		          'Strongly Positive [' + str(spositive) + '%]', 'Neutral [' + str(neutral) + '%]',
		          'Negative [' + str(negative) + '%]', 'Weakly Negative [' + str(wnegative) + '%]',
		          'Strongly Negative [' + str(snegative) + '%]']
		sizes = [positive, wpositive, spositive, neutral, negative, wnegative, snegative]
		colors = ['yellowgreen', 'lightgreen', 'darkgreen', 'gold', 'red', 'lightsalmon', 'darkred']
		patches, texts = plt.pie(sizes, colors=colors, startangle=90)
		plt.legend(patches, labels, loc="best")
		plt.title('How people are reacting on ' + searchTerm + ' by analyzing ' + str(noOfSearchTerms) + ' Tweets.')
		plt.axis('equal')
		plt.tight_layout()
		plt.show()


if __name__ == '__main__':
	analyze = Analyze()
	analyze.sentiment(100,"github")
