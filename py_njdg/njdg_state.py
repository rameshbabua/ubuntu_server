import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from njdgbase import njdg
import collections
from tqdm import tqdm

class njdg_state (njdg):
		
	def states(self):
		#states = { }	
		states = {'All':'National', 'Andhra Pradesh':2, 'Assam':6, 'Bihar':8, 'Chandigarh':27, 'Chhattisgarh':18,'DNH at Silvasa':32,'Delhi':26, 'Goa':30, 'Gujarat':17, 'Haryana':14, 'Himachal Pradesh':5, 'Jammu and Kashmir':12, 'Jharkhand':7, 'Karnataka':3, 'Kerala':4, 'Madhya Pradesh':23, 'Maharashtra':1,}
		#states = {'Goa':30, 'Maharashtra':1} 
		#backup - states = {'All':'National', 'Andaman and Nicobar':28, 'Andhra Pradesh':2, 'Assam':6, 'Bihar':8, 'Chandigarh':27, 'Chhattisgarh':18, 'Delhi':26, 'Diu and Daman':31, 'DNH at Silvasa':32, 'Goa':30, 'Gujarat':17, 'Haryana':14, 'Himachal Pradesh':5, 'Jammu and Kashmir':12, 'Jharkhand':7, 'Karnataka':3, 'Kerala':4, 'Madhya Pradesh':23, 'Maharashtra':1, 'Manipur':25, 'Meghalaya':21, 'Orissa':11, 'Punjab':22, 'Rajasthan':9, 'Tamil Nadu':10, 'Telangana':29, 'Tripura':20, 'Uttar Pradesh':13, 'Uttarakhand':15, 'West Bengal':16}
		
		od = collections.OrderedDict(sorted(states.items()))
		#links=[]
		links = ["lastmonth","filedinlastmonth", "lastmonth10yesrdisposal", "over10years_cases", "over5years_cases", "over2years_cases","lessthan2yrs", "totalpending_cases" ]  
		links1 =["seniorcitizen_cases", "total_female", "listtoday", "undated_cases","excessive_cases","totaljudges"]
		
		select = Select(self.driver.find_element_by_name('states_code'))

		for state, state_code in od.items():
			select.select_by_visible_text(state)
			self.driver.find_element_by_name('go').click()
			time.sleep(.5)

			if (state == 'All'):
				statename = 'INDIA'
				print state_code +" "+"Started"
				self.driver.switch_to_frame(0)
				time.sleep(.5)
				self.driver.switch_to_frame('data1')
				time.sleep(.5)
				#table = "//form[@id='frm']/table[2]"
				#self.csv_extract(table)
				for link in tqdm(links):
					la = "//a[contains(@href, '../stat_reports/national_detail.php?objection1=" + link + "&type=both')]"
					time.sleep(.5)
					self.click_link(statename,link,la)
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
					self.click_link(statename,link,la)
			else:
				print state +" "+"Started"				
				self.driver.execute_script("window.scrollTo(0,0)")
				self.driver.switch_to_frame(0)
				time.sleep(.5)
				self.driver.switch_to_frame('data1')
				time.sleep(.5)
				#table = "//form[@id='frm']/table[2]"
				#self.csv_extract(table)
				#time.sleep(.5)					
			
				for link in tqdm(links):
					la = "//a[contains(@href, '../stat_reports/state_detail.php?state_code=%d&objection1=%s&type=both')]" %(state_code,link)
					time.sleep(.5)					
					self.click_link(state,link,la)
				for link in tqdm(links1):
					self.driver.switch_to.default_content()					
					self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
					self.driver.switch_to_frame(0)
					time.sleep(.5)
					self.driver.switch_to_frame('data1')
					time.sleep(.5)
					self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
					time.sleep(.5)
					la = "//a[contains(@href, '../stat_reports/state_detail.php?state_code=%d&objection1=%s&type=both')]" %(state_code,link)
					time.sleep(1)					
					self.click_link(state,link,la)
			self.driver.switch_to.default_content()

	def states1(self):
		states = {'Chandigarh':27 }
		#states = {'Andaman and Nicobar':28,'Chandigarh':27,'Diu and Daman':31, 'Mizoram':19,'Sikkim':24} 

		od = collections.OrderedDict(sorted(states.items()))

		links = ["lastmonth","filedinlastmonth", "over10years_cases", "over5years_cases", "over2years_cases", "lessthan2yrs","totalpending_cases"]
		links1 = ["seniorcitizen_cases","total_female","listtoday", "undated_cases", "excessive_cases","totaljudges"]		


		select = Select(self.driver.find_element_by_name('states_code'))

		for state, state_code in od.items():
			select.select_by_visible_text(state)
			self.driver.find_element_by_name('go').click()
			time.sleep(.5)

			self.driver.execute_script("window.scrollTo(0,0)")
			self.driver.switch_to_frame(0)
			time.sleep(.5)
			self.driver.switch_to_frame('data1')
			time.sleep(.5)
			#table = "//form[@id='frm']/table[2]"
			#self.csv_extract(table)
			#time.sleep(.5)					
			print state +" "+"Started"	
			for link in tqdm(links):			
				la = "//a[contains(@href, '../stat_reports/state_detail.php?state_code=%d&objection1=%s&type=both')]" %(state_code,link)
				time.sleep(.5)					
				self.click_link(state,link,la)
			for link in tqdm(links1):
				self.driver.switch_to.default_content()					
				self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
				self.driver.switch_to_frame(0)
				time.sleep(.5)
				self.driver.switch_to_frame('data1')
				time.sleep(.5)
				self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
				la = "//a[contains(@href, '../stat_reports/state_detail.php?state_code=%d&objection1=%s&type=both')]" %(state_code,link)
				time.sleep(.5)					
				self.click_link(state,link,la)
			self.driver.switch_to.default_content()
	
if __name__ == '__main__':
	h = njdg_state()
	h.navigate()
	time.sleep(10)
	#h.enter()
	h.states()
	#h.states1()
