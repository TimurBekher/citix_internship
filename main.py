import pandas as pd 
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def filter_data(row):
	"""
	This function deletes data indicating the absence of anything in the house using the dictionary generator
	"""
	filtered_data = {key: value for key, value in row.items() if value != 'no' }
	return filtered_data



def get_random_rows():
	"""
	This function extracts 20 random strings from the dataset
	"""
	df = pd.read_csv('Housing.csv')
	rows = []
	for _ in range(20):
		# Choosing a random string
		random_row_index = df.sample().index[0]  # Getting the index of a random string
		random_row = df.loc[random_row_index]  # Getting random row
		random_row = random_row.to_dict() #converting row to dict
		filtered_row = filter_data(random_row) #filtering "no" values
		rows.append(filtered_row) #Adding the data to the list
		df = df.drop(random_row_index) #Deleting the selected row from the dataset
	return rows


def add_post(data,post):
	"""
	This function writes posts to  EXAMPLE.txt
	"""
	divider = "------------------------\n"
	with open('EXAMPLE.txt','a', encoding="utf-8") as file: #opening file
		for key, val in data.items(): #Unpacking keys and values from data dict
			file.write(f"{key}={val}\n") #Writing parameters to file
		file.write(post+"\n") #Writing post`s text to file
		file.write(divider) #Writing divider



def run_conversation():
	"""
	This function starts a dialog with chatGPT,
	sends data from the dataset in turn,
	accepts the response and sends it to the add_post function
	"""
	data = get_random_rows() #Getting random 20 rows from dataset
	for row in data: #Creating completions for each row
		messages = [{"role": "user", "content": f''' I will send you the real estate data in the form of a Python dictionary.
											    Generate a sales text for an Instagram post for each dataset. Here is data:{row}'''} ]

		response = client.chat.completions.create(
			model="gpt-3.5-turbo",
			messages=messages
		)
		add_post(data=row, post=response.choices[0].message.content) #Adding post and data to file

	

run_conversation()