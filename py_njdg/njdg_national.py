import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import urllib2, pytesseract
from PIL import Image
import csv
from tqdm import tqdm

class njdg:
	def __init__(self):
		self.filename = time.strftime("%Y%m%d")
		self.driver = webdriver.Firefox()
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


		links = ["lastmonth","filedinlastmonth", "lastmonth10yesrdisposal", "objection", "rejection", "unregistered_cases", "over10years_cases", "over5years_cases", "over2years_cases", "lessthan2yrs", "totalpending_cases"]
		links1 = ["seniorcitizen_cases","total_female","listtoday", "undated_cases", "excessive_cases","totaljudges"]		
		
		for link in tqdm(links):
			la = "//a[contains(@href, '../stat_reports/national_detail.php?objection1=" + link + "&type=both')]"
			self.click_link(la)
		for link in tqdm(links1):
			self.driver.switch_to.default_content()					
			self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
			self.driver.switch_to_frame(0)
			time.sleep(.5)
			self.driver.switch_to_frame('data1')
			time.sleep(.5)
			self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
			la = "//a[contains(@href, '../stat_reports/national_detail.php?objection1=" + link + "&type=both')]"
			time.sleep(.5)					
			self.click_link(la)


	def click_link(self,link):
		self.link=link
		time.sleep(1)
		self.driver.find_element_by_xpath(self.link).click()
		time.sleep(1)
		table= "//table[@id='example']"
		self.csv_extract1(table)
		time.sleep(1)
		self.driver.back()

	#getting table data using loop and to store into csv file
	def csv_extract1(self,table):
		table_head=table+"/thead"
		table_body=table+"/tbody"
		table_foot=table+"/tfoot"
		self.driver.switch_to.default_content()		
		self.driver.switch_to_frame(0)
		time.sleep(1)
		self.driver.switch_to_frame('data1')
		time.sleep(1)

		select = Select(self.driver.find_element_by_name('example_length'))
#		print [o.text for o in select.options] # these are string-s
		for o in select.options:
			select.select_by_visible_text('50')

		tablehd = self.driver.find_element_by_xpath(table_head)		
		tableby = self.driver.find_element_by_xpath(table_body)
		tableft = self.driver.find_element_by_xpath(table_foot)			
		with open(self.filename+'-national'+'.csv', 'a') as csvfile:
		    wr = csv.writer(csvfile)
		    for row in tablehd.find_elements_by_css_selector('tr'):
			wr.writerow([d.text for d in row.find_elements_by_css_selector('td')])
		    for row in tableby.find_elements_by_css_selector('tr'):
			wr.writerow([d.text for d in row.find_elements_by_css_selector('td')])
		    for row in tableft.find_elements_by_css_selector('tr'):
			wr.writerow([d.text for d in row.find_elements_by_css_selector('td')])

	
	#getting table data using loop and to store into csv file
	def csv_extract(self,table):
		self.driver.switch_to.default_content()		
		self.driver.switch_to_frame(0)
		time.sleep(1)
		self.driver.switch_to_frame('data1')
		time.sleep(1)
		table = self.driver.find_element_by_xpath(table)		
		with open(self.filename+'-national'+'.csv', 'a') as csvfile:
		    wr = csv.writer(csvfile)
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
	time.sleep(20)
	#h.enter()
	h.explore()
