# coding:utf8

from bs4 import BeautifulSoup
import re
import urlparse
import url_manager, html_downloader, html_parser, html_outputer

class HtmlParser(object):

	def __init__(self):
		self.downloader = html_downloader.HtmlDownloader()

	def _get_new_urls(self, page_url, soup):
		new_urls = set()
		# /view/123.htm
		links = soup.find_all('a', href=re.compile(r"/item"))
		for link in links:
			new_url = link['href']
			new_full_url = urlparse.urljoin(page_url, new_url)
			new_urls.add(new_full_url)
		return new_urls

	def _get_new_data(self, page_url, soup):
		res_data = {}
		res_data["url"] = page_url
		title_node = soup.find('dd', class_="lemmaWgt-lemmaTitle-title").find("h1")
		res_data["title"] = title_node.get_text()

		summary_node = soup.find('div', class_="lemma-summary")
		res_data["summary"] = summary_node.get_text()

		return res_data

	
	def parse(self, page_url, html_cont):
		if page_url is None or html_cont is None:
			return
		soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
		new_urls = self._get_new_urls(page_url, soup)
		new_data = self._get_new_data(page_url, soup)
		return new_urls, new_data

	def parse_prov(self, html_content):

		soup = BeautifulSoup(html_content, 'html.parser', from_encoding='utf-8')
		# print soup
		res_data = {}
		res_data['area'] = []
		res_data['prov'] = {}
		res_data['node_id'] = {}
		# res_data['provinces']=[]

		local_nodes = soup.find('div', class_="region").find_all('table')
		for local in local_nodes:
			area = local.find('th').get_text()
			res_data['area'].append(area)
			prov_list = local.find('td').find_all('a')
			res_data['prov'][area] = []
			for prov in prov_list:
				node_name = prov.get_text()
				node_id = filter(str.isdigit, str(prov['onclick']))
				res_data['prov'][area].append(node_name)
				res_data['node_id'][node_name] = node_id

		return res_data

	def parse_town_pages_count(self, city_content):
		city_content['pages_count'] = {}
		count = 1
		for i in city_content['node_id']:
			print '==============='
			print "正在分析 %s" % i.encode('utf-8')
			root_url = "http://c.wanfangdata.com.cn/LocalChronicleRegion.aspx?NodeId=%s" % city_content['node_id'][i]
			# print root_url
			page_content = self.downloader.download(root_url)
			soup = BeautifulSoup(page_content, 'html.parser', from_encoding='utf-8')
			if (soup.find('a', string = '地情概况') != None):
				pages_count = soup.find('span', class_ = 'page_link')
				pages_count = int(filter(str.isdigit, str(pages_count)) or 1)
			else:
				pages_count = 0
				
			city_content['pages_count'][i] = pages_count
			print "总页数：%d" % pages_count
			# if count == 1:
			# 	break
			# count = count + 1
		town_content = city_content
		print town_content
		return town_content

	def parse_every_town_list(self, town_content):
		town_content['all_town_url'] = {}
		for i in town_content['pages_count']:
			town_content['all_town_url'][i] = []
			print i
			count = town_content['pages_count'][i]
			if (count > 0):
				for x in range(1,count+1):
					url = "http://c.wanfangdata.com.cn/LocalChronicleRegion.aspx?NodeId=%s&PageNo=%d" % (town_content['node_id'][i], x)
					# print url
					town_content['all_town_url'][i].append(url)
		print t
		own_content
		return town_content

	def parse_doc_list(self, town_content):
		town_content['doc_list'] = {}
		for i in town_content['all_town_url']:
			count = town_content['pages_count'][i]
			if count > 0:
				print i
				print '============================================='
				town_content['doc_list'][i] = []
				for k in range(1, count+1):
					url = town_content['all_town_url'][i][k-1]
					page_content = self.downloader.download(url)
					soup = BeautifulSoup(page_content, 'html.parser', from_encoding='utf-8')
					info = soup.find('ul', class_ = 'fzrelocal_items').find_all('a', title=re.compile(u'镇'))
					# print info
					for j in range(0, len(info)):
						# print info[j]['title']
						# print info[j]['href']
						doc_obj = { 
							'title': info[j]['title'],
							'href': info[j]['href']
						}
						print doc_obj['title']
						town_content['doc_list'][i].append(doc_obj) 

					# print info['title']
					# print info['href']
					# print k
					# print url
					# if k == 1:
					# 	break
				print '\n'
		print town_content
		return town_content







