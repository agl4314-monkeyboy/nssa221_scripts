#!/usr/bin/env python3
# Student: Adam Levin
# Current Date: 04/09/2026
# Due Date: 04/10/2026
# Class: NSSA 221 Section 03
# Assignement: Script 3


import os
from pathlib import Path
import sys
import time

# display header banner
def print_header(title="Shortcut Creater"):
    print("\n\t" + "*" * 48)
    print(f"\t*************** {title} ***************")
    print("\t" + "*" * 48 + "\n")

# simulate a progress bar for better user experience
def progress_bar(message="Processing"):
    print(f"{message}, please wait...\n")
    print("[====================] 100%\n")
    time.sleep(0.2)  # simulate small wait

# find the user's desktop path dynamically
def get_desktop():
    return Path.home() / "Desktop"

# recursively search for all files named `filename` starting from `start_dir`
def find_all_files(filename, start_dir="/"):
    matches = []
    for root, dirs, files in os.walk(start_dir):
        # Skip directories we can't access
        try:
            if filename in files:
                full_path = os.path.join(root, filename)
                matches.append(full_path)
        except PermissionError:
            continue  # skip directories without permission
    return matches

# main function to create a shortcut
def create_shortcut():
    user_input = input("Please enter the file name or full path to create a shortcut: ").strip()
    
    # search the entire system for this filename
    print("Searching the system, please wait...")
    progress_bar()
    found_files = find_all_files(user_input)
    
    # if file not found
    if not found_files:
        print(f"Sorry, couldn't find {user_input}!")
        return
    
    # multiple files found, list them and let the user choose which one to use
    if len(found_files) > 1:
        print(f"Multiple files with the name '{user_input}' were found:")
        for idx, f in enumerate(found_files, 1):
            print(f"[{idx}] {f}")
        while True:
            choice = input(f"Select the file you want to create a shortcut for (1-{len(found_files)}): ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(found_files):
                target_file = Path(found_files[int(choice) - 1])
                break
            else:
                print("Invalid selection. Please try again.")
    # otherwise continue with the single found file
    else:
        target_file = Path(found_files[0])
        confirm = input(f"Found {target_file}. Select Y/y to create shortcut: ").strip().lower()
        if confirm != 'y':
            print("Shortcut creation canceled.")
            return

    # create the symbolic link on Desktop
    shortcut_path = get_desktop() / target_file.name
    # error handling in case it already exists
    if shortcut_path.exists():
        print(f"Error: A file or shortcut named '{target_file.name}' already exists on your Desktop.")
        return

    # print out some pretty user interaction
    progress_bar("Creating Shortcut")
    try:
        shortcut_path.symlink_to(target_file)
        print("Shortcut created. Returning to Main Menu.")
    except Exception as e:
        print(f"Error creating shortcut: {e}")

# main function to delete a shortcut
def delete_shortcut():
    # find all symbolic links on the desktop
    desktop = get_desktop()
    symlinks = [f for f in desktop.iterdir() if f.is_symlink()]
    if not symlinks:
        print("No shortcuts found on your Desktop.")
        return
    # get the name of the shortcut to delete from the user
    shortcut_name = input("Please enter the shortcut/link to remove: ").strip()
    shortcut_path = desktop / shortcut_name
    print("Searching, please wait...")
    progress_bar()
    
    # error handling for invalid name
    if not os.path.lexists(shortcut_path) or not shortcut_path.is_symlink():
        print(f"Sorry, couldn't find {shortcut_name}!")
        return

    # confirm with the user
    confirm = input(f"Are you sure you want remove {shortcut_name}? Press Y/y to confirm: ").strip().lower()
    if confirm != 'y':
        print("Shortcut deletion canceled.")
        return
    
    # delete the symbolic link
    progress_bar("Removing link")
    try:
        shortcut_path.unlink()
        print("Link removed, returning to Main Menu.")
    except Exception as e:
        print(f"Error removing link: {e}")

# main function to report all shortcuts on the desktop
def report_shortcuts():
    # find all symbolic links on the desktop
    desktop = get_desktop()
    symlinks = [f for f in desktop.iterdir() if f.is_symlink()]
    progress_bar("Generating Report")

    # print out the report in a nice format
    print_header("Shortcut  Report")
    print(f"You current directory is {Path.home()}.")
    print(f"\nThe number of links is {len(symlinks)}.\n")
    print(f"{'Symbolic Link':<16}\t{'Target Path'}")
    for link in symlinks:
        print(f"{link.name:<16}\t{os.readlink(link)}")
    
    # interact with the user to return to the main menu or delete a link(convenient)
    choice = input("\nTo return to the Main Menu, press Enter. Or select R/r to remove a link: ").strip().lower()
    if choice == 'r':
        delete_shortcut()

# main menu function to display options and handle user input
def main_menu():
    while True:
        # print menu
        print_header()
        print("Enter Selection:\n")
        print("\t1 - Create a shortcut in your home directory.")
        print("\t2 - Remove a shortcut from your home directory.")
        print("\t3 - Run shortcut report.\n")
        choice = input('Please enter a number (1-3) or "Q/q" to quit the program.\t').strip().lower()
        
        # handle user input and call the appropriate function
        if choice == '1':
            create_shortcut()
        elif choice == '2':
            delete_shortcut()
        elif choice == '3':
            report_shortcuts()
        elif choice == 'q':
            print("\nQuiting program: returning to terminal.\n")
            print("Have a wonderful day!")
            sys.exit(0)
        else:
            print("\nYou entered an invalid option!\n")
            print("Please select a number between 1 through 3.")

if __name__ == "__main__":
    # clear the terminal
    print("\033c", end="")
    main_menu()