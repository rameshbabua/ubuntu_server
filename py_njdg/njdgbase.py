import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import urllib2, pytesseract
from PIL import Image
import csv

class njdg:
	def __init__(self):
		self.driver = webdriver.Firefox()
		self.filename = time.strftime("%Y%m%d")
		time.sleep(2)

	#select NJDG Public website
	def navigate(self):
		self.driver.get('http://njdg.ecourts.gov.in/njdg_public/')
		
	#Entering login detials
	def enter(self):
		
		#taking screenshot
		self.take_screenshot()

		#crop image
		image_element = self.driver.find_element_by_id('captcha_image')
		location = image_element.location
		size = image_element.size
		self.crop_image(location,size)

		#capture image text
		text = self.recover_text('myfile.png').strip()
		#print text

		#entering captcha text
		txtbox1 = self.driver.find_element_by_name('captcha')
		txtbox1.send_keys(text)
		time.sleep(1)

		#submit
		self.driver.find_element_by_id('guestlogin').click()
		time.sleep(2)
	
	def explore(self):
		table = "//form[@id='frm']/table[2]"
		self.csv_extract(table)
		time.sleep(1)

	def click_link(self,state,link,flink):
		#state=state
		slink=link		
		self.link=flink
		time.sleep(.5)
		self.driver.find_element_by_xpath(self.link).click()
		time.sleep(1)
		table= "//table[@id='example']"
		self.csv_extract1(table,state,slink)
		#time.sleep(1)
		self.driver.back()

	#getting table data using loop and to store into csv file
	def csv_extract1(self,table,state,slink):
		self.state=state
		self.slink=slink
		table_body=table+"/tbody"
		table_foot=table+"/tfoot"
		self.driver.switch_to.default_content()	
		self.driver.switch_to_frame(0)
		time.sleep(.5)
		self.driver.switch_to_frame('data1')
		time.sleep(1)

		select = Select(self.driver.find_element_by_name('example_length'))
		for o in select.options:
			select.select_by_visible_text('100')

		tableby = self.driver.find_element_by_xpath(table_body)
		tableft = self.driver.find_element_by_xpath(table_foot)		
		with open(self.filename+'-complete'+'.csv', 'a') as csvfile:
		    wr = csv.writer(csvfile)
		    #wr.writerow([state])
		    for row in tableby.find_elements_by_css_selector('tr'):
			wr.writerow([self.filename]+[slink]+[state]+[d.text for d in row.find_elements_by_css_selector('td')])
		    for row in tableft.find_elements_by_css_selector('tr'):
			wr.writerow([self.filename]+[slink]+[state]+[d.text for d in row.find_elements_by_css_selector('td')])	
		    csvfile.close()
	
	#getting table data using loop and to store into csv file
	def csv_extract(self,table,state):
		self.state=state		
		self.driver.switch_to.default_content()		
		self.driver.switch_to_frame(0)
		time.sleep(1)
		self.driver.switch_to_frame('data1')
		time.sleep(1)
		table = self.driver.find_element_by_xpath(table)		
		with open(self.filename+'-complete_test'+'.csv', 'a') as csvfile:
		    wr = csv.writer(csvfile)
		    wr.writerow([state])
		    for row in table.find_elements_by_css_selector('tr'):
		        wr.writerow([d.text for d in row.find_elements_by_css_selector('td')])

	#taking screenshot
	def take_screenshot(self):
		self.driver.save_screenshot('myfile.png')

	#cropping image
	def crop_image(self,location,size):
		image = Image.open('myfile.png')
		x,y = int(location['x']),int(location['y'])
		w,h = int(size['width']), int(size['height'])
		image.crop((x, y, x+w, y+h)).save('myfile.png')

	#retrieving text
	def recover_text(self,filename):
		image = Image.open('myfile.png')
		r,g,b,a = image.split()			#removing the alpha channel
		image = Image.merge('RGB',(r,g,b))
		return pytesseract.image_to_string(image)


if __name__ == '__main__':
	h = njdg()
	h.navigate()
	h.enter()
	h.explore()
