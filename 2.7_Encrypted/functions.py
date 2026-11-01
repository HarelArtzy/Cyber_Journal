"""
Author: Harel Teva Artzy

Program name: Socket Client

Description: Connects to a server and sends it commands, it then receives the answers from the server and prints them.

Date: 27/10/2025
"""


import os
import glob
import shutil
import subprocess


VALID_COMMANDS = {"DIR", "DELETE", "COPY", "EXECUTE", "SCREENSHOT", "EXIT"}


def cmd_dir(sent_dir):
    """
    A function that receives a directory and returns its contents.
    :param sent_dir:
    :return files_list/error:
    """
    if not os.path.isdir(sent_dir):
        return "Directory not found".encode()

    files_list = glob.glob(os.path.join(sent_dir, "*"))
    files_list = "\n".join(files_list)
    return files_list.encode()



def cmd_delete(sent_file):
    """
    A function that receives a file and deletes it.
    :param sent_file:
    :return a string that says the file was deleted:
    """
    try:
        os.remove(sent_file)
        return f"Deleted {sent_file}".encode()
    except Exception as e:
        return f"Error deleting {sent_file}: {e}".encode()


def cmd_copy(sent_files):
    """
    A function that receives 2 files and copies one to the other.
    :param sent_files:
    :return a string that says the first file was copied into the second file:
    """
    try:
        if " " in sent_files:
            return f"Please send the command in the following format: COPY file1,file2".encode()
        sent_files = sent_files.split(",")
        shutil.copyfile(sent_files[0], sent_files[1])
        return f"Copied {sent_files[0]} into {sent_files[1]}".encode()
    except Exception as e:
        return f"Error occurred: {e}".encode()



def cmd_execute(sent_file):
    """
    A function that receives a file and executes it.
    :param sent_file:
    :return a string that says the file was executed:
    """
    try:
        subprocess.call(sent_file)
        return f"Executed '{sent_file}'.".encode()
    except Exception as e:
        return f"Error executing '{sent_file}': {e}".encode()


def cmd_screenshot(data): #ask nir if ok
    """
    A function that saves a screenshot of the server's screen and sends it over to the client.
    :param data:
    :return a byte string of the screenshot's data:
    """
    import pyautogui
    path = r'C:\Users\artzy\PycharmProjects\PythonProject5\Cyber_2.7\screen.jpg'
    image = pyautogui.screenshot()
    image.save(path)
    with open(path, "rb") as f:
        screen_data = f.read()
    return screen_data


def is_valid(request: str) -> bool:
    """
    A function that checks whether a request is valid.
    :param request:
    :return True if the request is valid, False otherwise:
    """
    if request in VALID_COMMANDS:
        return True
    return False


if __name__ == "__main__":
    assert is_valid("DIR") == True
    assert is_valid("DELETE") == True
    assert is_valid("COPY") == True
    assert is_valid("EXECUTE") == True
    assert is_valid("SCREENSHOT") == True
    assert is_valid("EXIT") == True
    assert is_valid("BLABLA") == False
