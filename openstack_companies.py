import geocoder
import sys
import wiki
from bs4 import BeautifulSoup


PATH_TO_COMPANIES_LIST = "/path/to/file"


def get_companies_list_from_html(html_file):
    """
    Returns list of companies from stackalitycs html file.

    Keyword arguments:
    html_file -- html-type file with companies list from stackalitycs.org
    """
    companies_list = []
    soup = BeautifulSoup(open(html_file), "html.parser")
    div_list = soup.find_all("div")
    for div_obj in div_list:
        companies_list.append(div_obj.text)
    return companies_list


def get_companies_list_from_txt(txt_file):
    with open(txt_file, 'r') as f:
        return f.readlines()


def get_formalized_countries(unformalized_list):
    # TODO: change logic for searching companies
    for country in unformalized_list:
        if "None" not in country:
            g = geocoder.google(country)
            print g
        else:
            print None


def get_companies_list(source):
    """
    Returns company's list from source.
    """
    if source.lower().endswith(".txt"):
        return get_companies_list_from_txt(source)
    elif source.lower().endswith(".html"):
        return get_companies_list_from_html(source)
    else:
        print "Unknown source type!"
        return None


def get_companies_info(companies_list, info_type):
    print "#---"
    print "I'm starting a request for company %s:" % info_type
    print "#---"
    for company in companies_list:
        company_html = wiki.get_company_page(company)
        company_info = wiki.get_company_info(company_html, info_type)
        if info_type == "Headquarters":
            print geocoder.google(company_info).country_long
        else:
            print company_info.strip()


def main():
    reload(sys)
    sys.setdefaultencoding('utf-8')
    companies_list = get_companies_list(PATH_TO_COMPANIES_LIST)
    if companies_list is None:
        return
    try:
        get_companies_info(companies_list, "Headquarters")
        get_companies_info(companies_list, "Area served")
    except Exception as e:
        print "Script failed with error: %s" % e


if __name__ == "__main__":
    main()
