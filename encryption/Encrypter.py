from cryptography.fernet import Fernet, InvalidToken
from colorama import Fore
import time


# Colors for massages
def red(text: str):return Fore.RED + text + Fore.RESET
def green(text: str): return Fore.GREEN + text + Fore.RESET
def cyan(text: str): return Fore.CYAN + text + Fore.RESET
def magenta(text: str): return Fore.MAGENTA + text + Fore.RESET
def yellow(text: str): return Fore.YELLOW + text + Fore.RESET


# Application class
class Encrypter:
    def __init__(self):
        self.key = None

    def load_an_existing_key(self, path):
        if path.endswith('.key'):
            with open(path, 'r') as f:
                self.key = f.read()
            print(f"The submitted key: {magenta(self.key)}")
        else:
            print(red("Invalid path for key"))

    def create_a_new_key(self, path):
        self.key = Fernet.generate_key()
        if path.endswith(".key"):
            with open(f"{path}", 'wb') as key_file:
                key_file.write(self.key)
            print(f"The generated key: {magenta(str(self.key))}")
            print("Saved as", path)
        else:
            print(red("Invalid path for key"))

    def encrypt_a_file(self, path):
        try:
            fernet = Fernet(self.key)
            with open(path, 'r') as f:
                content = f.read()
                encrypted_content = fernet.encrypt(bytes(content, "utf-8"))
            with open(path + ".encrypted", 'wb') as encrypted_file:
                encrypted_file.write(encrypted_content)
        except FileNotFoundError:
                if not path.endswith(".txt"):
                    print(red("Invalid file for encryption"))
                else:
                    print(red("File not found"))
        except TypeError:
            print(red("Key is none"))


    def decrypt_an_encrypted_file(self, path):
        try:
            fernet = Fernet(self.key)
            with open(path, 'r') as f:
                encrypted_content = f.read()
                decrypted_content = fernet.decrypt(bytes(encrypted_content, "utf-8"))
            with open(path + ".decrypted", 'wb') as decrypted_file:
                decrypted_file.write(decrypted_content)
        except FileNotFoundError:
            if not path.endswith(".txt.encrypted"):
                print(red("Invalid file for decryption"))
            else:
                print(red("File not found"))
        except InvalidToken:
            print(red("Invalid key for token"))
        except TypeError:
            print(red("Key is none"))

    def get_current_key(self):
        return str(self.key)


# Main function to handle user's choice
def main():
    encrypter = Encrypter()
    done = False
    while not done:
        print(f"\n({cyan('1')}) Load an existing key\n"
              f"({cyan('2')}) Create a new key\n"
              f"({cyan('3')}) Encrypt a file\n"
              f"({cyan('4')}) Decrypt an encrypted file\n"
              f"({cyan('5')}) Get the current key\n"
              f"({cyan('q')}) Quit")
        
        choice = input("What would you like to do?\t")
        if choice == 'q':  # Quit
            print(f"[{green('Quit')}]")
            done = True
        elif choice == '1':  # Load an existing key
            print(f"[{green('Load an existing key')}]")
            path = input("Enter the path to your key: ")
            encrypter.load_an_existing_key(path)

        elif choice == '2':  # Create a new key
            print(f"[{green('Create a new key')}]")
            path = input("Enter the path to for your new key: ")
            encrypter.create_a_new_key(path)

        elif choice == '3':  # Encrypt a file
            print(f"[{green('Encrypt a file')}]")
            print(yellow("Before encrypting a file, please make sure that your key is loaded and saved.\n"
                      "Otherwise, decryption of the file without the matching key won't be available."))
            answer = input(f"Would you like to proceed?[{cyan('Y/N')}] ")
            if answer == 'Y' or answer == 'y':
                path = input("Enter the path to the file: ")
                encrypter.encrypt_a_file(path)
            elif answer == 'N' or answer == 'n':
                print("Canceled")
            else:
                print(red("Invalid response"))

        elif choice == '4':  # Decrypt an encrypted file
            print(f"[{green('Decrypt an encrypted file')}]")
            print(yellow("Before decrypting the file, please make sure that the matching key is loaded.\n"
                      "Otherwise, the results of the decryption might not be valid."))
            answer = input(f"Would you like to proceed?[{cyan('Y/N')}] ")
            if answer == 'Y' or answer == 'y':
                path = input("Enter the path to the file: ")
                encrypter.decrypt_an_encrypted_file(path)
            elif answer == 'N' or answer == 'n':
                print("Canceled")
            else:
                print(red("Invalid response"))
        elif choice == '5':  # Get the current key
            print(f"[{green('Get the current key')}]")
            print(f"The current key: {magenta(encrypter.get_current_key())}")
        else:
            print(red("Invalid choice, please try again."))
        
        time.sleep(1.5)


# Run the application
if __name__ == '__main__':
    main()
