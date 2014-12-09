from bs4 import BeautifulSoup
import requests
import csv
import urllib

with open('data/FY14_Student_Racial_Ethnic_Report_20140328.csv', 'rU') as csvinput:
    with open('data/data.csv', 'w') as csvoutput:
        writer = csv.writer(csvoutput, lineterminator='\n')
        reader = csv.reader(csvinput)

        all = []
        row = next(reader)
        row.append('lat')
        row.append('lng')
        all.append(row)

        for row in reader:
            url = 'http://schoolinfo.cps.edu/schoolprofile/SchoolDetails.aspx?SchoolId=' + row[1]
            r = requests.get(url)
            soup = BeautifulSoup(r.content, "html.parser")
            street = soup.find('span', {'id': 'ctl00_ContentPlaceHolder1_lbAddress'})
            city = soup.find('span', {'id': 'ctl00_ContentPlaceHolder1_lbCSZ'})
            if street and city:
                address = street.text + ' ' + city.text
                request_url = 'https://maps.googleapis.com/maps/api/geocode/json?'
                request_url += urllib.urlencode({'address': address})
                a = requests.get(request_url)
                data = a.json()
                lat = data['results'][0]['geometry']['location']['lat']
                lng = data['results'][0]['geometry']['location']['lng']
                row.append(lat)
                row.append(lng)
                print row
                all.append(row)

        writer.writerows(all)
