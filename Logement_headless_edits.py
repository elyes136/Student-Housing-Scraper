from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
from colorama import Fore, Style
import re  # For regex matching
import discord  # For Discord bot
import asyncio  # For async operations
import os
from dotenv import load_dotenv
load_dotenv()

# 🔹 Website URL
URL = "https://trouverunlogement.lescrous.fr/"

# 🔹 Prompt for user input
CITY_NAME = input("Enter the city you want to search for: ")

# 🔹 Correct locators
SEARCH_BOX_SELECTOR = "input[class*='PlaceAutocomplete__input']"  # Search box
DROPDOWN_SELECTOR = "ul[role='listbox'] li"  # Dropdown options
SEARCH_BUTTON_SELECTOR = "button.fr-btn.svelte-w11odb"  # Search button
RESULTS_TITLE_SELECTOR = "h2.SearchResults-mobile.svelte-8mr8g"  # Results title

# 🔹 House listing locators
HOUSE_ITEM_SELECTOR = "li.fr-col-12.fr-col-sm-6.fr-col-md-4.svelte-11sc5my"  # House items
HOUSE_NAME_SELECTOR = "a[href^='/tools']"  # House name
HOUSE_ADDRESS_SELECTOR = "p.fr-card__desc"  # House address
HOUSE_SURFACE_SELECTOR = ".//p[contains(@class, 'fr-card__detail')]"  # House surface (relative XPath)
HOUSE_PRICE_SELECTOR = ".//p[contains(@class, 'fr-badge')]"  # House price (relative XPath)

# 🔹 Set up ChromeOptions for headless mode
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-blink-features=AutomationControlled")

# 🔹 Discord Bot Configuration
DISCORD_TOKEN =  os.getenv("DISCORD_TOKEN")  # Replace with your bot token
CHANNEL_ID = 1333027105591660564  # Replace with your Discord channel ID

# Initialize Discord bot
intents = discord.Intents.default()
client = discord.Client(intents=intents)
def search_city(city):
    """Search for houses in the specified city and return results."""
    driver = webdriver.Chrome(options=options)
    try:
        print(Fore.YELLOW + "🌐 Opening the website..." + Style.RESET_ALL)
        driver.get(URL)
        
        # Wait for search box and type city name
        search_box = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, SEARCH_BOX_SELECTOR))
        )
        search_box.clear()
        search_box.send_keys(city)
        time.sleep(2)  # Allow dropdown to appear

        # Select city from dropdown
        dropdown_options = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, DROPDOWN_SELECTOR))
        )
        for option in dropdown_options:
            if city.lower() in option.text.lower():
                option.click()
                break
        time.sleep(2)

        # Click search button
        search_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, SEARCH_BUTTON_SELECTOR))
        )
        search_button.click()

        # Wait for search results to load
        print(Fore.YELLOW + "⏳ Waiting for search results..." + Style.RESET_ALL)
        try:
            # Wait for the results title to appear
            results_title = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, RESULTS_TITLE_SELECTOR))
            )
            title_text = results_title.text.strip()
            # Check if no houses were found
            if title_text == "Aucun logement trouvé":
                print(Fore.RED + f"🏠 I found 0 houses." + Style.RESET_ALL)
                return set()  # No listings found

            print(Fore.GREEN + "✅ Search results loaded!" + Style.RESET_ALL)

            # Wait for the house listings to load
            print(Fore.YELLOW + "🔍 Waiting for house listings..." + Style.RESET_ALL)
            listings_elements = WebDriverWait(driver, 30).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, HOUSE_ITEM_SELECTOR))
            )
            print(Fore.GREEN + f"✅ Found {len(listings_elements)} house listings!" + Style.RESET_ALL)

            # Extract and print house details
            for house in listings_elements:
                try:
                    # Extract house name
                    house_name = house.find_element(By.CSS_SELECTOR, HOUSE_NAME_SELECTOR).text.strip()
                    # Extract house address
                    house_address = house.find_element(By.CSS_SELECTOR, HOUSE_ADDRESS_SELECTOR).text.strip()
                    # Extract house surface
                    surface = house.find_element(By.XPATH, HOUSE_SURFACE_SELECTOR).text.strip()
                    surface_match = re.search(r"(\d+,\d+) m²", surface)
                    if surface_match:
                        surface_formatted = surface_match.group(1).replace(",", ".")  # Format surface
                    else:
                        surface_formatted = "N/A"  # Handle missing or unexpected surface format
                    # Extract house price
                    price = house.find_element(By.XPATH, HOUSE_PRICE_SELECTOR).text.strip()
                    price_match = re.search(r"(\d+,\d+) €", price)
                    if price_match:
                        price_formatted = price_match.group(1).replace(",", ".")  # Format price
                    else:
                        price_formatted = "N/A"  # Handle missing or unexpected price format
                    
                    # Print house details
                    print(Fore.GREEN + f"🏠 House Name: {house_name}" + Style.RESET_ALL)
                    print(Fore.BLUE + f"📍 Address: {house_address}" + Style.RESET_ALL)
                    print(Fore.CYAN + f"📐 Surface: {surface_formatted} m² (Raw: {surface})" + Style.RESET_ALL)
                    print(Fore.MAGENTA + f"💰 Price: {price_formatted} € (Raw: {price})" + Style.RESET_ALL)
                    print("-" * 50)
                except NoSuchElementException:
                    print(Fore.RED + "❌ Could not extract house details." + Style.RESET_ALL)
                    continue

            # Send Discord notification if houses are found
            if listings_elements:
                return True

            return listings_elements
        except TimeoutException:
            print(Fore.RED + "❌ House listings did not load within the expected time." + Style.RESET_ALL)
            print(Fore.RED + f"🏠 I found 0 houses." + Style.RESET_ALL)
            return set()  # No listings found

    except (NoSuchElementException, TimeoutException) as e:
        print(Fore.RED + f"❌ An error occurred: {e}" + Style.RESET_ALL)
        print(Fore.RED + f"🏠 I found 0 houses." + Style.RESET_ALL)
        return set()
    finally:
        # Close the browser after each iteration
        driver.quit()

# Main loop to retry every 10 minutes
# Discord bot event
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    channel = client.get_channel(CHANNEL_ID)

    while True:
        if search_city(CITY_NAME):  # Check if the condition is met
            print("Fama dyar weee") 
            await channel.send(f'@here 🏠 Fama dyar weeeeeeeeee ejri f {CITY_NAME}')
            #await asyncio.sleep(150)
            #break  # Stop after sending the message (or remove this to keep monitoring)
        else:
            print(Fore.BLUE+"Condition not met. Checking again in 10 minutes ...")
        await asyncio.sleep(300)  # Wait 5 minutes before checking again
        #channel = client.get_channel(CHANNEL_ID)
# Run the bot
client.run(DISCORD_TOKEN)