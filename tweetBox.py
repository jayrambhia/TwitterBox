'''
Author : Jay Rambhia
email : jayrambhia777@gmail.com
Git : https://github.com/jayrambhia
gist : https://gist.github.com/jayrambhia
=============================================
Name : tweetBox
Repo : TwitterBox
Git : https://github.com/jayrambhia/TwitterBox
version 0.1
'''
import twitter
import pygtk
pygtk.require('2.0')
import gtk

class tweetBox:
	def __init__(self, api):
		self.api = api
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.set_size_request(800,30)
		self.window.connect("destroy", self.close_application)
		self.window.set_title("tweetBox")
		
		self.box = gtk.HBox(False,2)
		self.window.add(self.box)
		self.box.show()
		
		self.tweet_entry = gtk.Entry()
		self.tweet_entry.set_size_request(680,30)
		self.tweet_entry.set_max_length(140)
		self.box.pack_start(self.tweet_entry, False, False, 3)
		self.tweet_entry.show()
		
		self.button = gtk.Button('Tweet')
		self.button.set_size_request(100,30)
		self.button.connect('clicked', self.tweet)
		self.box.pack_end(self.button,False,False,2)
		self.button.show()
		
		self.window.show()
		
	def tweet(self, widget, data=None):
		text = self.tweet_entry.get_text()
		if text:
			status = self.api.PostUpdate(text)
			if status:
				self.tweet_entry.set_text('')
		return
		
	def close_application(self, widget):
		gtk.main_quit()
		
def main():
	'''
	Your consumer key, consumer secret, access token key, access token secret go here
	'''
#	api = twitter.Api(consumer_key="", consumer_secret="",access_token_key="", access_token_secret="",proxy ={'http':'http://username:password@proxy:port',
#	'https' : 'https://username:password@proxy:port' })
	'''
	If proxy, uncomment above two lines and add appropriate values. And comment the following line
	'''
	api = twitter.Api(consumer_key="", consumer_secret="",access_token_key="", access_token_secret="")
	tweetBox(api)
	gtk.main()
	
if __name__ == '__main__':
	main()
		
	
