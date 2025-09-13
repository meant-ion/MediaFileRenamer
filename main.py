import os
import pathlib
from time import localtime, strftime

flashdrive_dir = pathlib.Path("G:/Grandma Flashdrives")


def file_exists(file):
    for dirpath, dirnames, filenames in os.walk(flashdrive_dir):
        if file in filenames:
            return True
    return False


file_extensions = ['.jpg', '.png', '.jpeg', '.bmp', '.avi', '.wma', '.mp4', '.wmv', '.3gp', '.mov']

# last character to look for when renaming a file
last_file_path_char = '\\'

for item in flashdrive_dir.rglob("*"):
    if item.is_file():
        file_tuple = os.path.splitext(item)
        file_ext = file_tuple[1]
        if file_ext.lower() in file_extensions:
            file_info = os.stat(item)
            actual_create_time = localtime(file_info.st_mtime)
            # month-day-year mil_hour:min:sec
            new_file_name = strftime("%m-%d-%Y %H_%M_%S", actual_create_time)
            file_name_index = file_tuple[0].rfind(last_file_path_char)
            if file_name_index != -1:
                # for duplicate checking
                new_filename = new_file_name + file_ext.lower()
                full_filename = file_tuple[0][:file_name_index] + "\\" + new_file_name + file_ext.lower()
                # Just in case a file was created at the exact same time as another in the directory
                copy_num = 1
                while file_exists(new_filename):
                    new_filename = new_file_name + "-" + str(copy_num) + file_ext.lower()
                    full_filename = file_tuple[0][:file_name_index] + "\\" + new_file_name + "-" + str(
                        copy_num) + file_ext.lower()
                    copy_num += 1
                    print("Had to add num to file from it existing already, renaming to: " + full_filename)
                print("New filename: " + full_filename)
                print("Old filename: " + str(item))
                os.rename(item, full_filename)
