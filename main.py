import pandas
from pandas.core.indexes import category
import requests
import os
import bs4 as bs

class Saver:
	@staticmethod
	def write_csv(names, links, categories, filename):
		category_data_frame = pandas.DataFrame({
			'Название': names,
			'Ссылка': links,
			'Категория': categories
		})
		csv_file = category_data_frame.to_csv(index=False)
		with open(filename, "w", encoding='utf-8') as f:
			f.write(csv_file)

class Item:
	def __init__(self, name, link):
		self.name = name
		self.link = link

	def __str__(self):
		return self.name + self.link

class Category:
	def __init__(self, name):
		self.name = name
		self.url = "https://www.kivano.kg/" + name
		self.pages = ["?page=1", "?page=2", "?page=3"]
		self.items = []

	def populate(self):
		for page in self.pages:
			url = self.url+page
			self.fetch_by_page(url)


	def fetch_by_page(self, url):
		source = requests.get(url)
		soup = bs.BeautifulSoup(source.text, 'html.parser')
		items_fetched = soup.find_all('div', attrs={"class":"listbox_title oh"})
		for item in items_fetched:
			tmp_item = Item(item.text, "https://www.kivano.kg"+item.a["href"])
			self.items.append(tmp_item)

	def get_items_string(self):
		texts = ["", "", ""]
		counter = 0
		index = 0
		for el in self.items:
			texts[index] += f'{el.name}'
			counter += 1
			if counter >= 20:
				index += 1
				counter = 0
		return texts
			


	def write(self):
		names = []
		links = []
		categories = []

		for item in self.items:
			names.append(item.name)
			links.append(item.link)
			categories.append(self.name)
		
		Saver.write_csv(names, links, categories, self.name+".csv")

	def view_content(self):
		for el in self.items:
			print(el)

class Tovary:
	def __init__(self):
		categories_list = ["elektronika", "kompyutery", "posuda", "avtotovary"]
		self.cats = []
		for name in categories_list:
			cat = Category(name)
			cat.populate()
			self.cats.append(cat)
		
	def search_for_product(self, name):
		for el in self.cats:
			for item in el.items:
				if str(item.name) == str(name+"\n"):
					text = item.name + " " + item.link + " " + el.name
					return text
		
		return "Подобного товара не найдено."

def main():
	categories_list = ["elektronika", "kompyutery", "posuda", "avtotovary"]

	for name in categories_list:
		categoria = Category(name)
		categoria.populate()
		categoria.write()



def get_categories():
	return "Электроника\nКомпьютеры\nПосуда\nАвтотовары\n"

def return_by_category(name):
	categories_list = ["Электроника", "Компьютеры", "Посуда", "Автотовары"]
	if name in categories_list:
		if name == "Электроника":
			cat = Category("elektronika")
		elif name == "Компьютеры":
			cat = Category("kompyutery")
		elif name == "Посуда":
			cat = Category("posuda")
		elif name == "Автотовары":
			cat = Category("avtotovary")
		cat.populate()
		return cat.get_items_string()
	else:
		return ["Данной категории не существует."]
		

if __name__=='__main__':
	main()