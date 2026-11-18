#!/usr/bin/env python3
"""Render profile cards from GitHub GraphQL; API failures keep the last good SVGs."""
import argparse
import datetime as dt
import json
import os
from pathlib import Path
import urllib.request
from design_profile import THEMES, text, svg

ROOT = Path(__file__).resolve().parents[1]

def graphql(query, variables, token):
    request = urllib.request.Request('https://api.github.com/graphql',
        data=json.dumps({'query':query,'variables':variables}).encode(),
        headers={'Authorization':f'Bearer {token}', 'Content-Type':'application/json',
                 'User-Agent':'Bhavish-S-profile-cards'})
    with urllib.request.urlopen(request, timeout=45) as response:
        result=json.load(response)
    if result.get('errors'):
        raise RuntimeError('GitHub GraphQL request failed: '+str(result['errors']))
    return result['data']

def fetch(login, token):
    data=graphql('''query($login:String!){user(login:$login){login
      followers{totalCount} repositories(privacy:PUBLIC,ownerAffiliations:OWNER){totalCount}
      contributionsCollection{contributionCalendar{totalContributions weeks{contributionDays{date contributionCount contributionLevel}}}}
    }}''', {'login':login},token)['user']
    if not data:
        raise RuntimeError('GitHub account not found')
    repos=[]; cursor=None
    while True:
        page=graphql('''query($login:String!,$cursor:String){user(login:$login){repositories(first:100,after:$cursor,privacy:PUBLIC,ownerAffiliations:OWNER,isFork:false){
          nodes{stargazerCount languages(first:100){edges{size node{name color}}}}
          pageInfo{hasNextPage endCursor}
        }}}''',{'login':login,'cursor':cursor},token)['user']['repositories']
        repos.extend(page['nodes'])
        if not page['pageInfo']['hasNextPage']:break
        cursor=page['pageInfo']['endCursor']
    data['publicRepositories']=repos
    data['generatedAt']=dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    return data

def frame(c,title,subtitle,height,body):
    return svg(900,height,title,
        f'<rect x=".5" y=".5" width="899" height="{height-1}" rx="12" fill="{c["bg"]}" stroke="{c["line"]}"/>'
        +text(28,35,title,17,c['ink'],700)+text(28,58,subtitle,11,c['muted'],mono=True)+body)

def render(data):
    repos=data['publicRepositories'];calendar=data['contributionsCollection']['contributionCalendar']
    langs={};colors={}
    for repo in repos:
        for edge in repo['languages']['edges']:
            name=edge['node']['name']; langs[name]=langs.get(name,0)+edge['size'];colors[name]=edge['node']['color'] or '#89e9b5'
    ordered=sorted(langs.items(),key=lambda kv:kv[1],reverse=True)
    total=sum(langs.values()); generated={}
    for theme,c in THEMES.items():
        body=''
        metrics=[('Public repositories',data['repositories']['totalCount']),('Followers',data['followers']['totalCount']),('Stars · non-fork repos',sum(r['stargazerCount'] for r in repos)),('Contributions · past year',calendar['totalContributions'])]
        for i,(label,value) in enumerate(metrics):
            x=28+i*218
            body+=text(x,116,f'{value:,}',34,c['accent'],700)+text(x,142,label,12,c['muted'])
        generated[f'overview.{theme}.svg']=frame(c,'GitHub / account overview',data['login']+' · '+data['generatedAt'],168,body)
        body=''
        palette=([c['faint'],'#174d38','#20734d','#39a16b','#89e9b5'] if theme=='dark' else [c['faint'],'#c2e7cb','#81c99d','#42a46b','#18734d'])
        levels=['NONE','FIRST_QUARTILE','SECOND_QUARTILE','THIRD_QUARTILE','FOURTH_QUARTILE']
        for w,week in enumerate(calendar['weeks']):
            for day in week['contributionDays']:
                date=dt.date.fromisoformat(day['date']);row=(date.weekday()+1)%7
                color=palette[levels.index(day['contributionLevel'])]
                body+=f'<rect x="{28+w*16}" y="{80+row*16}" width="12" height="12" rx="3" fill="{color}"><title>{day["date"]}: {day["contributionCount"]} contributions</title></rect>'
        body+=text(28,216,'Past year · GitHub contribution calendar',12,c['muted'])
        generated[f'contributions.{theme}.svg']=frame(c,'Contribution activity',data['generatedAt'],240,body)
        body='';x=28;visible=ordered[:6]
        if len(ordered)>6:visible.append(('Other',sum(n for _,n in ordered[6:])))
        for name,value in visible:
            width=844*value/total if total else 0
            body+=f'<rect x="{x:.2f}" y="80" width="{width:.2f}" height="12" fill="{colors.get(name,c["muted"])}"/>'
            x+=width
        for i,(name,value) in enumerate(visible):
            x=28+(i%3)*286;y=124+(i//3)*28
            body+=f'<circle cx="{x+4}" cy="{y-4}" r="4" fill="{colors.get(name,c["muted"])}"/>'
            body+=text(x+16,y,f'{name}  {100*value/total:.1f}%',13,c['ink'])
        if not total:body+=text(28,115,'No public repository language data available.',14,c['muted'])
        generated[f'languages.{theme}.svg']=frame(c,'Language breakdown','Code bytes · public repositories owned by '+data['login']+' · forks excluded',212,body)
    return generated

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--data',type=Path);args=parser.parse_args()
    if args.data:data=json.loads(args.data.read_text())
    else:
        token=os.environ.get('GITHUB_TOKEN')
        if not token:raise SystemExit('GITHUB_TOKEN is required; existing cards were not changed.')
        data=fetch(os.environ.get('PROFILE_USERNAME','Bhavish-S'),token)
    generated=render(data)
    for name,content in generated.items():
        (ROOT/'assets/stats'/name).write_text(content)
    print('Updated six profile cards from GitHub account data.')

if __name__=='__main__':main()
