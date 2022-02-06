import time
import selenium
import json
import base64
from flask import Flask, jsonify, request
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC


application = Flask(__name__)

@application.route( '/invoice-report-usb', methods=["POST", "GET"] )
def invoicereportUsb():
	try:
		# ____________For WINDOWS server ___________________
		options = selenium.webdriver.ChromeOptions()
		# options.add_argument('headless')
		browser = webdriver.Chrome(chrome_options=options)
	except Exception as e:
		return jsonify( {"message": "Driver Not Found"} )
	try:
		usernameStr = request.form.get( "username" )
		passwordStr = request.form.get( "password" )
		dateFrom = request.form.get( "date_start" )
		dateTo = request.form.get( "date_end" )

		# encoded_data = base64.b64encode(passwordStr.encode('UTF-8')).decode('ascii')
		# decoded_pass = base64.b64decode(passwordStr.encode('UTF-8')).decode('ascii')
		# # print("encrytPass", encoded_data)
		# print("decrytPass", decoded_pass)

		login_url = "https://fo-asia.ttinteractive.com/Zenith/FrontOffice/(S(uq5lnvnhzcwhekoexpdb2kpo))/USBangla/en-GB/travelAgency/Login"

		browser.get(login_url)

		print("username-", usernameStr)
		print("pass-", passwordStr)

		# if usernameStr == "" or passwordStr == "":
		# 	usernameStr = "latiftravels"
		# 	passwordStr = "shamim2020"
		# else:
		# 	pass

		usernamefield = browser.find_element_by_id('LoginLog')
		usernamefield.send_keys(usernameStr)

		passwordfield = browser.find_element_by_id('LoginPwd')
		# passw = "shamim2020"
		passwordfield.send_keys(passwordStr)

		submitBtn = browser.find_element_by_id('Submit1')
		submitBtn.click()

		current_page_url = browser.current_url

		# ____________Login Credential Check___________________
		addrs_1 = "https://fo-asia.ttinteractive.com/newui/aerien/f_index.asp"
		addrs_2 = "http://fo-asia.ttinteractive.com/newui/aerien/f_index.asp"

		if not (current_page_url == addrs_2 or current_page_url == addrs_1):
			browser.close()
			return jsonify({"message": " Username or Password mismatched, Contact with Administrator"})
		else:

			# ____________Search Page___________________
			search_url = "https://fo-asia.ttinteractive.com/newui/aerien/f_index.asp?Id_SessionLangue=2#menu2-item153"

			browser.get(search_url)

			# ____________Ad 2 ___________________
			try:
				ad2 = browser.find_element_by_id("IMSMessageClose")
				ad2.click()
			except:
				pass


			# ____________Search Page___________________
			search_url = "https://fo-asia.ttinteractive.com/newui/aerien/f_index.asp#menu2-item154"

			browser.get(search_url)

			
			browser.switch_to.default_content()
			# ____________Goto iFrame___________________
			browser.switch_to.frame("mainFrame")
			
			# ___________Date Range__________________
			
			date_from = browser.find_element_by_id("usrPNRSearch_ctl00_PNRDateCreationMin")
			date_from.send_keys(Keys.HOME, dateFrom, Keys.TAB)

			# ____________Return Date___________________
			time.sleep(2)
			date_to = browser.find_element_by_id("usrPNRSearch_ctl00_PNRDateCreationMax")
			date_to.clear()
			date_to.send_keys(Keys.HOME, dateTo, Keys.TAB)

			# __________________Search button_________________

			searchBtn = browser.find_element_by_id("usrPNRSearch_ctl00_lbSearch")
			searchBtn.click()
			# ____________Goto iFrame___________________

			browser.switch_to.default_content()
			browser.switch_to.frame("mainFrame")

			# ____________Pagination____________
			pagination = browser.find_element_by_class_name("divPaginationAndCount")
			paginationText = pagination.text
			print(len(paginationText))

			invoice_info_array = []
			singlePage = pagination.find_elements_by_class_name("pageItem")
			row_serial = 0
			noOfData = 1
			pnr = []
			for page in singlePage:

				# ____________Goto iFrame___________________
				browser.switch_to.default_content()
				browser.switch_to.frame("mainFrame")
				# page.click()
				if row_serial == 0:
					pass
				elif row_serial == (len(paginationText)) :
					print("hoini")
					pass
				else:
					time.sleep(2)
					pageXpath = browser.find_element_by_xpath('//*[@id="PNRSeachInfos"]/fieldset/span/div/a[' + str(row_serial) + ']')
					pageXpath.click()
					# time.sleep(1)
					print("hoice")

				print("row_serial: ", row_serial)
				row_serial = row_serial + 1
				time.sleep(.5)
				resultBody = browser.find_element_by_id("results_wrapper")

				tableBody = resultBody.find_element_by_tag_name("table")
				tableTbody = tableBody.find_element_by_tag_name('tbody')

				pnrRow = tableTbody.find_elements_by_tag_name("tr")
				for row in pnrRow:  
					noData = row.text
					# print("noData:", noData)
					if not (row.get_attribute('class')=="spacer" or noData == "No data available in table"):
						pnrDict = {}
						browser.switch_to.default_content()
						browser.switch_to.frame("mainFrame")

						# pnrCol = row.find_element_by_class_name("pnrlink")
						pnrCol = row.find_element_by_class_name("th-pnr-code")
						# pnrDict["PNR "+str(noOfData)+""] = pnrCol.text
						pnr.append(pnrCol.text)

						print("No of data: ", noOfData)
						noOfData = noOfData + 1
					else:
						print("pass hoice")
						pass

			print(pnr)
			ticket_info_array = []

			for i in range(len(pnr)):

				# ____________Search Page___________________
				# search_url = "https://fo-asia.ttinteractive.com/newui/aerien/f_index.asp#menu2-item154"
				# browser.get(search_url)
				
				browser.switch_to.default_content()
				time.sleep(1)
				search_pnr = browser.find_element_by_id("Search")
				search_pnr.clear()
				search_pnr.send_keys(Keys.HOME, pnr[i], Keys.ENTER)

				time.sleep(1)
				newfrm = browser.find_element_by_class_name("primaryFrameZone")
				search_frame = newfrm.find_element_by_tag_name("iframe")
				browser.switch_to.frame(search_frame)

				# _______Coupon Page__________
				time.sleep(0.2)

				# couponTicketnumber
				FNTPNRCode_value = browser.find_element_by_class_name("FNTPNRCode").text
				ticketStatus = browser.find_element_by_id("instanceCtrlContent_ctrlEnteteSyntheseDossier_lblEtatDossier")
				# onwardflight = browser.find_element_by_class_name("TripOutbound").text
				onwardflightDateT = browser.find_element_by_class_name("TripOutboundDate").text
				onwardflightDate = onwardflightDateT.replace('Departure ', "")
				issue_Date = browser.find_element_by_id("instanceCtrlContent_ctrlInfoBaseDossier_lbDateCreation").text
				returnFlight = browser.find_element_by_class_name("TripInbound").text
				returnflightDateT = browser.find_element_by_class_name("TripInboundDate").text
				returnflightDate = returnflightDateT.replace('Departure ', "")
				total_Fare = browser.find_element_by_id("instanceCtrlContent_UsrDossierSynthese_ctrlSyntheseTarifDossier_lblTotalDossier").text.replace(",","")
				totalBase_Fare = browser.find_element_by_id("instanceCtrlContent_UsrDossierSynthese_ctrlSyntheseTarifDossier_lblPrixTotalHT").text.replace(",","")

				ticket_info_dic = {}
				paxInfoArry = []

				comIndex = 2
				segment = browser.find_element_by_class_name("SegmentsContent")
				# pax_ro = segment.find_elements_by_class_name("paxRow")
				segmentRo = segment.find_elements_by_class_name("segmentRow")
				adultNo = 0
				childNo = 0
				infantNo = 0
				segmentNo = 1

				for paxSegment in segmentRo:
					sectorFlight = paxSegment.find_element_by_class_name("segmentHeaderLeg").text
					pax_ro = paxSegment.find_elements_by_class_name("paxRow")
					for pax in pax_ro:
						pnr_dict = {}

						info_box = pax.find_element_by_class_name("couponInfos")
						ticket_class_value = info_box.find_element_by_class_name("couponFareBasis").text
						ticket_number_value = info_box.find_element_by_class_name("couponTicketnumber").text
						ticketNoSplit = ticket_number_value.split(" ")
						ticket_no = ticketNoSplit[0]
						try:
							basefare1 = info_box.find_element_by_class_name("couponNetFare").text
							basefare = basefare1.replace('Price Exc. Taxes\n', "")
							tax1 = info_box.find_element_by_class_name("couponTaxes").text
							tax = tax1.replace('Taxes\n', "")
							totalAmount = info_box.find_element_by_class_name("couponTotalFares").text
						except:
							basefare = ""
							tax = ""
							totalAmount = ""

						try:
							commission = browser.find_element_by_id("instanceCtrlContent_ctrlSyntheseEcriture_dlListePrestations_ctl0" + str(comIndex) + "_divValVenduDevBase").text
							comIndex += 2
						except:
							commission = "not found"

						pax_name_row = pax.find_element_by_class_name("couponHeader")
						pax_name_c = pax_name_row.find_element_by_class_name("paxName").text
						pax_nameBrck = pax_name_c.split(" ")
						# print(pax_nameBrck)
						pax_name1 = pax_name_c.replace("AD ", "")
						pax_name2 = pax_name1.replace("CHD Child", "")
						# print("pax_name2-",pax_name2)
						pax_name = pax_name2.replace("INF Infant", "")
						# print(pax_name)
						pax_type = pax_nameBrck[0]
						if segmentNo == 1:
							if pax_type == "AD":
								pax_serial = 0
								adultNo = adultNo + 1
							elif pax_type == "CHD":
								pax_serial = 1
								childNo = childNo + 1
							elif pax_type == "INF":
								pax_serial = 2
								infantNo = infantNo + 1
						else:
							pass

						pax_salutation = pax_nameBrck[1]
						ticketStatusChld = pax_name_row.find_element_by_class_name("couponStatus").text

						# if colIndex != 0:
						pnr_dict["TicketNo"] = ticket_no
						pnr_dict["TicketPassengerType"] = pax_serial
						pnr_dict["IssueDate"] = issue_Date
						pnr_dict["TravelDate"] = onwardflightDate
						pnr_dict["IATACode"] = ""
						pnr_dict["Sector"] = sectorFlight
						pnr_dict["TravelClassCode"] = ""
						pnr_dict["TravelClass"] = ticket_class_value.replace('Class\n', "")
						pnr_dict["PaxSalutation"] = pax_salutation.strip(".")
						pnr_dict["PaxName"] = pax_name.strip()
						pnr_dict["TravelReturnClassCode"] = ""
						pnr_dict["ReturnClass"] = ""
						if "BDT" in basefare:
							pnr_dict["BaseFare"] =basefare.strip(" BDT").replace(",", "")
						elif "MYR" in basefare:
							pnr_dict["BaseFare"] =basefare.strip(" MYR").replace(",", "")		
						if "BDT" in tax:
							pnr_dict["tax"] =tax.strip(" BDT").replace(",", "")
						elif "MYR" in tax:
							pnr_dict["tax"] =tax.strip(" MYR").replace(",", "")
						if "BDT" in commission:
							pnr_dict["Commission"] =commission.strip(" BDT").replace(",", "")
						elif "MYR" in commission:
							pnr_dict["Commission"] =commission.strip(" MYR").replace(",", "")
						else:
							pnr_dict["Commission"]=""

						pnr_dict["TaxDetails"] = ""
						
						pnr_dict["CommissionTax"] = ""
						pnr_dict["Ticket_status"] = ticketStatusChld
						# pnr_dict["Total_Price"] = totalAmount.replace('Total Amount\n', "")
						paxInfoArry.append(pnr_dict)
					segmentNo = segmentNo + 1

				
				ticket_info_dic["PNR"] = FNTPNRCode_value
				ticket_info_dic["Transaction_Description"] = ticketStatus.text
				if "BDT" in totalBase_Fare:
					ticket_info_dic["TotalBaseFare"] = totalBase_Fare.strip(" BDT").replace(",", "")
				elif "MYR" in totalBase_Fare:
					ticket_info_dic["TotalBaseFare"] = totalBase_Fare.strip(" MYR").replace(",", "")
				if "BDT" in total_Fare:
					ticket_info_dic["TotalFare"] = total_Fare.strip(" BDT").replace(",", "")
				elif "MYR" in total_Fare:
					ticket_info_dic["TotalFare"] = total_Fare.strip(" MYR").replace(",", "")
				
				
				ticket_info_dic["TotalCommission"] = ""
				ticket_info_dic["TotalCommissionTax"] = ""
				ticket_info_dic["TravelDate"] = onwardflightDate
				ticket_info_dic["IssueDate"] = issue_Date
				ticket_info_dic["ReturnDate"] = returnflightDate
				ticket_info_dic["Return_Flight"] = returnFlight
				ticket_info_dic["NoOfAdult"] = adultNo
				ticket_info_dic["NoOfChild"] = childNo
				ticket_info_dic["NoOfInfant"] = infantNo
				ticket_info_dic["CustomerId"] = ""
				ticket_info_dic["SupplierId"] = ""
				ticket_info_dic["TicketInfo"] = paxInfoArry

				ticket_info_array.append(ticket_info_dic)


			print(ticket_info_array)
			# return jsonify( ticket_info_array )
			# print(ticket_info_array)
			browser.quit()
			return jsonify(ticket_info_array)

	except Exception as e:
		browser.quit()
		return jsonify ({"message": "Contact With Administrator"})
		

if __name__ == '__main__':
	application.run( port='8000', host='127.0.0.1', debug=True)