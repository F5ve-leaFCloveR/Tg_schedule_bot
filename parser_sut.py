from bs4 import BeautifulSoup as bs
import requests
import pandas as pd

URL_sut = "https://www.sut.ru/studentu/raspisanie/raspisanie-zanyatiy-studentov-ochnoy-i-vecherney-form-obucheniya?group=54828&date=2023-02-06"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

def parse(url = URL_sut, head = headers):
    r = requests.get(URL_sut, headers=head)
    soup = bs(r.text, "html.parser")

    result_dict = {"day": [], "time": [], "information":[]}
    parse = soup.find_all('div', class_='vt239')
    
    for classies in parse:
        if classies.text.strip() != "":
            time = bs(str(classies), "html.parser")
            parsed_time_key = time.find_all('div', class_='vt283')
            for key in parsed_time_key:
                if key.text.strip() != "":
                    time_key = key.text
                    break
            for days in range(1, 7):
                per_day = time.find_all('div', class_=f"vt239 rasp-day rasp-day{days}")
                for disc in per_day:
                    if disc.text.strip() != "":
                        result_dict["day"].append(days)
                        result_dict["time"].append(time_key)
                        result_dict["information"].append(disc.text.replace("\t", ""))
    print(result_dict["day"][1])
    print(result_dict["time"][1])
    print(result_dict["information"][1])

    return result_dict

df = pd.DataFrame(data=parse()) 
df.to_csv("parsed_data.csv", index=False)
