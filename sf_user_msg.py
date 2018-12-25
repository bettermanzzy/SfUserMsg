from __future__ import print_function
import requests
import sys
import pandas as pd

BEARER_TOKEN = 'fbfd6b48b8c47c0c15d7'

if __name__ == '__main__':

    url_name = sys.argv[1]

    try:
        project_name = url_name.split('sourceforge.net/projects/')[1]
        project_name = project_name.split('/')[0]
    except:
        print("input error")

    url = 'https://sourceforge.net/rest/p/'+project_name

    r = requests.get(url,params={
        'access_token': BEARER_TOKEN,
        'ticket_form.summary': 'Test ticket',
        'ticket_form.description': 'This is a test ticket',
        'ticket_form.labels': 'test',
        'ticket_form.custom_fields._my_num': '7'})
    if r.status_code == 200:
        print('Ticket created at: %s' % r.url)
    else:
        print('Error [%s]:\n%s' % (r.status_code, r.text))

    name = []
    username = []
    url = []
    for  developer in r.json()['developers']:
        name.append(developer['name'])
        username.append(developer['username'])
        url.append(developer['url'])

    print('developers name ', name)
    print('developers username', username)
    print('developers url', url)

    dict = {'name': name,'username': username,'userurl': url}
    writer = pd.ExcelWriter(project_name + '.xlsx')
    df = pd.DataFrame(dict)
    df.to_excel(writer, columns=['name', 'username', 'userurl'], index=False,encoding='utf-8', sheet_name='Sheet')
    writer.save()
