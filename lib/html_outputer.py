# coding:utf8

class HtmlOutputer(object):

	def __init__(self):
		self.datas = []
	
	def collect_data(self, data):
		if data is None:
			return
		self.datas.append(data)

	def output_html(self, data):
		fout = open('output.html', 'w')

		fout.write("<html>")
		fout.write("<body>")
		fout.write("<table>")

		for data in self.datas:
			fout.write("<tr>")
			fout.write("<td>%s</td>" % data['url'])
			fout.write("<td>%s</td>" % data['title'].encode('utf-8'))
			fout.write("<td>%s</td>" % data['summary'].encode('utf-8'))
			fout.write("</tr>")


		fout.write("</table>")
		fout.write("</body>")
		fout.write("</html>")

		fout.close()

	def output_city_html(self, data):

		# data = {
		# 	'area':[
		# 		'a','b','c','d'
		# 	],
		# 	'prov':{
		# 		'a': ['a1','a2','a3'],
		# 		'b': ['b3','b4'],
		# 		'c': ['c3','c4'],
		# 		'd': ['d3','d4']
		# 	},
		# 	'node_id':{
		# 		'a': '1'
		# 		'b': '2'
		# 	},
		# 	'pages_count': {
		# 		'a': 1,
		# 		'b': 2
		# 	},
		# 	'all_town_url': {
		# 		'a': ['xxx','xxxx','xxxx']
		# 	},
		# 	'doc_list': {
		# 		'a': [
		# 			{title: 'xxxxxxx'},
		# 			{href: 'sdsdsds'}
		# 		]
		# 	},
			# 'dir_list': {
			# 	'doc': [
			# 		{title: 'xxxxx',href: 'ssss'}
			# 	]
			# }

		# }

		fout = open('city.html', 'w')


		fout.write("<html>")
		fout.write("<head>")
		fout.write("<meta http-equiv='content-type' content='text/html;charset=utf-8'>")
		fout.write('<link rel="stylesheet" href="styles.css" type="text/css" />')
		fout.write("</head>")
		fout.write("<body>")
		fout.write("<h1 class='title'>新方志</h1>")
		# fout.write('<hr/>')
		fout.write('<ul class="wtree">')

		for area in data['area']:
			fout.write('<li>')
			fout.write('<span>%s</span>' % area.encode('utf-8'))
			if (data['prov'][area]):
				fout.write('<ul>')
				for prov in data['prov'][area]:
					fout.write('<li>')
					fout.write('<span>%s <div style="display: inline-block; background-color: #FFEB3B;">id: %s</div></span>' % (prov.encode('utf-8'), data['node_id'][prov]))
					if data['pages_count'][prov] > 0:
						fout.write('<ul>')
						print prov
						for doc in range(0, len(data['doc_list'][prov])):
							print '=================='
							fout.write('<li><span>%s</span> [<a target="_blank" href="http://c.g.wanfangdata.com.cn/%s">link</a>]</li>' % (data['doc_list'][prov][doc]['title'].encode('utf-8'), data['doc_list'][prov][doc]['href'].encode('utf-8')))
						fout.write('</ul>')

					fout.write('</li>')
				fout.write('</ul>')

			fout.write('</li>')

		fout.write('</ul>')

		fout.write("</body>")
		fout.write("</html>")


		fout.close()