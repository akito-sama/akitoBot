import requests
import bs4
import collections


def wiki_search(text, lang="fr"):
    a = 0
    url_reponse = "//upload.wikimedia.org/wikipedia/commons/thumb/d/d1/Wikipedia-logo-v2-fr.svg/langfr-150px-Wikipedia-logo-v2-fr.svg.png"
    liste = []
    url = f'https://{lang}.wikipedia.org/wiki/{text}' if not text.startswith('http') else text
    rps = requests.get(url)
    if rps.ok:
        soup = bs4.BeautifulSoup(rps.text, 'html.parser')
        info_box = soup.find('div', {'class': 'infobox_v3 large'})
        if info_box:
            url_reponse = info_box.findNext('img')['src']
        content = soup.find('div', {'class': "mw-parser-output"})
        ps = content.findAll('p')[:]
        counter = 0
        for p in ps:
            if p.text.strip() != "" and len(p.text.strip()) > 30:
                liste.append(f'{p.text.strip()}\n')
                counter += len(p.text)
                if counter >= 500 or p.text.strip().endswith(':'):
                    break
        if liste[0].strip().replace('\n', '').endswith(':'):
            a = content.findAll('h2')
            a = a[0] if a != [] else content
            liste.append(f'{a.text}\n')
            # ul = content.findAll('ul')[2]
            ul = a.findNext('ul')
            for i in ul.text.split('\n'):
                liste.append(f'\t{i}\n')
        liste.append(f'\nto see another things about thats, visits the web site {url}\n')
    elif rps.status_code == 404:
        urlsearch = f"https://fr.wikipedia.org/w/index.php?title=Spécial:Recherche&search={text.replace(' ', '+')}"
        rps = requests.get(urlsearch)
        if rps.ok:
            soup = bs4.BeautifulSoup(rps.text, 'html.parser')
            div = soup.find('div', {'class': 'mw-search-result-heading'})
            url = div.findNext('a')['href']
            return wiki_search(f'https://{lang}.wikipedia.org{url}')
        else:
            liste.append("the page is introuvable pleas verify the orthograph or the language")
            return "".join(liste)
    else:
        liste.append("an error has been occured")
    return "".join(liste), url_reponse, rps.url


def larousse(text, boolean=True):
    url = f"https://www.larousse.fr/dictionnaires/francais/{text}"
    rqt = requests.get(url)
    printt = print if not boolean else lambda *args: None
    if rqt.ok:
        soup = bs4.BeautifulSoup(rqt.text, 'html.parser')
        def_div = soup.find('div', {'id': "definition"})
        if def_div:
            dico = collections.defaultdict(list)
            ul_def = def_div.findNext('ul', {'class': 'Definitions'})
            printt("\n".join("def:\n\n\t" + li.text.replace(':', '\n\nExemple :\n\n\t').strip() for li in ul_def if not isinstance(li, bs4.NavigableString)))
            for li in ul_def:
                if not isinstance(li, bs4.NavigableString):
                    if ':' in li.text:
                        splited = li.text.split(':')
                        dico['definition'].append(splited[0])
                        dico['exemple'].append(splited[1])
                    else:
                        dico['definition'].append(li.text)

            ul_syn = soup.findAll('ul', {'class': "Synonymes"})
            dico['synonymes'] = [li.text.replace('\n', '') for li in ul_syn if not isinstance(li, bs4.NavigableString)]

            return dico, url
        else:
            def_div = soup.find('section', {'class': 'corrector'})
            ul = def_div.find_all_next('h3')
            return tuple((f"{li.text}", f"https://www.larousse.fr/dictionnaires/francais/{li.text}\n") for li in ul), None


def larousse_conjug(verbe, time, mode:str):
    mode = mode.upper()
    url = f"https://www.larousse.fr/conjugaison/francais/{verbe}"
    rqt = requests.get(url)
    liste = []
    if rqt.ok:
        soup = bs4.BeautifulSoup(rqt.text, 'html.parser')
        text = soup.find('p', {"class": "groupe aux"})
        description = text.text
        h2s = soup.findAll("h2")
        for h2 in h2s:
            if h2.text.strip().startswith(mode):
                liste.append(f'{h2.text.lower().strip()}\n')
                break
        else:
            return
        h3s = h2.find_all_next('h3')
        for h3 in h3s:
            if h3.text.lower().strip() == f'-{time.lower().strip()}':
                liste.append(f'{h3.text.lower().strip()}\n')
                break
        else:
            return
        ul = h3.findNext('ul')
        for li in ul:
            if not isinstance(li, bs4.NavigableString):
                liste.append(f'-{li.text}\n')
        return liste, description


if __name__ == '__main__':
    # text, time, mode = input("entrer ce que vous voulez rechercher\n").split()
    # txt, url, *_ = wiki_search(text, lang='fr')
    text = "gumball"
    print(wiki_search(text))
    # text = input("bla bla bla \n")
    # c = larousse(text, True)
    # print(json.dumps(c, indent=4, ensure_ascii=False) if isinstance(c, dict) else c)
    # print(larousse_conjug(*text.split('-')))