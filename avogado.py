from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import requests
import time


# URL of the page
url = 'https://www.avogado6.com/'

# Set up Chrome options for headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")

# Set up the Selenium WebDriver
driver = webdriver.Chrome(options=chrome_options)
driver.get(url)

# Wait for the page to load
time.sleep(5)  # Adjust time as necessary

# Find the first 'matrix-gallery-items-container' and click on it
try:
    # Find the first 'matrix-gallery-items-container'
    gallery_container = driver.find_element(By.XPATH, "//div[@data-testid='matrix-gallery-items-container']")
    
    # Find the first item within the container
    gallery_item = gallery_container.find_element(By.XPATH, ".//div[@data-testid='gallery-item-item']")
    
    # Find the clickable button within the item and click it
    click_action_button = gallery_item.find_element(By.XPATH, ".//div[@data-testid='gallery-item-click-action-image-zoom'][@role='button']")
    click_action_button.click()

    # Wait for the high-resolution image link to appear
    time.sleep(5)  # Adjust time as necessary

    # Extract the high-resolution image URL
    wow_image = driver.find_element(By.ID, 'img_imageZoomComp_0')
    high_res_image_url = wow_image.get_attribute('data-src')

    # Download the image
    response = requests.get(high_res_image_url)
    if response.status_code == 200:
        #with open('/Users/work/art.jpg', 'wb') as file:
        with open('latest_image.jpg', 'wb') as file:
            file.write(response.content)
    else:
        print("Failed to download the image.")

except NoSuchElementException:
    print("No gallery items found or element not located.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the browser
    driver.quit()




# Function to convert the image to ASCII
def image_to_ascii(image_path, output_file):
    # ASCII characters used to build the output text
    ASCII_CHARS = "@%#*+=-:. "
    # Load the image
    try:
        image = Image.open(image_path)
    except Exception as e:
        print(f"Unable to open image: {e}")
        return

    # Resize the image
    width, height = image.size
    aspect_ratio = height/float(width)
    new_width = 80
    new_height = int(aspect_ratio * new_width * 0.55)
    image = image.resize((new_width, new_height))

    # Convert the image to grayscale
    image = image.convert('L')

    # Convert each pixel to an ASCII character
    pixels = image.getdata()
    ascii_str = ''
    for pixel in pixels:
        ascii_str += ASCII_CHARS[pixel//25]

    # Split the string based on width
    img_ascii = [ascii_str[i:i+new_width] for i in range(0, len(ascii_str), new_width)]
    ascii_str = "\n".join(img_ascii)

    # Write to a text file
    with open(output_file, 'w') as f:
        f.write(ascii_str)

# Example usage
image_path = 'latest_image.jpg'  # Path to your downloaded image
output_file = '/Users/work/ascii_art.txt'    # Output file
image_to_ascii(image_path, output_file)