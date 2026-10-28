"""Support-operations metrics from the public GitHub threads: who answered, how fast, whether
the user was redirected to email support, and whether a question was closed unanswered.
Writes data/threads.json.

    python3 threads.py
"""
import json, re, subprocess
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from evalkit.models import ROOT

STAFF = ('MEMBER', 'OWNER', 'COLLABORATOR', 'CONTRIBUTOR')
LINKBACK = re.compile(r'\s*(<!-- linear-linkback -->)?\s*<p><a href="https://linear\.app/linear/issue/[^"]+">[^<]*</a></p>\s*')


def gh(path):
    out = subprocess.run(['gh', 'api', '--paginate', path], capture_output=True, text=True).stdout
    return json.loads(out or '[]')


def ts(s):
    return datetime.strptime(s, '%Y-%m-%dT%H:%M:%SZ')


def one(x):
    n = x['number']
    issue = gh(f'repos/linear/linear/issues/{n}')
    comments = gh(f'repos/linear/linear/issues/{n}/comments')
    human = [c for c in comments if c.get('author_association') in STAFF and not c['user']['login'].endswith('[bot]')
             and not LINKBACK.fullmatch(c['body'])]
    bot_relay = [c for c in comments if c['user']['login'] == 'linear-code[bot]' and not LINKBACK.fullmatch(c['body'])]
    replies = sorted(human + bot_relay, key=lambda c: c['created_at'])  # linear-code relays staff replies written in Linear
    stale = any('automatically closed' in c['body'] for c in comments)
    first = replies[0]['created_at'] if replies else None
    return {'number': n, 'type': x['type'], 'area': x['area'], 'state': issue['state'],
            'state_reason': issue.get('state_reason'), 'created_at': issue['created_at'],
            'linked_internal_ticket': any(LINKBACK.fullmatch(c['body']) for c in comments),
            'staff_replies': len(replies),
            'hours_to_first_reply': round((ts(first) - ts(issue['created_at'])).total_seconds() / 3600, 1) if first else None,
            'redirected_to_support': any('support@linear.app' in c['body'] for c in replies),
            'closed_by_stale_bot_unanswered': stale and not replies}


def main():
    items = json.loads((ROOT / 'data/questions/classified.json').read_text())
    with ThreadPoolExecutor(4) as ex:
        rows = list(ex.map(one, items))
    (ROOT / 'data/threads.json').write_text(json.dumps(rows, indent=1))
    print(len(rows), 'threads')


if __name__ == '__main__':
    main()
