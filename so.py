import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://stackoverflow.com/jobs?q=python&sort=i"

def get_last_page():
  result = requests.get(URL)
  soup = BeautifulSoup(result.text, "html.parser")
  pages = soup.find("div", {"class":"s-pagination"}).find_all("a")
  last_page = pages[-2].get_text(strip=True)
  return int(last_page)

def extract_job(html):
  title = html.find("a", {"class":"s-link"})["title"]
  h3 = html.find("h3", {"class":"fs-body1"}).find_all("span")
  company = h3[0].get_text(strip=True)
  location = h3[1].get_text(strip=True)
  id = html["data-jobid"]
  return {"title" : title, "company" : company, "location" : location, "link" : f"https://stackoverflow.com/jobs/{id}"}



def extract_jobs(last_page):
  jobs = []
  for page in range(last_page):
    url = f"{URL}&pg={page+1}"
    if(page == 0):
      url = URL
    print(f"SO page : {page+1} scrapping")
    html = requests.get(url)
    soup = BeautifulSoup(html.text, "html.parser")
    results = soup.find_all("div", {"class":"-job"})
    for result in results:
      job = extract_job(result)
      jobs.append(job)
  return jobs


def get_jobs():
  last_page = get_last_page()
  jobs = extract_jobs(last_page)
  return jobs

