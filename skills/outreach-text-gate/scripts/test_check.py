"""Self-check: python3 test_check.py"""
import datetime as dt
from check import check

T = dt.date(2026, 11, 15)
SRC = 'Senior Backend Engineer, legacy payments module, posted 2026-09-02'
good = {'observation': 'Your Senior Backend post has been open for 65 days, and it names a legacy payments module.',
        'guess': 'I bet the payments release is already slipping while that seat stays empty.',
        'question': 'Who is covering payments work until the role is filled?',
        'confidence': '5', 'hook_source': SRC, 'source_date': '2026-09-02'}
assert check(good, T) == ('ok', '', ''), check(good, T)

bad = dict(good, observation='Saw your impressive company is hiring.', confidence='3',
           question='Do you have 15 minutes on Tuesday for a call?', guess='', source_date='2026-01-10',
           hook_source='JOB-4471')
g, r, h = check(bad, T)
assert g == 'review'
for n in ('1:', '2:', '3:', '4:', '5:', '6:', '7:'):
    assert n in r, (n, r)

old = dict(good, source_date='2026-03-01', guess='I bet the payments release is slipping right now while that seat stays empty.')
assert '9:' in check(old, T)[1]
drift = dict(good, guess='I bet your mobile app reviews keep dropping after the redesign.')
assert '8:' in check(drift, T)[2]
assert check(dict(good, observation=''), T)[0] == 'general'
print('ok')
