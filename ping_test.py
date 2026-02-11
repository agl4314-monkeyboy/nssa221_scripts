#!/usr/bin/python3

# Adam Levin 01/28/2026

# imports
import subprocess
import re

# globals
ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
ping_domain_local = '129.21.3.17'
ping_domain_remote = '8.8.8.8'
dns_domain = 'www.google.com'

# menu function to print
def menu() -> int:
    try:
        option = int(input('''
1. Display the default gateway
2. Test Local Connectivity
3. Test Remote Connectivity
4. Test DNS Resolution
5. Exit/quit the script\n>> '''))
    except:
        return 0
    if (option < 1 or option > 5):
        return 0
    else:
        return option

def get_gateway() -> str:
    # use check_output since we only need to read output and not run complex commands
    # universal tells to treat output as string
    output = subprocess.check_output(['ip', 'r'],universal_newlines=True)
    return re.search(ip_pattern, output)[0]

# helper function to test ping RIT router ip
def ping_test_local() -> str:
    output = subprocess.check_output(['ping', '-c', '4', ping_domain_local],universal_newlines=True)
    return output

# helper function to test ping remote ip
def ping_test_remote() -> str:
    output = subprocess.check_output(['ping', '-c', '4', ping_domain_remote],universal_newlines=True)
    return output


# helper function to test dns resolution
def dns_test() -> str:
    output = subprocess.check_output(['dig', dns_domain],universal_newlines=True)
    return output

# clear terminal then run a while loop to get user inputs
def main():
    print("\033c", end="") # clear terminal
    option = menu()
    while option != 5:
        if option == 1:
            print(f'\n{get_gateway()}\n')
        elif option == 2:
            print(f'\n{ping_test_local()}\n')
        elif option == 3:
            print(f'\n{ping_test_remote()}\n')
        elif option == 4:
            print(f'\n{dns_test()}\n')
        elif option == 5:
            exit()
        else:
            # invalid input handling
            print('invalid option')
        option = menu()



    




if __name__ == "__main__":
    main()