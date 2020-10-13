import time
import requests
import hashlib
import urllib.parse

base_url = "https://gateway.marvel.com/v1/public/characters?"

api_key = input("Enter your public key: ")
private_key = input("Enter your private key: ")
ts = str(time.time())

#Turns the timestamp, private and public key into a hashed value.
hash = hashlib.md5()
hash.update(bytes(ts, 'utf-8'))
hash.update(bytes(private_key, 'utf-8'))
hash.update(bytes(api_key, 'utf-8'))
hasht = hash.hexdigest()


def select():
    main_menu = input("How do you want to search a character?\n1: By it's full name\n2: By the first letters of it's name\n0: quit\n")
    query_url = ""
    if main_menu == "1":
        #The query will become name=<input>
        query_url = "name=" + input("Enter your hero's name:\n") + "&"
    elif main_menu == "2":
        #The query will become nameStartsWith=<input>
        query_url = "nameStartsWith=" + input("Enter the first letters of your hero's name:\n") + "&"   
    
    elif main_menu == "0":
        query_url = "quit"

    else:
        query_url = "invalid"

    return query_url

while True:
    #Selects which search criteria to use. Exits the script cleanly or with an exception error.
    query_url = select()

    if query_url == "quit":
        break

    elif query_url == "invalid":
        print("Please enter a valid number!")
        break

    else:
        #Construct the complete URL
        url = base_url + query_url + urllib.parse.urlencode({"apikey" : api_key, "hash": hasht, "ts": ts, "limit": 100})

        print("URL: " + (url))

        json_data = requests.get(url).json()
        json_code = json_data["code"]
        
        #if the response is successfull, reply with code 200 and message Ok
        if json_code == 200:
            print("Response code: " + str(json_code) + ": " + str(json_data["status"]))

        #if the response contains errors, reply with the error message
        else:
            print("Error: " + str(json_code) + ": " + str(json_data["message"]))
            break

        #show the amount of results the query returns
        total = json_data["data"]["total"]
        print("Total results: " + str(total))

        #if there is exactly 1 result, show the result + extra information
        if total == 1:
            print("Name:\t\t" + str(json_data["data"]["results"][0]["name"]))
            print("Description:\t" + str(json_data["data"]["results"][0]["description"]))
            print("=================================")
            print("Total appearances in comics: " + str(json_data["data"]["results"][0]["comics"]["available"]))
            print("=================================")
        
        #if there is more than 1 result, show a list of character names
        if total > 1:    
            for each in json_data["data"]["results"]:
                print(str (each["name"]))

        #if therer are no results, show a message
        if total == 0:
            print("No hero found with that name")