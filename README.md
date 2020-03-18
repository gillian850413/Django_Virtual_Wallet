# Django Virtual Wallet Project
This project aims to develop a virtual wallet web application using Django. The app allows the users to send/request money to other users and manage their spendings and payment information. It also has web pages for admin and staff to check the user list and all the transactions made in the app. These pages will not be visible to regular app users. <br>

**Application Link:** 

<img src="https://github.com/gillian850413/Django_Virtual_Wallet/blob/master/screenshot.png" width="550" height="300" />

## Requisites
- Django 2.2.5 (or later version)
- Python 3.7
- Pycharm 
- Anaconda
- SQLite

## Setup
This project requires Python 3.7 and conda environment. To setup the environment, please follow these steps:
- Create a new conda virtual environment in local or cloud services
```
conda create -n django_env python=3.7.4 
conda activate django_env 
```
- Clone the github repository
```
git clone https://github.com/gillian850413/Django_Virtual_Wallet.git
```
- Install the required packages in the conda environment
```
conda install pip
pip install -r requirements.txt
```

## Run Django Project Locally
You can use Pycharm and conda environment to run this project with the following steps:
- Open the project with Pycharm and set the project interpreter as the conda environment you created previously
- Click Tools, then click Run manage.py Task... 
- Input the following command to run the application locally (default port number is 8000)
```
runserver [port number]
``` 
If you would like to run the project on terminal, open your project to the right environment, then run the following command
```
python manage.py runserver [port number]
```

## Functionalities
### Regular User Pages
- User Management
  - Registration
  - Login/Logout
  - View/Update User Profile
  - Change Password
- Payment Method Management
  - Account
  - Bank
  - Card Information
- Transaction Management 
  - Send Money
  - Request Money
  - Incomplete Transaction
  - Activity (History Transactions)
  
### Staff User Pages
- User Management
  - User Account
  - User List
  - User Information/Transactions/Payment Method
- Transaction Management
  - Transaction List
  - Transaction Detail

## Other Information
- For more details include testing instructions, please check [Readme.pdf](https://github.com/gillian850413/Django_Virtual_Wallet/blob/master/chiang_pinhuey_final_project/README.pdf) 
- CSS Template: [Colorlib](https://colorlib.com)

