# -*- coding: utf-8 -*-
import datetime

'''fin = open('C:\Users\cc\Desktop/imdb_s/imdb_s.csv')
fout1 = open('C:\Users\cc\Desktop/imdb_s/actors.txt','w')
fout2 = open('C:\Users\cc\Desktop/imdb_s/imdb_s.txt','w')
fin = open('C:\Users\cc\Desktop/imdb_b/imdb_b.csv')
fout1 = open('C:\Users\cc\Desktop/imdb_b/actors.txt','w')
fout2 = open('C:\Users\cc\Desktop/imdb_b/imdb_b.txt','w')
movies = {}
actorid = {}
fin.readline()
fin.readline()
aid = 0
for line in fin:
	x = str(line).split(',')
	movie = x[0].strip()
	actor = x[1].strip()
	if actor not in actorid:
		aid += 1
		actorid[actor] = aid
	if movie not in movies:
		movies[movie] = set()
	movies[movie].add(actorid[actor])
for item in sorted(actorid.iteritems(),key=lambda d:d[1],reverse=False):
	fout1.write(str(item[1]) + '\t' + item[0] + '\n')
for movie in movies:
	actors = list(movies[movie])
	for i in range(len(actors)):
		for j in range(i+1,len(actors)):
			fout2.write(str(actors[i]) + '\t' + str(actors[j]) + '\t' + movie[-4:] + '\n')
fin.close()
fout1.close()
fout2.close()'''

fin = open('C:\Users\cc\Desktop/mail/maildir.txt')
fout1 = open('C:\Users\cc\Desktop/mail/address.txt','w')
fout2 = open('C:\Users\cc\Desktop/mail/mails.txt','w')
addressid = {}
aid = 0
miny = 9999
maxy = 0
for line in fin:
	x = str(line).split('    ')
	a1 = x[0]
	a2 = x[1]
	if a1 not in addressid:
		aid += 1
		addressid[a1] = aid
	if a2 not in addressid:
		aid += 1
		addressid[a2] = aid
	fout2.write(str(addressid[a1]) + '\t' + str(addressid[a2]) + '\t' + x[2])
	t = datetime.datetime.strptime(x[2][:-13],'%a, %d %b %Y %H:%M:%S')
	miny = min(miny, t.year)
	maxy = max(maxy, t.year)
fout2.close()
print miny,maxy
for item in sorted(addressid.iteritems(),key=lambda d:d[1],reverse=False):
	fout1.write(item[0] + '\t' + str(item[1]) + '\n')
fout1.close()