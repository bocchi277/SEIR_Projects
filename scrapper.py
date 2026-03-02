from bs4 import BeautifulSoup
import sys
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options

def loadUrl(userUrl):
    change_options = Options()
    change_options.add_argument("--headless=new")
    driver = webdriver.Chrome(options = change_options)
    try:
        driver.get(userUrl)
        time.sleep(3)
        content = driver.page_source
    except Exception:
        return None
    finally:
        driver.close()
    if content:
        soup = BeautifulSoup(content, 'html.parser')
        title_tag = soup.find('title')
        title = title_tag.text if title_tag else "Title Tag is missing"
        bodyTag = soup.find('body')
        bodyText = bodyTag.get_text(separator="\n", strip=True) if bodyTag else "Body is Not there"
        links = [link.get('href') for link in soup.find_all('a') if link.get('href')]
        formatLinks = [i for i in links if i.startswith("https://") or i.startswith("/")]
        return {"title": title, "bodyText": bodyText, "Links": formatLinks}
    else:
        print("Some error happened!!")
        return None
if __name__ == "__main__":
    try:
        userUrl = sys.argv
        if len(userUrl) == 2:
                userUrl = sys.argv[1]
                if not userUrl.startswith("https://"):
                   userUrl = f"https://{userUrl}"
                content = loadUrl(userUrl)
                if content:
                    for i in content:
                        if i != "Links":
                            print(f"The {i} is --> {content[i]}")
                        else:
                            print("The links are -->")
                            for j in content[i]:
                                print(j)
                else:
                    print("Failed , Empty Content")
        else:
            print("You gave either more or less than 1 argument.. Kindly Type 'python <urlname>'")
    except Exception as e:
        print(e)