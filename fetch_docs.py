"""Crawl Linear's public docs and developer docs: start from the sitemap, follow every
/docs/ and /developers/ link
found in each page, keep each page's text. One request at a time with a pause. Resumable."""
import html, json, re, time, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'data/docs'


def text_of(page):
    page = re.sub(r'(?is)<(script|style|noscript|svg|nav|footer|header)\b.*?</\1>', ' ', page)
    title = re.search(r'(?is)<title>(.*?)</title>', page)
    main = re.search(r'(?is)<main\b.*?</main>', page)
    body = main.group(0) if main else page
    body = re.sub(r'(?i)<(h[1-4]|p|li|tr|br|div)\b', r'\n<\1', body)
    t = html.unescape(re.sub(r'<[^>]+>', ' ', body))
    t = '\n'.join(re.sub(r'[ \t]+', ' ', l).strip() for l in t.splitlines())
    return (html.unescape(title.group(1)).strip() if title else ''), re.sub(r'\n{3,}', '\n\n', t).strip()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    queue = (ROOT / 'data/doc_urls.txt').read_text().split()
    seen = set(queue)
    while queue:
        url = queue.pop(0)
        section, rest = re.match(r'https://linear\.app/(docs|developers)/?(.*)', url.rstrip('/')).groups()
        slug = ('dev__' if section == 'developers' else '') + (rest.replace('/', '__') or section)
        f = OUT / f'{slug}.json'
        if f.exists() and 'links' in json.loads(f.read_text()):
            links = json.loads(f.read_text())['links']
        else:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (support-docs research)'})
            try:
                page = urllib.request.urlopen(req, timeout=30).read().decode('utf-8', 'replace')
            except Exception as e:
                print('skip', url, e); continue
            links = sorted({'https://linear.app' + l.rstrip('/') for l in
                            re.findall(r'href="(?:https://linear\.app)?(/(?:docs|developers)/[a-z0-9][a-z0-9\-/]*)', page)})
            title, text = text_of(page)
            f.write_text(json.dumps({'url': url, 'title': title, 'text': text, 'links': links}, indent=1))
            time.sleep(1)
        for l in links:
            if l not in seen:
                seen.add(l); queue.append(l)
    print(len(list(OUT.glob('*.json'))), 'pages')


if __name__ == '__main__':
    main()
