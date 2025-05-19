import json
import requests
import os
import time
import sys
from bs4 import BeautifulSoup
import pickle
import re


def is_captcha_page(soup):
    """Check if the current page is a CAPTCHA verification page"""
    captcha_text = soup.find(string="Vui lòng xác minh không phải Robot")
    thong_bao = soup.find(string="THÔNG BÁO")
    return captcha_text is not None or thong_bao is not None


def save_progress(last_completed_page):
    """Save the last successfully completed page number"""
    with open("crawl_progress.txt", "w") as f:
        f.write(str(last_completed_page))


def load_progress():
    """Load the last successfully completed page number"""
    if os.path.exists("crawl_progress.txt"):
        with open("crawl_progress.txt", "r") as f:
            return int(f.read().strip())
    return None


def crawl_alonhadat_page(page_num=1, max_retries=3, retry_delay=5):
    url = f"https://alonhadat.com.vn/nha-dat/can-ban/nha-dat/1/ha-noi/trang--{page_num}.html"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.encoding = "utf-8"
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Check if we've hit a CAPTCHA page
            if is_captcha_page(soup):
                print(f"\n\033[91mCAPTCHA detected on page {page_num}!\033[0m")
                print("The website requires human verification.")
                print(f"Please manually visit: {url}")
                print("Complete the CAPTCHA verification in your browser.")
                
                # Save the current state and progress for resuming later
                save_progress(page_num - 1)
                
                user_input = input("Once you've completed verification, press Enter to retry, or type 'skip' to skip this page: ")
                if user_input.lower() == 'skip':
                    print(f"Skipping page {page_num}...")
                    return []
                continue  # Retry the request
            
            items = soup.find_all("div", class_="content-item")
            
            # If we don't find any content items but also no CAPTCHA, the page might be empty
            if not items:
                print(f"Warning: No content items found on page {page_num}. The page might be empty or have a different structure.")
            
            results = []
            for item in items:
                try:
                    # Ensure title and link exist
                    title_div = item.find("div", class_="ct_title")
                    if not title_div:
                        continue
                    anchor = title_div.find("a")
                    if not anchor or not anchor.get("href"):
                        continue
                    title = anchor.get_text(strip=True)
                    link = "https://alonhadat.com.vn" + anchor["href"]

                    # Extract date
                    date_div = item.find("div", class_="ct_date")
                    date = date_div.get_text(strip=True) if date_div else ""

                    # Extract area
                    area_div = item.find("div", class_="ct_dt")
                    area = area_div.get_text(strip=True).replace("Diện tích:", "") if area_div else ""

                    # Extract price
                    price_div = item.find("div", class_="ct_price")
                    price = price_div.get_text(strip=True).replace("Giá:", "") if price_div else ""

                    # Extract floors
                    floors_span = item.find("span", class_="floors")
                    floors = floors_span.get("title", "") if floors_span else ""

                    # Extract bedrooms
                    bed_span = item.find("span", class_="bedroom")
                    bedrooms = bed_span.get("title", "") if bed_span else ""

                    # Extract address
                    addr_div = item.find("div", class_="ct_dis")
                    address = addr_div.get_text(separator=", ", strip=True) if addr_div else ""

                    # Initialize optional fields
                    road_width = car_parking = description = orientation = dimension = ""
                    # Extract description summary
                    desc_div = item.find("div", class_="ct_content")
                    if desc_div:
                        description = desc_div.get_text(separator=" ", strip=True)
                    # Parse orientation and dimension from description
                    if description:
                        orient_m = re.search(r"Hướng[:：]\s*([^\s,]+)", description)
                        if orient_m:
                            orientation = orient_m.group(1)
                        dim_m = re.search(r"KT[:：]\s*([\d\.x]+)", description)
                        if dim_m:
                            dimension = dim_m.group(1)
                    # Extract additional span titles
                    for span in item.find_all("span", title=True):
                        t = span["title"]
                        if "Đường trước nhà" in t:
                            road_width = t.split(":", 1)[1].strip()
                        if "Chỗ để xe" in t:
                            car_parking = t.split(":", 1)[1].strip()

                    results.append({
                        # Primary info
                        "title": title,
                        "url": link,
                        "date": date,
                        "area": area,
                        "price": price,
                        "floors": floors,
                        "bedrooms": bedrooms,
                        "address": address,
                        # Optional fields
                        "road_width": road_width,
                        "car_parking": car_parking,
                        "description": description,
                        "orientation": orientation,
                        "dimension": dimension,
                    })
                except Exception as e:
                    print(f"Error parsing item: {e}")
            
            return results
            
        except requests.RequestException as e:
            print(f"Request failed (attempt {attempt+1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                print(f"Waiting {retry_delay} seconds before retrying...")
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
    
    print(f"Failed to crawl page {page_num} after {max_retries} attempts.")
    return []


def main():
    # Default page range
    start_page = 2
    end_page = 200

    # Set up output directory relative to project root
    root_dir = os.getcwd()
    output_dir = os.path.join(root_dir, 'Data Collection', 'Datasets', 'alonhadat.com', 'json')
    os.makedirs(output_dir, exist_ok=True)
    
    # Check if resuming from a previous run
    last_completed = load_progress()
    if last_completed is not None:
        resume = input(f"Previous crawl stopped at page {last_completed}. Resume from page {last_completed + 1}? (y/n): ")
        if resume.lower() == 'y':
            start_page = last_completed + 1
    
    # Allow command-line arguments to override defaults
    if len(sys.argv) >= 3:
        start_page = int(sys.argv[1])
        end_page = int(sys.argv[2])
    
    print(f"Starting crawl from page {start_page} to {end_page}...")
    
    for page_num in range(start_page, end_page + 1):
        print(f"\nCrawling page {page_num}...")
        data = crawl_alonhadat_page(page_num)
        
        if data:  # Only write file if we got data
            output_file = os.path.join(output_dir, f"page_{page_num}.jsonl")
            with open(output_file, "w", encoding="utf-8") as file:
                for d in data:
                    file.write(json.dumps(d, ensure_ascii=False) + "\n")
            print(f"Successfully saved {len(data)} items to {output_file}")
            save_progress(page_num)  # Update progress after successful save
        else:
            print(f"No data retrieved for page {page_num}")


if __name__ == "__main__":
    main()
