#!/usr/bin/env python3
"""Text gate for the three personalised fields of a prospect list (observation, guess, question).

Usage: python3 check.py prospects.csv [-o checked.csv] [--today YYYY-MM-DD]

Adds three columns:
  text_gate     ok | review | general   (general = no observation, row goes to the generic segment)
  gate_reason   which of the nine conditions fired, in Ukrainian
  needs_human   conditions 6 and 8 that a script cannot decide: a person (or Claude) reads the source

Conditions come from the instruction «Персоналізований аутріч із трьох полів», section 6.
"""
import argparse
import csv
import datetime as dt
import re
import sys

ALIASES = {
    'observation': ['observation'],
    'guess': ['guess'],
    'question': ['question'],
    'confidence': ['confidence', 'впевненість'],
    'source_text': ['hook_source', 'basis', 'source_text', 'source', 'джерело зачіпки'],
    'source_date': ['source_date', 'дата джерела', 'date'],
}
BANNED = ['saw', 'i noticed', 'as a', 'impressive', 'exciting', 'reach out', 'hope this finds you',
          'leverage', 'solutions', 'partner with', 'thrilled', 'passionate']
BAD_START = ('saw', 'i saw', 'i noticed', 'hope')
ASKS_TIME = re.compile(r'\b(call|meeting|meet|chat|calendar|slot|zoom|hop on|book|minutes?|next week|'
                       r'monday|tuesday|wednesday|thursday|friday|\d{1,2}\s?(am|pm))\b', re.I)
NOW = re.compile(r'\b(now|right now|currently|this week|these days)\b', re.I)
STOP = set('a an the and or of to in on at for with your you yours their they it its is are was were be been '
           'this that these those i we my our has have had will would bet guessing odds likely probably '
           'already still while until so as by from up out about into than then there here what who how'.split())


def col(row, key):
    for name in ALIASES[key]:
        for k, v in row.items():
            if k and k.strip().lower() == name:
                return (v or '').strip()
    return ''


def parse_date(s):
    for fmt in ('%Y-%m-%d', '%d.%m.%Y', '%d/%m/%Y', '%Y/%m/%d'):
        try:
            return dt.datetime.strptime(s.strip()[:10], fmt).date()
        except ValueError:
            pass
    return None


def words(s):
    return re.findall(r"[A-Za-zА-Яа-яІіЇїЄєҐґʼ'’0-9-]+", s)


def content(s):
    return {w.lower().strip("'’ʼ") for w in words(s) if len(w) > 2 and w.lower() not in STOP}


def check(row, today):
    obs, guess, q = col(row, 'observation'), col(row, 'guess'), col(row, 'question')
    src, sdate = col(row, 'source_text'), col(row, 'source_date')
    if not obs:
        return 'general', '', ''
    r, human = [], []
    conf = col(row, 'confidence')
    try:
        if float(conf.replace(',', '.')) < 4:
            r.append(f'1: впевненість {conf}')
    except ValueError:
        r.append('1: немає впевненості')
    n = len(words(obs))
    if n < 10 or n > 25:
        r.append(f'2: observation {n} слів')
    if not guess:
        r.append('3: guess порожній')
    if obs.lower().lstrip('"“ ').startswith(BAD_START):
        r.append('4: заборонене перше слово')
    text = ' '.join((obs, guess, q)).lower()
    hits = [b for b in BANNED if re.search(r'\b' + re.escape(b) + r'\b', text)]
    if hits:
        r.append('5: ' + ', '.join(hits))
    if not src:
        human.append('6: немає тексту джерела, перевірити')
    elif len([w for w in words(src) if re.fullmatch(r'[A-Za-zА-Яа-яІіЇїЄєҐґ]{4,}', w)]) < 2:
        r.append('6: у джерелі лише номер або код')
    if not q:
        human.append('question порожній')
    elif ASKS_TIME.search(q):
        r.append('7: question просить дзвінок або час')
    if guess and not (content(obs) & content(guess)):
        human.append('8: observation і guess без спільних слів, звірити обʼєкт')
    d = parse_date(sdate) if sdate else None
    if not d:
        r.append('9: немає дати джерела')
    elif (today - d).days > 183 and NOW.search(guess):
        r.append(f'9: джерелу {(today - d).days} днів, а guess пише now')
    return ('review' if r else 'ok'), '; '.join(r), '; '.join(human)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('csv')
    ap.add_argument('-o', '--out')
    ap.add_argument('--today')
    a = ap.parse_args()
    today = parse_date(a.today) if a.today else dt.date.today()
    with open(a.csv, newline='', encoding='utf-8-sig') as f:
        rows = list(csv.DictReader(f))
    if not rows:
        sys.exit('порожній файл')
    if not any(k and k.strip().lower() == 'observation' for k in rows[0]):
        sys.exit('немає колонки observation')
    out = a.out or a.csv.rsplit('.', 1)[0] + '.checked.csv'
    fields = list(rows[0].keys()) + [c for c in ('text_gate', 'gate_reason', 'needs_human') if c not in rows[0]]
    stats = {'ok': 0, 'review': 0, 'general': 0}
    human = 0
    for row in rows:
        g, reason, h = check(row, today)
        row.update(text_gate=g, gate_reason=reason, needs_human=h)
        stats[g] += 1
        human += bool(h)
    with open(out, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    print(f"рядків {len(rows)} · ok {stats['ok']} · review {stats['review']} · general {stats['general']} · людині {human}")
    print(out)


if __name__ == '__main__':
    main()
