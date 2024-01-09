import requests
from bs4 import BeautifulSoup
import tldextract
from data import create_table, insert_domain


def get_html_content(url):
    response = requests.get(url)
    return response.content


def make_soup(html_content):
    return BeautifulSoup(html_content, "html.parser")


def soup_from_url(url):
    html_content = get_html_content(url)
    return make_soup(html_content)


def get_box_section(soup):
    return soup.find("section", class_="box")


def get_box_section_from_url(url):
    soup = soup_from_url(url)
    return get_box_section(soup)


def get_a_tags(box_section):
    return box_section.find_all("a") if box_section else []


def get_a_tags_from_url(url):
    box_section = get_box_section_from_url(url)
    return get_a_tags(box_section)


def get_a_tag_text(a_tags):
    return [tag.get_text().strip() for tag in a_tags]


def get_a_tag_text_from_url(url):
    a_tags = get_a_tags_from_url(url)
    return get_a_tag_text(a_tags)


def clean_list(text_list):
    clean_list = []
    for text in text_list:
        extracted = tldextract.extract(text)
        if extracted.domain and extracted.suffix:
            domain = f"{extracted.domain}.{extracted.suffix}"
            clean_list.append(domain)
    return clean_list


def clean_list_from_url(url):
    text_list = get_a_tag_text_from_url(url)
    return clean_list(text_list)


def url_from_user():
    return input("Enter url: ")


def fetch_and_process_txt_file(base_url, max_pages=641):
    page = 1
    while page <= max_pages:
        url = base_url if page == 1 else f"{base_url}/{page}"
        print(f"Getting list from page {page}...")
        clean_list = clean_list_from_url(url)
        print("Writing to file...")
        with open("domains.txt", "a") as file:
            for domain in clean_list:
                file.write(f"{domain}\n")
        page += 1
    print("Done!")
    return True


def fetch_and_process_db(base_url, max_pages=641):
    page = 1
    while page <= max_pages:
        url = base_url if page == 1 else f"{base_url}/{page}"
        print(f"Getting list from page {page}...")
        clean_list = clean_list_from_url(url)
        print("Writing to db...")
        for domain in clean_list:
            insert_domain(domain)
        page += 1
    print("Done!")
    return True


def main():
    create_table("domains")
    base_url = url_from_user()
    fetch_and_process_db(base_url)
    return True


if __name__ == "__main__":
    main()
