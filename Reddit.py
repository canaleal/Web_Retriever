import praw
import requests

from Database import *
from Modules import *


# Set Reddit Client with data from file and return client
def config_reddit():
    text_data = open("info.txt", "r")
    if text_data.readable():
        arr = text_data.readlines()
        text_data.close()
        return praw.Reddit(client_id=arr[0].rstrip(),
                           client_secret=arr[1].rstrip(),
                           username=arr[2].rstrip(),
                           password=arr[3].rstrip(),
                           user_agent=arr[4].rstrip())


# Manager sets and gets user data from Reddit Client
def get_manager(main_obj_inst, x):
    data, data_obj = None, None
    try:
        if database_obj is not None:
            print("\n")
            database_obj.print_item("recent")
            database_obj.print_item("category")
        if x == 1:
            data = input("Insert Sub-Reddit: ")
            data_obj = main_obj_inst.subreddit(data)
        elif x == 2:
            data = input("Insert User: ")
            data_obj = main_obj_inst.redditor(data)

        count_pic = get_number("a positive number of Images")
        directory = input("Save Location: ")
        set_dir(directory)

        items = get_data(data_obj, count_pic)
        save_data(directory, data, items[0], items[1])
    except Exception as e:
        print(e)


# Get time returns array of data from Reddit Client
def get_data(data_obj, count_pic):
    while True:
        print("\n0:Hot\n1:New\n2:Top")
        setting = get_number("an option")
        if setting == 0:
            return data_obj.hot(limit=count_pic), "Hot"

        elif setting == 1:
            return data_obj.new(limit=count_pic), "New"

        elif setting == 2:
            return data_obj.top(limit=count_pic), "Top"

        else:
            print("Not an option.")


# Save images to a folder and store recent if mongoDB account exists
def save_data(directory, sub, data_array, category):
    i = 0
    for submit in data_array:
        if not submit.stickied:
            if ".jpg" not in submit.url or ".png" not in submit.url:
                continue
            else:
                print(submit.url)
                img_data = requests.get(submit.url).content
                encoded = bytes((directory + "/" + sub + str(i) + ".jpg"), encoding='utf-8')
                with open(encoded, 'wb') as handler:
                    handler.write(img_data)
                    i = i + 1

    print("Done.")
    if database_obj.get_id() is not '':
        database_obj.update_recent(sub)
        database_obj.update_category(category)


def menu_user():
    while True:
        print("\n0:Clear\n1:Update-Password\n2:Delete-Account (Requires Login)\n3:Exit")
        option3 = get_number("an option")
        if option3 == 0:
            shift()
        elif option3 == 1:
            database_obj.update_password(get_input("Enter old password"), get_input("Enter new password"))
        elif option3 == 2:
            print("0:Keep Account\n1:Delete Account")
            if get_number("an option") == 1:
                database_obj.delete_account(get_input("Password"))
        elif option3 == 3:
            shift()
            break
        else:
            print("Not an option.")


# Main Menu with user options. Prompts shown inside print.
def menu_search():
    while True:
        print("\n0:Clear\n1:Sub-Reddit\n2:User-Reddit\n3:Manage-User (Requires Login)\n4:Exit")
        option2 = get_number("an option")
        if option2 == 0:
            shift()
        elif option2 == 1 or option2 == 2:
            get_manager(main_obj, option2)
        elif option2 == 3 and database_obj is not None:
            menu_user()
        elif option2 == 4:
            print("\n")
            break
        else:
            print("Not an option.")


if __name__ == "__main__":

    if test_connection():
        main_obj = config_reddit()
        database_obj = Database()
        while True:
            print("\n0:No Database\n1:Login\n2:SignUp\n3:Exit")
            option = get_number("an option")
            if option == 0:
                menu_search()
            elif option == 1:
                print("\nEnter Credentials:")
                if database_obj.login(get_input("Username"), get_input("Password")):
                    menu_search()

            elif option == 2:
                database_obj.sign_up(get_input("Username"), get_input("Password"))

            elif option == 3:
                break
            else:
                print("Not an option.")
    else:
        print("Can't connect to the internet.")
