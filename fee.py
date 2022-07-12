# Write a program for Fees management system.
#   1. Deposit fees of a student
#   2. Defaulters students list based on year
#   3. Display of a student who has submitted the fees based on year
#   4. Display of student who has not submitted the fees based on year
#   5. Display fees structure depending upon the student year
#   6. Display last date of submitting the student fees
#   7. Provide 10% discount to some students (OPTIONAL)
#   8. Generate a report/file based on the different year

# for using os , json and datatime module
import os
import json
from datetime import date

# class for the system
class fees():
    flag = 1

    def __init__(self):
        """"""
        # Check if file exist or not
        # If not exist, then create the file else continue

        self.complete_path = self.get_complete_path_file()
        if not (os.path.exists(self.complete_path)):
            standard_json_file = {"students": []}

            # File does not exists
            with open(self.complete_path, 'w') as new_file:
                json.dump(standard_json_file, new_file)
            
    # function creating the folder and file for storing the database
    def get_complete_path_file(self):
        # for creating the file path
        folder_path = "Fees_management"
        separator = "/"
        file_path = "Fee_file.json"
        complete_path = folder_path + separator + file_path
        return complete_path

    # Function to open file in read mode and read lines
    def read_json_file(self):
        """Reading from json fiile"""

        # opening file in read mode
        with open(self.complete_path, 'r') as json_file:
            custom_file = json.load(json_file)
        
        return custom_file
        
    # Function to open file in write mode and write data in it
    def write_json_file(self, new_data):
        """Writing in json file"""

        # open file in write mode
        with open(self.complete_path,"w") as file:
            # Writing the complete data to the file
            json.dump(new_data, file)

    def input_deposit_fees(self):
        """"""
        # Getting the new contents/data
        student_no = input("Enter your roll no = ")
        student_name = input("Enter your name = ") 
        current_year = input("Enter the year you are studying in = ")
        percentage = int(input("Enter your percentage = "))
        
        # read from json file 
        old_data = self.read_json_file()

        # read the fee structure
        stored_year_data = self.read_stored_data()

        # find out = keys
        keys_of_stored_structure = stored_year_data['fee_structure'].keys()
        list(keys_of_stored_structure)

        # check if invalid percentage enetered
        if (percentage > 100):

            print("Invalid percentage entered")
            self.flag = 0
        
        # if valud then check for scholarship
        elif (percentage > 95):

            for key in keys_of_stored_structure:

                if( str(key) == current_year ):

                    fee_deposit = int(input("Deposit your fees = "))
                    fee_deposit = fee_deposit - stored_year_data['fee_structure'][str(key)]['scholarship_amount']
                    print(stored_year_data['fee_structure'][str(key)]['scholarship_amount']," : Amount refunded because of good percentage")
                    scholarship = "Given"

        
        else:

            fee_deposit = int(input("Deposit your fees = "))
            scholarship = "None"


        # to check if student's data is already entered or not
        for roll_no in old_data['students']:

            if(roll_no['Roll_no'] == student_no):

                print("Roll no. already Entered earlier")
                self.flag = 0

        # Check if fees is entered higher than required fees

        if fee_deposit > stored_year_data['fee_structure'][current_year]['total_fees']:

            print("cannot submit fees more than the required amount.")
            self.flag = 0

        # if both the earlier conditions are fallse then write the data into the file
        if not self.flag == 0:

            # Formatted the new data/contents
            student = {
                "Roll_no" : student_no,
                "Student_Name" : student_name,
                "Year_studying_in" : current_year,
                "Percantage " : percentage,
                "Deposited_amount" : int(fee_deposit),
                "Date_submitted_on" : str(date.today()),
                "Scholarship" : scholarship
            }
            return student
        
    # function to  deposite fees
    def deposit_fees(self):
        """Deposit Fees"""

        # Read the json file
        old_data = self.read_json_file()
        
        # Assigning to new data
        new_data = old_data

        # Taking input from user
        student = self.input_deposit_fees()

        if student:
            # Appending the new contents/data to the old content/data
            new_data['students'].append(student)
    
            # Write to JSON file
            self.write_json_file(new_data=new_data)
    
    # function to read from stored data
    def read_stored_data(self):
        """Reading the fee structure"""

        # opening the fee structure file in read format
        with open("Fees_management" + "/" + "fee_structure.json", 'r') as json_file:
            custom_file = json.load(json_file)
        
        return custom_file

    # function to find defaulter's name
    def defaulter_name(self):
        """Defaulter's name"""

        # read from json file
        data = self.read_json_file()

        # read data from stored file
        stored_year_data = self.read_stored_data()

        # find out keys
        keys_of_stored_structure = stored_year_data['fee_structure'].keys()
        list(keys_of_stored_structure)

        # loop to find defaulter's name by reading the total fees from stored data
        print("Defaulter's Name :- ")
        for  key in keys_of_stored_structure:

            for student_detail in data['students']:

                # if fee entered is less than required fee for none scholarship amount
                if  (student_detail['Scholarship'] == "None" and student_detail['Deposited_amount'] < stored_year_data['fee_structure'][str(key)]['total_fees'] and student_detail['Year_studying_in'] == key ):

                    print("Name : ",student_detail['Student_Name'])
                    print("Year : ",student_detail['Year_studying_in'])
                
                elif (student_detail['Scholarship'] == "Given" and student_detail['Deposited_amount'] < stored_year_data['fee_structure'][str(key)]['After_scholarship'] and student_detail['Year_studying_in'] == key ):

                    print("Name : ",student_detail['Student_Name'])
                    print("Year : ",student_detail['Year_studying_in'])

    # function to find student's datails if fee submitted based on year
    def student_detail_if_fee_submitted_based_year(self):
        """Student's details if fee submmitted based on year"""

        # read from json file
        data = self.read_json_file()

        # read data from stored file
        stored_year_data = self.read_stored_data()

        # find out keys
        keys_of_stored_structure = stored_year_data['fee_structure'].keys()
        list(keys_of_stored_structure)

        # input the year for which we need to find details of that student
        year = input("Enter the year = ")

        # using loop to find student's detail if fee submitted based on year
        for key in keys_of_stored_structure:

            for student_detail in data['students']:

                # check student year with the input year
                if (student_detail['Year_studying_in'] == year ):

                    # check with year from the stored data and compare deposited amount with the total fee from stored data for none scholarship student
                    if ( student_detail['Scholarship'] == "None" and year ==  key  and student_detail['Deposited_amount'] == stored_year_data['fee_structure'][str(key)]['total_fees'] ):

                        print("Student Roll no = ",student_detail['Roll_no'])
                        print("Student Name = ",student_detail['Student_Name'])
                    
                    # check with year from the stored data and compare deposited amount with the total fee from stored data for given scholarship student
                    elif ( student_detail['Scholarship'] == "Given" and year ==  key  and student_detail['Deposited_amount'] == stored_year_data['fee_structure'][str(key)]['After_scholarship'] ):

                        print("Student Roll no = ",student_detail['Roll_no'])
                        print("Student Name = ",student_detail['Student_Name'])
                    

    # function to find student detail if fee not submitted based on year
    def student_detail_fee_not_submitted_based_year(self):
        """Student's details if fee not submmitted based on year"""

        # read from json file
        data = self.read_json_file()

        # read data from stored file
        stored_year_data = self.read_stored_data()

        # find out keys
        keys_of_stored_structure = stored_year_data['fee_structure'].keys()
        list(keys_of_stored_structure)

        # input the year for which we need to find details of that student
        year = input("Enter the year = ")

        # using loop to find student's detail if fee submitted based on year
        for key in keys_of_stored_structure:
            for student_detail in data['students']:

                # check student year with the input year
                if(student_detail['Year_studying_in'] == year ):

                    # check with year from the stored data and compare deposited amount with the total fee from stored data
                    if( student_detail['Scholarship'] == "None"and year ==  key  and student_detail['Deposited_amount'] < stored_year_data['fee_structure'][str(key)]['total_fees'] ):

                        print("Student Roll no = ",student_detail['Roll_no'])
                        print("Student Name = ",student_detail['Student_Name'])
        
                    # check with year from the stored data and compare deposited amount with the total fee from stored data
                    elif( student_detail['Scholarship'] == "Given" and year ==  key  and student_detail['Deposited_amount'] < stored_year_data['fee_structure'][str(key)]['After_scholarship'] ):

                        print("Student Roll no = ",student_detail['Roll_no'])
                        print("Student Name = ",student_detail['Student_Name'])
        

    # function to display fee structure
    def fee_structure(self):
        """To display fee structure"""

        stored_year_data = self.read_stored_data()

        # find out keys
        keys_of_stored_structure = stored_year_data['fee_structure'].keys()
        list(keys_of_stored_structure)

        # input the year for which we need to find details of that student
        year = input("Fee Structure of the year = ")

        # using loop to iterate over the stored and find year and print the fee structure
        for key in keys_of_stored_structure:

            if(year == key):
                
                print("Tuition fees : ",stored_year_data['fee_structure'][str(key)]['tution_fees'])
                print("Training fees : ",stored_year_data['fee_structure'][str(key)]['training_fees'])
                print("Extra curricular fees : ",stored_year_data['fee_structure'][str(key)]['extra_curricular'])
                print("Total fees : ",stored_year_data['fee_structure'][str(key)]['total_fees'])
                print("Last Date to Deposit : ",stored_year_data['fee_structure'][str(key)]['last_date_submit'])
                print("Scholarship Amount : ",stored_year_data['fee_structure'][str(key)]['scholarship_amount'])
                print("After Scholarship, Fee : ",stored_year_data['fee_structure'][str(key)]['After_scholarship'])
                # stored_year_data['fee_structure'][str(key)]['total_fees']

    # function to display last date of submitting fees
    def last_date(self):
        """Last date to submit fees"""

        # read data from stored file
        stored_year_data = self.read_stored_data()

        # find out keys
        keys_of_stored_structure = stored_year_data['fee_structure'].keys()
        list(keys_of_stored_structure)

        # input the year for which we need to find the last date to submit ffee
        year = input("Enter the year = ")

        # using loop to find the year from fee structure file and print the last date to submit fee 
        for key in keys_of_stored_structure:

            if(year == str(key)):

                print("Last Date to Deposit : ",stored_year_data['fee_structure'][str(key)]['last_date_submit'])
        
    # function to display the report file of the student
    def report_file(self):
        """To generate report file"""

        # read from json file
        data = self.read_json_file()

        # read data from stored file
        stored_year_data = self.read_stored_data()

        # find out keys
        keys_of_stored_structure = stored_year_data['fee_structure'].keys()
        list(keys_of_stored_structure)

        # input the year for which we need to find details of that student
        year = str(input("Enter the year you want to generate report for = "))

        # creating an empty dictionary
        report_data = {'students': []}

        # using loop to find the year for which report file is to be created
        for key in keys_of_stored_structure:

            for student_detail in data['students']:

                if(year == key and year == student_detail['Year_studying_in']):

                    # if found then add the student details to the empty dictionary
                    report_data['students'].append(student_detail)

        # add the fee structure details of that year to the dictionary 
        report_data.update({'fees_structure': stored_year_data['fee_structure'].get(year, {})})

        # created the report file for that file in write format and dump the dictionary to that file
        with open("Fees_management" + "/" + year +"report_file.json", "w") as newfile:
            json.dump(report_data, newfile)

    # function to continue
    def user_continue(self):

        # taking input to continue or not
        user_choice = input("Do you want to continue = ")
        return user_choice
        

# main function
def main():
    """Main function"""
    # we will use it for menu's loop

    # creating class object
    fees_object1 = fees()

    user_choice = "Yes"


    # loop for menu
    while(user_choice.lower() == "yes" ):
        print("Menu :- \n1. Deposit fees of a student \n2. Defaulters students name list ")
        print("3. Display student's details who has submitted the fees based on year\n4. Display student's name who has not submitted the fees")
        print("5. Display fee structure based on year\n6. Display last date of submitting fees\n7. Generate a report file\n8. Exit")
        menu_choice = int(input("Enter your choice = "))


        # for depositng the fees of the student
        if (menu_choice == 1):
            fees_object1.deposit_fees()
            user_choice = fees_object1.user_continue()

        # for finding defaulter's name
        elif (menu_choice == 2):
            fees_object1.defaulter_name()
            user_choice = fees_object1.user_continue()

        # for displaying student's detail based who has submitted the fees based on year
        elif (menu_choice == 3):
            fees_object1.student_detail_if_fee_submitted_based_year()
            user_choice = fees_object1.user_continue()

        # for displaying student's details who has not submitted the fees based on year
        elif (menu_choice == 4):
            fees_object1.student_detail_fee_not_submitted_based_year()
            user_choice = fees_object1.user_continue()
        
        # for displaying fee structure based on year
        elif (menu_choice == 5):
            fees_object1.fee_structure()
            user_choice = fees_object1.user_continue()

        # function to display last date of submitting fees
        elif (menu_choice == 6):
            fees_object1.last_date()
            user_choice = fees_object1.user_continue()
        
        # to generate report file
        elif (menu_choice == 7):
            fees_object1.report_file()
            user_choice = fees_object1.user_continue()

        # to exit the progam
        elif (menu_choice == 8):
            print("Thank You")
            exit()

        # wrong choice entered
        else:
            print("Wrong Choice Entered")
            user_choice = fees_object1.user_continue()


    else:
        print("Thank You")
        exit()
            

# main
if __name__ == "__main__":
    main()