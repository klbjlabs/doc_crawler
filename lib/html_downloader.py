
import urllib2

class HtmlDownloader(object):
	
	def download(self, url):
		if url is None:
			return None
		# print 'downloader => %s' % url
		response = urllib2.urlopen(url)
		# print response.read()
		if response.getcode() != 200:
			return None
		return response.read()