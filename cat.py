import requests
from tabulate import tabulate
from colorama import Fore, Style

# Function to read all authorization tokens from query.txt
def get_authorization_tokens():
    with open('query.txt', 'r') as file:
        return [line.strip() for line in file if line.strip()]

# Function to set headers with the provided token
def get_headers(token):
    return {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "authorization": f"tma {token}",
        "content-type": "application/json",
        "priority": "u=1, i",
        "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Microsoft Edge\";v=\"127\", \"Chromium\";v=\"127\", \"Microsoft Edge WebView2\";v=\"127\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "Referer": "https://cats-frontend.tgapps.store/",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }

def fetch_tasks(headers):
    url = "https://cats-backend-wkejfn-production.up.railway.app/tasks/user?group=cats"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def clear_task(task_id, headers):
    url = f"https://cats-backend-wkejfn-production.up.railway.app/tasks/{task_id}/complete"
    response = requests.post(url, headers=headers, json={})
    
    if response.status_code == 200:
        print(Fore.GREEN + f"Task {task_id} successfully marked as completed.")
        return response.json()
    else:
        print(Fore.RED + f"Failed to mark task {task_id} as completed.")
        response.raise_for_status()
        
def print_welcome_message():
    print(Fore.WHITE + r"""
       
ooooooooooooo oooooooooooo   .oooooo.    ooooo     ooo ooooo   ooooo
8'   888   `8 `888'     `8  d8P'  `Y8b   `888'     `8' `888'   `888'
     888       888         888            888       8   888     888 
     888       888oooo8    888            888       8   888ooooo888 
     888       888    "    888     ooooo  888       8   888     888 
     888       888       o `88.    .88'   `88.    .8'   888     888 
    o888o     o888ooooood8  `Y8bood8P'      `YbodP'    o888o   o888o
                                                                    
                                                                    
                                                                    
  .oooooo.          .o.       ooooo      ooo oooo    oooo           
 d8P'  `Y8b        .888.      `888b.     `8' `888   .8P'            
888               .8"888.      8 `88b.    8   888  d8'              
888              .8' `888.     8   `88b.  8   88888[                
888     ooooo   .88ooo8888.    8     `88b.8   888`88b.              
`88.    .88'   .8'     `888.   8       `888   888  `88b.            
 `Y8bood8P'   o88o     o8888o o8o        `8  o888o  o888o            
          """)
    print(Fore.BLUE + Style.BRIGHT + "CATSGANG BY TEGUHGANK")
    print(Fore.YELLOW + Style.BRIGHT + "TEGUH GANK")
    print(Fore.GREEN + Style.BRIGHT + "DONASI DONG BANG :) 089619642255 GOPAY ")
    print(Fore.BLUE + Style.BRIGHT + "TEGUHGANK :)\n\n")        

def complete_all_tasks():
    tokens = get_authorization_tokens()
    
    confirmation = input(Fore.WHITE + f"Apakah Anda ingin menyelesaikan semua task? (y/n): ").strip().lower()
    if confirmation != 'y':
        return
    
    for token in tokens:
        headers = get_headers(token)
        tasks = fetch_tasks(headers).get('tasks', [])
        
        for task in tasks:
            if not task['completed']:
                try:
                    clear_task(task['id'], headers)
                except requests.RequestException:
                    # Handle any request exception and move on to the next task
                    print(Fore.WHITE + f"Skipping task {task['id']} due to an error.")

def user():
    tokens = get_authorization_tokens()
    all_user_data = []
    total_rewards_sum = 0
    
    for token in tokens:
        headers = get_headers(token)
        url = "https://cats-backend-wkejfn-production.up.railway.app/user"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            # Extract required fields
            first_name = data.get('firstName')
            last_name = data.get('lastName')
            telegram_age = data.get('telegramAge')
            total_rewards = data.get('totalRewards')
            
            # Collect user data
            all_user_data.append([first_name, last_name, telegram_age, total_rewards])
            total_rewards_sum += total_rewards  # Accumulate total rewards
        else:
            print(Fore.RED + f"Failed to fetch user data for token {token}.")
            response.raise_for_status()
    
    # Prepare data for tabulate
    table_data = [
        ["First Name", "Last Name", "Telegram Age", "Total Rewards"]
    ]
    table_data.extend(all_user_data)
    
    # Print table
    print(tabulate(table_data, headers='firstrow', tablefmt='grid'))
    
    # Print total rewards sum with color
    print(Fore.GREEN + f"\nTotal Rewards: " + Fore.WHITE + f"{total_rewards_sum}" + Style.RESET_ALL)

def main():
    print_welcome_message()
    complete_all_tasks()
    print(Fore.WHITE + f"\nDisplaying user information...")
    user()

# Example usage
if __name__ == "__main__":
    main()
