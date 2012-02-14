'''
Author : Jay Rambhia
email : jayrambhia777@gmail.com
Git : https://github.com/jayrambhia
gist : https://gist.github.com/jayrambhia
=============================================
Name : twitterBox
Repo : TwitterBox
Git : https://github.com/jayrambhia/TwitterBox
version 0.1
'''

import twitter
import pygtk
pygtk.require('2.0')
import gtk
from threading import Thread
import gobject
gtk.gdk.threads_init()

class TwitterBox:
	def __init__(self, api):
		self.thread_flag=False
		self.status_flag=False
		self.api = api
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.set_size_request(1000,700)
		self.window.set_resizable(False)
		self.window.set_title("Twitter Box")
		self.window.set_border_width(4)
		self.window.connect("destroy", self.close_application)
		
		self.vbox = gtk.VBox(False, 2)
		self.window.add(self.vbox)
		self.vbox.show()
		
		self.tweetbox = gtk.HBox(False,2)
		self.vbox.pack_start(self.tweetbox, False, False, 2)
		self.tweetbox.show()
		
		self.tweet_entry = gtk.Entry()
		self.tweet_entry.set_size_request(880,30)
		self.tweet_entry.set_max_length(140)
		self.tweetbox.pack_start(self.tweet_entry, False, False, 3)
		self.tweet_entry.show()
		
		self.button = gtk.Button('Tweet')
		self.button.set_size_request(100,30)
		self.button.connect('clicked', self.tweet)
		self.tweetbox.pack_end(self.button,False,False,2)
		self.button.show()
		
		self.notify_box = gtk.HBox(False,2)
		self.notify_box.set_size_request(1000,30)
		self.vbox.pack_start(self.notify_box, False, False, 2)
		self.notify_box.show()
		
		self.notify_label = gtk.Label('Tweets')
		self.notify_box.add(self.notify_label)
		self.notify_label.show()
		
		self.vbox1 = gtk.EventBox()
		self.vbox1.set_size_request(700,580)
		self.vbox1.connect('leave_notify_event',self.show_tweet)
		self.vbox.pack_start(self.vbox1, False, False, 2)
		self.vbox1.show()
		
		self.sw = gtk.ScrolledWindow()
		self.sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		self.sw.show()
		self.vbox1.add(self.sw)
        
		self.tweetview = gtk.TextView()
		self.tweetbuffer = self.tweetview.get_buffer()
		self.tweetbuffer.set_text('TwitterBox\nby:@jayrambhia')
		self.tweetview.set_editable(False)
		
		self.tweetview.show()
		self.sw.add(self.tweetview)
		
		self.bottombox = gtk.HBox(False,5)
		self.bottombox.set_size_request(1000,30)
		self.vbox.pack_end(self.bottombox, False, False, 3)
		self.bottombox.show()
		
		self.bottomlabel = gtk.Label('@jayrambhia')
		self.bottomlabel.set_size_request(1000,30)
		self.bottombox.add(self.bottomlabel)
		self.bottomlabel.show()
		
		self.window.show()
		
	def tweet(self, widget, data=None):
		text = self.tweet_entry.get_text()
		if text and not self.status_flag:
			gobject.idle_add(self.set_notify_label, 'Tweeting...')
			self.change_status_flag(True)
			self.set_status(text)
		return
				
	def close_application(self, widget):
		gtk.main_quit()

	def show_tweet(self, widget, data=None):
		if not self.thread_flag:
			gobject.idle_add(self.change_thread_flag, True)
			gobject.idle_add(self.set_notify_label, 'Getting Tweets...')
			self.get_tweet_thread()
		
	def get_tweet_thread(self):
		Thread(target=self.get_tweet).start()
		
	def set_status_thread(self, text):
		Thread(target=self.set_status, args=(text,)).start()
			
	def change_thread_flag(self, value):
		self.thread_flag = value
		
	def change_status_flag(self, value):
		self.status_flag = value
	
	def set_status(self, text):
		try:
			status = self.api.PostUpdate(text)
			gobject.idle_add(self.set_notify_label, 'Tweeted')
			self.tweet_entry.set_text('')
		except Error:
			gobject.idle_add(self.set_notify_label, 'Got some error')
		self.change_status_flag(False)
		
	def get_tweet(self):
		timeline=''
		tweet_list=[]
		tweet_str=''
		try:
			timeline = self.api.GetFriendsTimeline()
			if timeline:
				for i in range(len(timeline)):
					screen_name = '@'+timeline[i].user.screen_name
					user_name = timeline[i].user.name
					text = timeline[i].text
					tweet = screen_name+' ('+user_name+') '+':\n\t'+text
					tweet_list.append(tweet)
					tweet_str = tweet_str + tweet + '\n'
					
		except ValueError:
			print 'Got some error'
			gobject.idle_add(self.set_notify_label, 'Got some error')
			
		gobject.idle_add(self.set_tweetview, tweet_str)
		gobject.idle_add(self.change_thread_flag, False)
		gobject.idle_add(self.set_notify_label, 'Tweets')
		
	def set_tweetview(self,text):
		self.tweetbuffer.set_text(text)
		return
		
	def set_notify_label(self, text):
		self.notify_label.set_text(text)	
		return
		
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

	TwitterBox(api)
	gtk.main()
	return 

if __name__ == '__main__':
	main()
