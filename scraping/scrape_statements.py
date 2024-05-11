import requests
from time import sleep
from bs4 import BeautifulSoup
import re


'''
Function to iterate througth the links in a soup object to find a target link
    Args:
        soup: BeautifulSoup object
        target_text: str, the text to search for in the links
    Returns:
        list, the links that contain the target text
'''
def find_target_links(url, target_text):
    # Soup the URL
    soup = get_soup(url)

    # Iterate through the links in the soup object
    links = []
    for link in soup.find_all('a', href=True):
        if target_text in link.text:
            links.append(link['href'])
        elif target_text in link['href']:
            links.append(link['href'])
    
    # Return the list of links if the target text is found
    if links:
        return links
    else:
        # Throw an error if the target text is not found
        raise ValueError(f'Target text "{target_text}" not found in the links')

# Function to download a PDF from a URL
def download_pdf(url, output_folder, pdf_to_download):
    # Clean the PDF name    
    cleaned_pdf_name = name_pdf(pdf_to_download)
    # Put the PDF name together with the output path
    output_path = f'{output_folder}{cleaned_pdf_name}'
    
    # Check if the PDF is already downloaded
    try:
        with open(output_path, 'rb') as f:
            print('Already downloaded PDF')
        return output_path
    except FileNotFoundError:
        print(f'Downloading PDF: {output_path}')

    # Fetch the PDF
    response = requests.get(url)

    # Save the PDF
    with open(output_path, 'wb') as f:
        f.write(response.content)

    return output_path

# Function to get the soup object from a URL
def get_soup(url):
    # Try to fetch the page
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(e)
        return None
    
    # Parse the page
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

# Function to name the output PDF
def name_pdf(url):
    # Get the date from the URL which is a series of numbers after 'monetary'
    date_str = url.split('monetary')[-1].split('.')[0]
    # Use a regex to separate the date part from the letters/numbers
    match = re.match(r"(\d{4})(\d{2})(\d{2})(.*)", date_str)
    if match:
        year, month, day, remainder = match.groups()
        formatted_date = f"-{year}-{month}-{day}"
        if remainder:
            formatted_date += f"-{remainder}"
        return f"press-release{formatted_date}.pdf"
    else:
        raise ValueError("Input string format is not recognized")

# Main function
def scrape_statements():
# if __name__ == '__main__':
    # Base URL for the Federal Reserve
    base_url = 'https://www.federalreserve.gov'

    # Output path for the PDFs
    output_path = './statements/'

    # URL to FOMC materials
    url = 'https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm'

    starting_month_number = 3
    starting_year = 2014
    ending_month_number = 12
    ending_year = 2024

    url = f'''
        https://www.fedsearch.org/fomc-docs/search?
        advanced_search=true&
        fomc_document_type=policystatement&
        text=&
        search_precision=All+Words&
        from_month={starting_month_number}&
        from_year={starting_year}&
        to_month={ending_month_number}&
        to_year={ending_year}&
        sort=Most+Recent+First&
        Search=Search
        '''

    url = 'https://www.federalreserve.gov/newsevents/pressreleases.htm'

    url = 'https://www.federalreserve.gov/newsevents/pressreleases.htm#'

    base_url = 'https://www.federalreserve.gov'

    # Fetch the page
    press_release_soup = get_soup(url)
    # response = requests.get(url)
    # soup = BeautifulSoup(response.text, 'html.parser')

    # Sleep for 1 second to avoid being blocked
    sleep(1)

    # Find the link to the 2024 FOMC page
    FOMC_link_2024 = find_target_links(url, '2024 FOMC')[0]
    print(FOMC_link_2024)

    FOMC_link_2024 = base_url + FOMC_link_2024
    # Find the links to the 2024 press releases
    # press_release_links = find_target_links(FOMC_link_2024, 'pressrelease')
    # print(FOMC_link_2024)

    press_release_links = find_target_links(FOMC_link_2024, 'FOMC statement')

    # print(press_release_links)

    # Iterate through the press release links
    for link in press_release_links:
        # Get the full URL
        full_url = base_url + link

        # print(full_url)

        # Find the PDF link
        pdf_link = find_target_links(full_url, 'pdf')[0]
        pdf_link = base_url + pdf_link

        # print(pdf_link)

        pdf_to_download = pdf_link.split("/")[-1]

        # Download the PDF
        output_path = download_pdf(pdf_link, output_path, pdf_to_download)

        # Sleep for 1 second to avoid being blocked
        sleep(1)

        return output_path

        break