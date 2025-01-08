# Module: pubmed_fetcher
import requests
import xml.etree.ElementTree as ET
import csv
import re
from typing import List, Optional

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
EMAIL = "abhinavprajapati351@gmail.com"

def fetch_paper_ids(query: str, retmax: int = 100) -> List[str]:
    """Fetch PubMed IDs based on the query."""
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": retmax,
        "retmode": "json",
        "email": EMAIL,
    }
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    return response.json().get("esearchresult", {}).get("idlist", [])

def fetch_xml_data(paper_ids: List[str]) -> str:
    """Fetch detailed XML data for given PubMed IDs."""
    params = {
        "db": "pubmed",
        "id": ",".join(paper_ids),
        "retmode": "xml",
        "email": EMAIL,
    }
    response = requests.get(FETCH_URL, params=params)
    response.raise_for_status()
    return response.text

def extract_pubmed_data_to_csv(
    xml_data: str, csv_filename: Optional[str] = None
) -> List[List[str]]:
    """Parse PubMed XML data and extract required fields to CSV or list."""
    root = ET.fromstring(xml_data)

    # Prepare data container
    results = []

    # Process articles
    for article in root.findall(".//PubmedArticle"):
        pubmed_id = article.find(".//PMID").text if article.find(".//PMID") is not None else ""
        title = article.find(".//ArticleTitle").text if article.find(".//ArticleTitle") is not None else ""
        pub_year = article.find(".//PubDate/Year").text if article.find(".//PubDate/Year") is not None else ""
        pub_month = article.find(".//PubDate/Month").text if article.find(".//PubDate/Month") is not None else ""
        pub_day = article.find(".//PubDate/Day").text if article.find(".//PubDate/Day") is not None else ""
        pub_date = f"{pub_year}-{pub_month}-{pub_day}".strip("-")

        authors = []
        non_academic_authors = []
        company_affiliations = []
        corresponding_author_email = "N/A"

        for author in article.findall(".//Author"):
            last_name = author.find("LastName").text if author.find("LastName") is not None else ""
            fore_name = author.find("ForeName").text if author.find("ForeName") is not None else ""
            author_name = f"{last_name}, {fore_name}".strip(", ")
            authors.append(author_name)

            affiliation = author.find(".//Affiliation").text if author.find(".//Affiliation") is not None else ""

            if affiliation and not any(keyword in affiliation.lower() for keyword in ["university", "institute", "school"]):
                non_academic_authors.append(author_name)
                company_affiliations.append(affiliation)

            emails = re.findall(r"[\w.-]+@[\w.-]+\.[a-z]{2,}", affiliation, re.IGNORECASE)
            if emails:
                corresponding_author_email = ", ".join(emails)

        results.append([
            pubmed_id,
            title,
            pub_date,
            "; ".join(authors),
            "; ".join(non_academic_authors),
            "; ".join(company_affiliations),
            corresponding_author_email,
        ])

    # Write to CSV if filename provided
    if csv_filename:
        with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([
                "PubmedID", "Title", "Publication Date", "Authors",
                "Non-academic Authors", "Company Affiliations", "Corresponding Author Email"
            ])
            writer.writerows(results)

    return results