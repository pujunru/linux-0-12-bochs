import os
import requests
from bs4 import BeautifulSoup

PAR_URL = "http://www.oldlinux.org/Book-Lite/Bochs/"

def traverse_site(site: str, cur_dir: str):
    os.mkdir(cur_dir)
    page = requests.get(site)
    soup = BeautifulSoup(page.content, "html.parser")
    all_a = soup.find_all("a")
    for a in all_a:
        print(a.attrs)
        if a["href"] == "../":
            continue
        rel_link = next(a.children)
        next_link = f"{site}{next(a.children)}"
        print(next_link)
        # if the rel_link is ended with /, this is a sub link, continue
        if rel_link.endswith("/"):
            traverse_site(next_link, os.path.join(cur_dir, rel_link))
        # else, it is a file, download it and save to cur_dir
        else:
            if rel_link.endswith(".txt") or rel_link.endswith(".TXT") or rel_link.endswith("README"):
                with open(os.path.join(cur_dir, rel_link), "w+") as f:
                    f.write(requests.get(next_link).text)
            else:
                with open(os.path.join(cur_dir, rel_link), "wb+") as f:
                    f.write(requests.get(next_link, stream=True).raw.read())


def main():
    root_path = os.path.join(os.curdir, "bochs")
    traverse_site(PAR_URL, root_path)

if __name__ == "__main__":
    main()
