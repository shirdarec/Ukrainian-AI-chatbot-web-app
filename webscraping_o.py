import requests
from bs4 import BeautifulSoup as bs
import json
import markdownify

# best run on linux. Windows might cause errors in symblos attached to name of sections when creating md file

BASE_URL = "https://www.nav.no/tjenester/en"
START_URL = "https://www.nav.no"

resp = requests.get(BASE_URL)

soup = bs(resp.content, "html.parser")

all_sections = soup.find_all("section")

def extract_details(i, bs_tag):
  skip = False
  curr_section = bs_tag.find_all("span")[-1].text
  short_details = bs_tag.find_all("p")[0].text
  more_lnk = str(bs_tag.find_all("a")[0]).split("=")[2].split('"')[1]
  more_lnk = more_lnk.replace(START_URL, "")
  if more_lnk.startswith("/"):
    final_link = START_URL+more_lnk
  else:
    skip = True
  if skip:
    print("skip", i, more_lnk)
    return
  resp2 = requests.get(final_link)
  soup2 = bs(resp2.content, "html.parser")
  if i < 1:
    md_text = markdownify.markdownify(json.loads(soup2.find_all("script")[-1].text)['props']['pageProps']['content']["data"]['text']["processedHtml"])
  else:
    md_texts = []
    if len(soup2.find_all("script")[-1].text) != 0:
      s_j = json.loads(soup2.find_all("script")[-1].text)
      if "content" in s_j["props"]['pageProps']:
        #
        if "pageContent" in s_j["props"]['pageProps']['content']['page']['regions']:
          for comp in s_j["props"]['pageProps']['content']['page']['regions']['pageContent']['components']:
            if "regions" in comp:
              if "content" in comp["regions"]:
                for comp2 in comp['regions']['content']['components']:
                  if "config" in comp2:
                    if "html" in comp2['config']:
                      md_texts.append(markdownify.markdownify(comp2['config']['html']['processedHtml']))
              else:
                print("no-cont", i, more_lnk)
            else:
              print("rgn", i, more_lnk)
        else:
          print('pgcont', i,more_lnk)
      else:
        print("nocont", i, more_lnk)
    else:
      print("no data", i, more_lnk)

  with open(f"markdown_files/markdown_o/{i+1}-{curr_section}.md", "w", encoding="utf-8") as f:
    f.write(f"#{curr_section}\n")
    f.write(f"{short_details}\n")
    if i < 1:
      f.write(md_text)
    else:
      f.writelines(md_texts)

for i in range(200, len(all_sections)):
  extract_details(i, all_sections[i])