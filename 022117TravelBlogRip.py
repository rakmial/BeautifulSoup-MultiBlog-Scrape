import codecs
import urllib
import pandas
from bs4 import BeautifulSoup
import csv

html_1 = urllib.urlopen('http://nomadicsamuel.com/top100travelblogs').read()
soup = BeautifulSoup(html_1, 'html.parser')

nomad_dict_list = []
for row in soup.find_all('tr'):
    row_batch = dict()
    span_ct = 0
    for datum in row.find_all('span'):
        if span_ct == 0:
            try:
                row_batch['nomadicsamuel_Rank'] = int(datum.get_text())
            except ValueError:
                row_batch['nomadicsamuel_Rank'] = 0
        elif span_ct == 1:
            row_batch['blog_name'] = datum.get_text().encode('utf-8').strip()
            td_parent = datum.parent
            try:
                nomad_subhtml = urllib.urlopen(td_parent['href']).read()
                nomad_sub_soup = BeautifulSoup(nomad_subhtml,'html.parser')
                for para in nomad_sub_soup.find_all('p'):
                    if para.get_text()[:6] == 'Follow':
                        try:
                            row_batch['blog_canon_link'] = para.a.get('href').encode('utf-8').strip()
                        except AttributeError:
                            row_batch['blog_canon_link'] = ''
            except KeyError:
                row_batch['blog_canon_link'] = ''
        elif span_ct == 2:
            try:
                row_batch['nomadicsamuel_Score'] = float(datum.get_text())
            except ValueError:
                row_batch['nomadicsamuel_Score'] = 0.
        span_ct += 1
    nomad_dict_list.append(row_batch)

keys = nomad_dict_list[0].keys()
with open(r'/run/media/jtl/OtherMind/_Neura/1. Upwork/2017.02.21 Travel Blog Scrapes/nomadic_samuel_files/blog_master.csv', 'wb') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(nomad_dict_list)
