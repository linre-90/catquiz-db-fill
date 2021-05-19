# Written 11.5.2021 with Jupyter Notebook by linre-90 
#
# [DESCRIPTION]
# Script fills cat's opinions quiz-app database. 
#
# [STEPS DESCRIPTION]
# Reads open office calc document saved as csv file.
# Converts data to python dictionary, checks for empty fields.
# Seperates questions to easy | medium | hard categories.
# Connects to firebase project with .json credentials
# Reads connection URL for firebase db from config.ini
# Creates database structure and fills it, asks input for language code.
# Not most beautifull script but it was fast to write and works...

import csv

# temp index to limit data amount while checking headers 
index = 5

questionTank = []

# csv files created from open office calc
# fi questions csv file
fi_file = "questions_fi.csv"
# en questions csv file
en_file = "questions_en.csv"

# read csv
with open(en_file, newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if index < 0:
            break
        #print(row)
        #print(row["easy"])
        #print(row["medium"])
        #print(row["hard"])
        
        temp = {
            "question": row["question"],
            "correct": row["correct"],
            "false1": row["option1"],
            "false2": row["option2"],
            "explanation": row["Explanation"]
        }
        
        # map difficulty to type
        difficultyIndicator = "x"
        if row["easy"] == difficultyIndicator:
            temp["type"] = "easy"
        elif row["medium"] == difficultyIndicator:
            temp["type"] = "medium"
        elif row["hard"] == difficultyIndicator:
            temp["type"] = "hard"
        else:
            print("Error in data! On line: ",reader.line_num)
            raise ValueError("invalid difficulty")    
        
        # check data has length
        for key in temp:
            if len(temp[key]) < 1:
                print("Error in data! On line: ",reader.line_num)
                raise ValueError("Missing data")   
        
        #print(temp)
        
        # append to list that is gonna be saved in db
        questionTank.append(temp)
        
        #index = index -1
        
#print(questionTank)



# spread questionTank to seperate difficulties
easy = []
medium = []
hard = []

for entry in questionTank:
    if entry["type"] == "easy":
        easy.append(entry)
    elif entry["type"] == "medium":
        medium.append(entry)
    elif entry["type"] == "hard":
        hard.append(entry)

# check balance
print("Easy questions: ", len(easy))
print("Medium questions: ", len(medium))
print("Hard questions: ", len(hard))
print("Total questions: ", (len(easy) + len(medium) + len(hard)))




# install firebase_admin with pip
#import sys
#!{sys.executable} -m pip install --upgrade pip
#!{sys.executable} -m pip install firebase-admin



# get db url from config.ini
import configparser

# read config file
config = configparser.ConfigParser()
config.read("config.ini")

#print(config["DEFAULT"]["dburl"])

db_url = config["DEFAULT"]["dburl"]



# connect to firebase admin to project
import firebase_admin
from firebase_admin import credentials

# load certificate
cred = credentials.Certificate("certificate.json")

# get the app
firebase_admin.initialize_app(cred,{'databaseURL': db_url})


from firebase_admin import db

# language ref
ref_en = db.reference(input("What language code are we processing?"))

# difficulty refs
ref_en_easy = ref_en.child("easy")
ref_en_medium = ref_en.child("medium")
ref_en_hard = ref_en.child("hard")


# feed easy
for i in range(len(easy)):
    ref_en_easy.child(str(i)).set(easy[i])
    
# feed medium
for j in range(len(medium)):
    ref_en_medium.child(str(j)).set(medium[j])
    
# feed hard  
for k in range(len(hard)):
    ref_en_hard.child(str(k)).set(hard[k])






