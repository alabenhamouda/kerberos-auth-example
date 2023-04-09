#!/usr/bin/python3
from KerberosClient import KerberosClient

krb = KerberosClient("host@kdc.insat.tn")
SERVER_URL = 'http://kdc.insat.tn:5000'
RED = "\033[31m"
RESET = "\033[0m"


def output_in_red(msg):
    print(RED + msg + RESET)


def handle_response(response):
    if response is None:
        output_in_red(
            "Something went wrong, please check your kerberos ticket!")
    elif response.status_code == 200:
        output_in_red(response.content.decode("utf-8"))
    else:
        print(
            f'Error {response.status_code}: {response.content.decode("utf-8")}')


def menu():
    """Display a menu to the user and get their choice."""
    print('1. List content of a directory')
    print('2. Read a file')
    print('3. Upload a file')
    print('4. Quit')
    choice = input('Enter your choice (1/2/3/4): ')
    return choice


def list_directory_content():
    """List the content of a directory on the Flask server."""
    directory_path = input('Enter the directory path: ')
    data = {"path": directory_path}
    response = krb.post(
        f"{SERVER_URL}/directory", data)
    handle_response(response)


def read_file():
    """Read a file on the Flask server."""
    file_path = input('Enter the file path: ')
    data = {"file_path": file_path}
    response = krb.post(
        f"{SERVER_URL}/read_file", data)
    handle_response(response)


def upload_file():
    """Upload a file to the Flask server."""
    file_path = input('Enter the file path to upload: ')
    destination_path = input('Enter the destination path: ')
    response = krb.upload_file(
        f'{SERVER_URL}/upload', file_path, destination_path)
    handle_response(response)


def main():
    while True:
        choice = menu()
        if choice == '1':
            list_directory_content()
        elif choice == '2':
            read_file()
        elif choice == '3':
            upload_file()
        elif choice == '4':
            break
        else:
            print('Invalid choice. Please try again.')


if __name__ == '__main__':
    main()
