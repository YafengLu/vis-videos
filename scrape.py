import requests
import json
import csv

# Get token from https://developer.vimeo.com/apps/136774#personal_access_tokens
# Under "Generate an access token", select "Authenticated (you)" then click on "Generate"
token = "YOUR_TOKEN_GOES_HERE"

videos = []

i = 1
while True:
    print("Loading page %s" % i)
    r = requests.get(f"https://api.vimeo.com/channels/721847/videos?page={i}", headers={"Authorization": f"bearer {token}"})
    d = json.loads(r.text)

    if 'error' in d.keys():
        break

    for v in d['data']:
        videos.append({'created_time': v['created_time'], 'description': v['description'], 'uri': v['uri'], 'name': v['name'] })

    i += 1


with open('all_videos.json', 'w') as outfile:
    json.dump(videos, outfile)



fails = 0
for i in range(0, len(videos)):
    event = False
    t = videos[i]['name'].upper()

    categories = ["VAST", "INFOVIS", "SCIVIS", "ARTS PROGRAM", "TUTORIAL", "KEYNOTE", "WORKSHOP", "PANEL", "CAPSTONE",
                 "BELIV", "VDS", "LDAV", "VAHC"]
    for category in categories:
        if category in t:
            event = category
            break

    if "VISAP" in t:
        event = "ARTS PROGRAM"

    if not event:
        #print t
        fails += 1
        event = ""

    if "30 SECOND VIDEO" in t or "PREVIEW" in t:
        if event:
            event = event + ", PREVIEW"
        else:
            event = "PREVIEW"

    videos[i]['year'] = videos[i]['created_time'].split('-')[0]
    videos[i]['event'] = event
    videos[i]['uri'] = videos[i]['uri'].replace('/videos', 'https://vimeo.com')


with open('vis_videos.json', 'w') as outfile:
    json.dump(videos, outfile)

csv_video_list = []
with open('videos.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)

    for v in videos:
        row = [v['year'], v['event'], v['name'], v['description'], v['uri'] ]
        map(lambda s: s.encode('ascii','ignore'), row)
        print row
        writer.writerow(row)



