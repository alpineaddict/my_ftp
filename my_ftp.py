#!/usr/bin/env python

'''
Small FTP program used for testing to upload and download files.
Specifically designed to work with speedtest.tele2.net.
'''

import ftplib
import os
import sys
from pyinputplus import inputNum, inputYesNo
import constant


def user_welcome():
    '''
    Welcome user and present FTP information.
    '''

    print("=" * 11 + " My_FTP " + "=" * 11)
    print("      Welcome to My_FTP.")
    print("My_FTP is an FTP program that can be used to \n"
            "upload and download files from a test FTP server.")
    print("My_FTP cannot delete any files from test FTP server.")
    print("=" * 10 + " CONSTANTS " + "=" * 10)
    print("Username: anonymous")
    print("Passowrd: a")
    print("FTP Server: speedtest.tele2.net")
    print("=" * 30)

def item_menu(ftp_connection):
    '''
    Prompt user with an item menu and issue class functions accordingly.
    Promp user for choice to re-run through file upload/download again.
    '''
    while True:
        print("=" * 12 + " MENU " + "=" * 12)
        print("Please choose an option from the menu:")
        print("1) Upload")
        print("2) Download")
        print("3) Exit program")
        choice = inputNum(prompt="Option: ", min=1, max=3)
        if choice == 1:
            while True:
                ftp_connection.upload_prompt()
                ftp_connection.upload_file()
                retry_upload = inputYesNo(prompt="Upload another? ")
                if 'yes' in retry_upload:
                    continue
                else:
                    break
            continue
        elif choice == 2:
            while True:
                ftp_connection.download_prompt()
                ftp_connection.download_file()
                retry_download = inputYesNo(prompt="Download another? ")
                if 'yes' in retry_download:
                    continue
                else:
                    break
            continue
        else:
            print("Exiting program. Goodbye!")
            sys.exit()

class MyFTP():
    '''
    Build out an FTP object to interact with FTP server at speedtest.tele2.net
    MyFTP object can upload local files and/or download files locally.
    '''

    def __init__(self, FTP_SERVER, USERNAME, PASSWORD):
        self.FTP_SERVER = FTP_SERVER
        self.USERNAME   = USERNAME
        self.PASSWORD   = PASSWORD

        try:
            print("Attempting to connect to FTP server...")
            self.ftp_object = ftplib.FTP(FTP_SERVER)
            self.login = self.ftp_object.login(self.USERNAME, self.PASSWORD)
            print("Status: " + self.login)
        except ftplib.all_errors as e:
            error_code_string = str(e)
            print(error_code_string)
            print("Terminating program. Goodbye!")
            sys.exit()

    def directory_exist_check(self, local_file_path):
        '''
        Check to see whether or not directory exists. Return bool val
        for condition. Will be used to determine whether or not to proceed
        to file upload or download.
        '''
        self.local_file_path = local_file_path
        if os.path.exists(self.local_file_path):
            return True

    def upload_prompt(self):
        '''
        Prompt user for information needed for FTP file upload.
        '''

        print("=" * 11 + " UPLOAD " + "=" * 11)
        print("FTP REQUIREMENTS:")
        print(" - Files will be uploaded to /upload/ directory.")
        print(" - New folders cannot be created.")
        self.ftp_object.cwd("/upload")
        self.local_file_path = input("Full file path (Local): ")
        self.new_file_name = input("New file name (Ex: lines.txt): ")

    def upload_file(self):
        '''
        Attempt to upload file to FTP.
        '''
        if self.directory_exist_check(self.local_file_path):
            try:
                print("Attempting file upload...")
                with open(self.local_file_path,'rb') as fh:
                    self.file_upload = self.ftp_object.storbinary(
                        "STOR " + self.new_file_name, fh)
                    if "Transfer complete" in self.file_upload:
                        print("File uploaded successfully!")
                        print("Status: " + self.file_upload)
                    else:
                        print("Sorry, upload failed. Try again.")
                        print(self.file_upload)
            except ftplib.all_errors as e:
                error_code_string = str(e)
                print(error_code_string)
        else:
            print("ERROR! Path does not exist locally.")

    def download_prompt(self):
        '''
        Prompt user for information needed for FTP file download.
        '''

        print("=" * 10 + " DOWNLOAD " + "=" * 10)
        self.ftp_object.cwd('/')
        print("Please specify file to download, local target directory and new"
            " filename.")
        print("Current directory: /")
        print("Please review contents of root directory for file to download.")
        self.ftp_object.retrlines("LIST")
        self.download_file_name = input("File name to download: ")
        self.local_file_path = input("Target local directory: ")
        if self.local_file_path[-1] != "/":
            self.local_file_path += "/"
        self.new_file_name = input("New file name (Ex: newLines.txt): ")
        self.new_file_name = self.local_file_path + self.new_file_name

    def download_file(self):
        '''
        Attempt to download file from FTP to local repository.
        '''
        if self.directory_exist_check(self.local_file_path):
            try:
                print("Attempting file download...")
                with open(self.new_file_name,"wb") as fh:
                    self.file_download = self.ftp_object.retrbinary(
                        "RETR " + self.download_file_name, fh.write)
                    if "Transfer complete" in self.file_download:
                        print("Download successful!")
                        print("Status: " + self.file_download)
                    else:
                        print("Sorry, download failed. Try again.")
                        print(self.file_download)
            except ftplib.all_errors as e:
                error_code_string = str(e)
                print(error_code_string)
        else:
            print("ERROR! Path does not exist locally.")

if __name__ == "__main__":
    user_welcome()
    my_ftp_connection = MyFTP(
        constant.FTP_SERVER,
        constant.USERNAME,
        constant.PASSWORD)
    item_menu(my_ftp_connection)
