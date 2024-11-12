import phonenumbers
from phonenumbers import geocoder, carrier
import random
import time
import os
from colorama import init, Fore
#Made by TheZ
init(autoreset=True)


country_info = {
    "DE": {
        "name": "Germany",
        "area_codes": ['30', '40', '69', '89', '211', '201', '711', '621', '511', '231'],  
        "mobile_prefixes": ['151', '160', '170', '171', '172', '173'], 
        "country_code": '49',  
        "max_length": 11  
    },
    "US": {
        "name": "United States",
        "area_codes": ['212', '305', '415', '718', '323', '213'],
        "mobile_prefixes": ['310', '415', '212', '202', '323'], 
        "country_code": '1',  
        "max_length": 10  
    },
    "GB": {
        "name": "United Kingdom",
        "area_codes": ['20', '161', '131'],
        "mobile_prefixes": ['079', '078', '074'],  
        "country_code": '44', 
        "max_length": 10  
    }
}


def generate_phone_number(country_code, max_length, mobile_prefixes=None):
    if mobile_prefixes:
        region_prefix = random.choice(mobile_prefixes)  
    else:
        region_prefix = random.choice(country_info[country_code]["area_codes"])  
    
    remaining_digits = max_length - len(region_prefix) - len(country_code) - 1  
    if remaining_digits <= 0:
        return None  
    

    remaining_digits_str = ''.join(random.choices('0123456789', k=remaining_digits))
    
   
    return f"+{country_info[country_code]['country_code']} {region_prefix} {remaining_digits_str}"

def check_valid_phone_number(phone_number, country_code):
    try:
     
        parsed_number = phonenumbers.parse(phone_number, country_code)
        
        
        if phonenumbers.is_valid_number(parsed_number):
            return True
        else:
            return False
    except phonenumbers.NumberParseException:
        return False


def search_for_valid_numbers(country_code, duration, max_length=10, mobile_prefixes=None):
    print(f"Searching for valid phone numbers in {country_code}...\n")
    
    start_time = time.time()  
    valid_numbers = []
    invalid_numbers = []
    tested_numbers_count = 0  

    while True:
        
        full_number = generate_phone_number(country_code, max_length, mobile_prefixes)

        if full_number:
            
            is_valid = check_valid_phone_number(full_number, country_code)

            
            if is_valid:
                print(f"{Fore.GREEN}Valid: {full_number}")
                valid_numbers.append(full_number)
            else:
                print(f"{Fore.RED}Invalid: {full_number}")
                invalid_numbers.append(full_number)

           
            tested_numbers_count += 1

        
        elapsed_time = time.time() - start_time
        if elapsed_time >= duration:
            print(f"\nSearch stopped after {int(elapsed_time)} seconds. Total numbers tested: {tested_numbers_count}.")
            break
    
    return valid_numbers, invalid_numbers, tested_numbers_count


def save_valid_numbers_to_file(valid_numbers):
    
    script_directory = os.path.dirname(os.path.abspath(__file__))
    
   
    file_path = os.path.join(script_directory, "valid_numbers.txt")
    
  
    with open(file_path, 'w') as file:
        for number in valid_numbers:
            file.write(f"{number}\n")
    
    print(f"\nValid phone numbers saved to {file_path}")

def main():
    print("Welcome to the Phone Number Crawler! - TheZ\n")

    
    print("Select a country by its country code:")
    for code, info in country_info.items():
        print(f"{code}: {info['name']}")
    country_code = input("\nEnter the country code (e.g., 'DE' for Germany): ").strip().upper()

    if country_code not in country_info:
        print("Invalid country code.")
        return

   
    try:
        duration = int(input("Enter the duration for the search (in seconds): ").strip())
    except ValueError:
        print("Please enter a valid number for the duration.")
        return


    try:
        number_length = int(input("Enter the total length of the phone number (excluding country code, e.g., 11 for Germany): ").strip())
    except ValueError:
        print("Please enter a valid number for the phone number length.")
        return

    
    search_type = input("Do you want to search for mobile numbers (M), landlines (L), or both (B)? ").strip().upper()
    if search_type == 'M':
        mobile_prefixes = country_info[country_code]["mobile_prefixes"]
    elif search_type == 'L':
        mobile_prefixes = None  
    else:
        mobile_prefixes = country_info[country_code]["mobile_prefixes"] + country_info[country_code]["area_codes"]

   
    valid_numbers, invalid_numbers, tested_numbers_count = search_for_valid_numbers(
        country_code, duration, max_length=number_length, mobile_prefixes=mobile_prefixes)

    print(f"\nTotal numbers tested: {tested_numbers_count}")
    print(f"Valid numbers found: {len(valid_numbers)}")
    print(f"Invalid numbers found: {len(invalid_numbers)}")

   
    if valid_numbers:
        print("\nValid phone numbers found:")
        for number in valid_numbers:
            print(f"{Fore.GREEN}{number}")
        
      
        save_valid_numbers_to_file(valid_numbers)
        
    if invalid_numbers:
        print("\nInvalid phone numbers found:")
        for number in invalid_numbers:
            print(f"{Fore.RED}{number}")

if __name__ == "__main__":
    main()
# Made By TheZ
