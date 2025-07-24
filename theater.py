import sys
import time
from bs4 import BeautifulSoup
import requests
import base64
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# Create a session to handle cookies automatically
session = requests.Session()

BASE_URL = "https://mrt.gt4it.com"

# Mapping of show time values to all possible Arabic day names
DAYS_OF_WEEK = {
    1: ["الاحد", "الأحد", "اﻷحد", "الاحاد", "اﻷحاد"],
    2: ["الإثنين", "الاثنين", "اﻹثنين", "الثنين", "إثنين", "اثنين"],
    3: ["الثلاثاء", "ثلاثاء", "الثلثاء", "ثلثاء", "الثلاثا", "ثلاثا"],
    4: ["الاربعاء", "الأربعاء", "اﻷربعاء", "اربعاء", "أربع"],
    5: ["الخميس", "خميس", "الخم", "الخم"],
    6: ["الجمعه", "الجمعة", "جمعه", "جمعة", "الجم"],
    7: ["السبت", "سبت", "السب", "سبت"]
}


def fetch_page(url, method='GET', data=None, retries=3, delay=1):
    """Fetches a page using the specified method with retry logic."""
    for attempt in range(retries):
        try:
            if method == 'POST':
                if isinstance(data, str):
                	data = data.encode('utf-8')
                response = session.post(
                    url,
                    headers={'Content-Type': 'application/x-www-form-urlencoded'},
                    data=data,
                    timeout=10)
            else:
                print("+++++Getting main page++++")
                response = session.get(url, timeout=10)

            response.encoding = 'utf-8'
            return response

        except Exception as e:
            print(f"[fetch_page] Attempt {attempt + 1} failed for {url}: {e}")
            if attempt < retries - 1:
                time.sleep(delay)  # Wait before retrying
            else:
                print(f"[fetch_page] Giving up after {retries} attempts.\n")

    return None  # If all attempts fail

def find_option_value(soup, target_texts):
    """Finds and returns the value of the option containing any of the target texts."""
    for option in soup.find_all('option'):
        if any(text in option.text for text in target_texts):
            return option['value']
    return None

def get_qr_code_url(soup):
    """Extracts and returns the QR code URL from the HTML."""
    img_tag = soup.select_one('div.qr img')
    if img_tag:
        return f"{BASE_URL}/{img_tag['src'].lstrip('../')}"
    return None

def write_qr_code_url_to_file(qr_code_url, show_name, date_time_str):
    try:
        print(f"Show Name: {show_name}: {date_time_str} ")
        print(f"QR Code URL: {qr_code_url}\n\n")
        with open("/data/data/com.termux/files/home/storage/downloads/qr_code_info.txt", "a") as file:
            file.write(f"Show Name: {show_name}: {date_time_str} ")
            file.write(f"QR Code URL: {qr_code_url}\n\n")
        print(f"Successfully wrote to file for {show_name}\n")
    except Exception as e:
        print(f"Failed to write to file: {e}")


def process_show(show_name, show_day, main_page_soup):
    """Processes the logic for a single show name, with retry logic for QR code not found."""
    for attempt in range(3):
        try:
            print(f"[{show_name}] Attempt {attempt + 1}")

            # Find offer ID
            offer_id = find_option_value(main_page_soup, [show_name])
            if not offer_id:
                print(f"[{show_name}] Offer option not found.")
                time.sleep(1)
                continue

            print(f"[{show_name}] Offer ID: {offer_id}")

            # Fetch showtime HTML
            showtime_response = fetch_page(
                f"{BASE_URL}/index/getoffertime",
                method='POST',
                data=f'offer_id={offer_id}'
            )

            if not showtime_response:
                print(f"[{show_name}] Failed to fetch showtime page.")
                time.sleep(1)
                continue

            soup = BeautifulSoup(showtime_response.text, 'html.parser')

            # Find showtime ID
            offerstime_id = find_option_value(soup, show_day)
            if not offerstime_id:
                print(f"[{show_name}] Showtime option not found.")
                time.sleep(1)
                continue

            print(f"[{show_name}] Showtime ID: {offerstime_id}")

            # Fetch QR code HTML
            qr_code_response = fetch_page(
                f"{BASE_URL}/index/offers",
                method='POST',
                data=f'name=Michael&phone=01227205558&offerstime_id={offerstime_id}&offer_id={offer_id}&submit=حجز'
            )

            if not qr_code_response:
                print(f"[{show_name}] QR code request failed.")
                time.sleep(1)
                continue

            soup = BeautifulSoup(qr_code_response.text, 'html.parser')
            qr_code_url = get_qr_code_url(soup)
            date_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Success
            if qr_code_url:
                print(f"[{show_name}] QR Code URL found: {qr_code_url}")
                write_qr_code_url_to_file(qr_code_url, show_name, date_time_str)
                return  # Done
            else:
                print(f"[{show_name}] QR code not found.")
                write_qr_code_url_to_file("QR code not found", show_name, date_time_str)
                time.sleep(1)

        except Exception as e:
            print(f"[{show_name}] Unexpected error: {e}")
            time.sleep(1)

    print(f"[{show_name}] Failed after 3 attempts. Skipping.\n")


def banner():
    encoded = b'ICAgICBfX19fXyAgICAgICAgICAgICAgXyAgICAgICANCiAgX198X19fICB8XyBfICBfX18gX19ffCB8XyAgIF8gDQogLyBfIFwgLyAvIF9gIHwvIF8gXF8gIC8gfCB8IHwgfA0KfCAgX18vLyAvIChffCB8ICBfXy8vIC98IHwgfF98IHwNCiBcX19fL18vIFxfXywgfFxfX18vX19ffF98XF9fLCB8DQogICAgICAgICB8X19fLyAgICAgICAgICAgIHxfX18vIA0KICAgICAgICAgQnkgTWljaGFlbCBXYWdkecKp'
    font = base64.b64decode(encoded).decode('utf-8')
    print(font)
def main():
    banner()
    # Take inputs from the command line
    show_names = sys.argv[1].split(',')
    show_time_value = int(sys.argv[2])
    show_day = DAYS_OF_WEEK.get(show_time_value, [])

    if not show_day:
        print("Invalid show time value. Please provide a value between 1 and 7.")
        return

    # Fetch the initial main page once and parse it
    main_page_response = fetch_page(BASE_URL)
    if not main_page_response:
        print("Failed to fetch the main page.\n")
        return

    main_page_soup = BeautifulSoup(main_page_response.text, 'html.parser')

    # Process each show name in parallel
    with ThreadPoolExecutor() as executor:
        for show_name in show_names:
            executor.submit(process_show, show_name, show_day, main_page_soup)


if __name__ == "__main__":
    main()
