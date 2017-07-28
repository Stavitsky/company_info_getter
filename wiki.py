import sys
import wikipedia
from bs4 import BeautifulSoup


reload(sys)
sys.setdefaultencoding('utf-8')


def get_company_page(company):
    company_page = wikipedia.page(company)
    # print company_page.url
    return company_page.html()


def get_company_info(company_html, info_type="Headquarters"):
    """
    Returns company's info depends on info_type.

    Keywords arguments:
    company_html -- HyperText of company's wikipedia page
    info_type -- 'Headquarters' or 'Area served'
    """
    if info_type == "Headquarters":
        return _get_headquarters_from_html(company_html)
    elif info_type == "Area served":
        return _get_area_served_from_html(company_html)


def _get_headquarters_from_html(html):
    """
    Returns company's headquarters country from wikipedia page html.

    Keywords arguments:
    html -- HyperText of company's wikipedia page
    """
    soup = BeautifulSoup(html, "html.parser")
    country = soup.find("span", {"class": "country-name"})
    if country is None:
        # print "No country-name class, try to parse table."
        return _parse_html_table(soup, html, "Headquarters")
    return country.text


def _get_area_served_from_html(html):
    """
    Returns company's served area from wikipedia page html.

    Keywords arguments:
    html -- HyperText of company's wikipedia page
    """
    soup = BeautifulSoup(html, "html.parser")
    return _parse_html_table(soup, html, "Area served")


def _parse_html_table(soup, page, header):
    """
    Returns value from wikipedia infobox table.

    Keyword arguments:
    soup -- BeautifulSoup object
    page -- wikipedia html
    header -- infobox table row header
    """
    tables = soup.findChildren("table", {"class": "infobox vcard"})
    try:
        infobox_table = tables[0]
    except Exception:
        return None
    rows = infobox_table.findChildren(["th", "tr"])
    for row in rows:
        th_cells = row.findChildren("th")
        for th_cell in th_cells:
            if th_cell.text == header:
                return row.findChildren("td")[0].text


def main():
    pass


if __name__ == "__main__":
    main()
