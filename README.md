Twitter Most Followed
=====================

Rationale
---------

**How to Find Out Who's Popular on Twitter.** And why there's no point in doing it

> That’s easy. You just look at the number of followers, and you’ll get @katyperry, @justinbieber, and @BarackObama — the top most followed accounts in the whole Twitterverse. No surprise there, right?

> But what if you want to focus on a particular group of Twitter users, for example the Hacker News community? Who’s in the top most followed accounts by the HNers? This is not a trivial exercise, we need a different approach, but if you’re a HNer, the result will be just as predictable.

Read the whole story here: https://medium.com/@ducu/d659884fd942


Approach
--------

Let's take the Hacker News community as our target group.

There's a Twitter account named [@newsyc20](http://twitter.com/newsyc20/) (Hacker News 20 - "Tweeting Hacker News stories as soon as they reach 20 points."). We consider this as our **source**, and the followers of @newsyc20 as the HNers, our **target group**. To find out the top most followed accounts by our target group members, we get the complete lists of who each of them is following (aka friends), and we aggregate all these lists, counting the occurences of each friend.

You can realize that the most followed account will be exactly @newsyc20, because all the members are following it. But who's on the 2nd and 3rd place? Who's in the top 100 most followed? This is what we're going to find out by running the routine below, a transcript from [main.py](https://github.com/ducu/twitter-most-followed/blob/master/main.py)


``` python
# Step 1: Specify the source
source_name = 'newsyc20' # target group source
source_id, source_data = load_user_data(screen_name=source_name)

# Step 2: Load target group members
followers = load_followers(source_id) # target group

# Step 3: Load friends of target group members
for follower_id in followers:
	load_friends(user_id=follower_id)

# Step 4: Aggregate friends into top most followed
aggregate_friends() # count friend occurences
top_most_followed(100) # display results
```


Requirements
------------

The Python script in this repo uses [Twitter REST API](https://dev.twitter.com/docs/api/1.1) to get the data, and [Redis](http://redis.io/) to store and aggregate it. To use Twitter API you need [an existing application](https://apps.twitter.com/), and [some access tokens](https://dev.twitter.com/docs/auth/obtaining-access-tokens).

There are a couple of performance issues though when dealing with big data sets.

**Twitter API Rate Limits**

We have 13.3K members in our HNers target group. In order to load the friends for each of these members (step 3), we're calling the Twitter API [friends/ids](https://dev.twitter.com/docs/api/1.1/get/friends/ids) method. This method is rate limited at 15 calls/15 minutes/token. We have to perform about 15.3K calls, since one call returns at most 5000 items. The problem is that with a single access token, it would take 10 days and 16 hours to get all this data.

[Tweepy](https://github.com/tweepy/tweepy/) is the preferred Twitter API client for Python, and the current release works with a single access token. But here's a fork I created especially to extend Tweepy so it works with several access tokens in a round robin fashion transparently - https://github.com/svven/tweepy. Using about four dozen tokens, the overall retrieval time was reduced to 5 hours (2 hours work time, 3 hours sleep). With about hundred tokens added to `RateLimitHandler`, you would get maximum efficiency out of a single Tweepy API object. See how it's done in `get_api()` from [twitter.py](https://github.com/ducu/twitter-most-followed/blob/master/twitter.py).

**Redis ZUNIONSTORE**

After storing all this data, we have about 12.4K simple sets of friend ids in Redis, one set for each of our target group members. We are short of almost 1K sets because there are that many protected Twitter accounts so we cannot get their friends from Twitter API. There's an average of 1.3K items per set, ranging from 1 to 8.6M maximum items, a total of 16.2M items.

Aggregating all these sets can be easily done using the ZUNIONSTORE command with the default weight of 1. See `RedisStorage.set_most_followed()` method in [storage.py](https://github.com/ducu/twitter-most-followed/blob/master/storage.py). The problem is that for this workload, ZUNIONSTORE took more than 1 hour to execute on my 4GB machine. That was surprisingly slow, having a recent stable release of Redis, ver 2.8.9.

It turned out that a [performance patch](https://github.com/antirez/redis/pull/1786) for this command has been recently added, but it is only available in the beta 8 release of Redis, ver 3.0.0. You can read about it in the [release notes](https://raw.githubusercontent.com/antirez/redis/3.0/00-RELEASENOTES). Having installed this, running the ZUNIONSTORE on the same data set took less than 2 minutes.

---

To conclude, in order to run this exercise for a big data set, make sure you have a bunch of access tokens that you can use in [config.py](https://github.com/ducu/twitter-most-followed/blob/master/config.py), and install [Redis 3.0.0 beta 8](https://github.com/antirez/redis/archive/3.0.0-beta8.tar.gz). Then `pip install -r requirements.txt` in your [virtualenv](http://virtualenv.readthedocs.org/en/latest/virtualenv.html) so you have following packages

```
hiredis==0.1.4
redis==2.10.1
git+https://github.com/svven/tweepy.git#egg=tweepy
```


Credits
-------

Thanks to Jeff Miller ([@JeffMiller](https://twitter.com/JeffMiller)) for @newsyc20. It's one of the best Hacker News Twitter bots. Jeff actually did a similar analysis on the Hacker News community, but with a slightly different [approach](http://talkfast.org/2010/07/28/twitter-users-most-followed-by-readers-of-hacker-news/).

Many thanks also to Josiah Carlson ([@dr_josiah](https://twitter.com/dr_josiah)) for his valuable support on Redis related issues.


Results
-------

Finally here's the top 100 most followed accounts by the Hacker News community.
Popularity equals the number of followers only from within our HNers target group.

Rank | Popularity | Name | Twitter | Followers | Friends
--- | --- | --- | --- | --- | ---
1 | 12476 | Hacker News 20 | [@newsyc20](http://twitter.com/newsyc20) | 13377 | 0
2 | 5266 | TechCrunch | [@TechCrunch](http://twitter.com/TechCrunch) | 3781036 | 872
3 | 4600 | Bill Gates | [@BillGates](http://twitter.com/BillGates) | 17099119 | 165
4 | 3921 | A Googler | [@google](http://twitter.com/google) | 8836866 | 411
5 | 3890 | WIRED | [@WIRED](http://twitter.com/WIRED) | 3115526 | 72
6 | 3562 | Twitter | [@twitter](http://twitter.com/twitter) | 31793932 | 131
7 | 3488 | Mashable | [@mashable](http://twitter.com/mashable) | 4289712 | 2773
8 | 3410 | The Hacker News | [@TheHackersNews](http://twitter.com/TheHackersNews) | 151838 | 2197
9 | 3219 | Barack Obama | [@BarackObama](http://twitter.com/BarackObama) | 45567454 | 648558
10 | 2926 | Lifehacker | [@lifehacker](http://twitter.com/lifehacker) | 1436383 | 39
11 | 2894 | The New York Times | [@nytimes](http://twitter.com/nytimes) | 12847085 | 985
12 | 2774 | Tim O'Reilly | [@timoreilly](http://twitter.com/timoreilly) | 1789255 | 1234
13 | 2666 | The Economist | [@TheEconomist](http://twitter.com/TheEconomist) | 5679068 | 111
14 | 2652 | Jack | [@jack](http://twitter.com/jack) | 2618138 | 1195
15 | 2615 | Paul Graham | [@paulg](http://twitter.com/paulg) | 182848 | 107
16 | 2604 | Elon Musk | [@elonmusk](http://twitter.com/elonmusk) | 864374 | 36
17 | 2528 | The Next Web | [@TheNextWeb](http://twitter.com/TheNextWeb) | 1161272 | 1164
18 | 2490 | YouTube | [@YouTube](http://twitter.com/YouTube) | 44628570 | 823
19 | 2464 | CNN Breaking News | [@cnnbrk](http://twitter.com/cnnbrk) | 18354871 | 108
20 | 2451 | GitHub | [@github](http://twitter.com/github) | 340889 | 184
21 | 2429 | TED Talks | [@TEDTalks](http://twitter.com/TEDTalks) | 3112388 | 299
22 | 2414 | Hacker News Bot | [@hackernewsbot](http://twitter.com/hackernewsbot) | 25807 | 0
23 | 2410 | Wall Street Journal | [@WSJ](http://twitter.com/WSJ) | 4893760 | 914
24 | 2362 | Ars Technica | [@arstechnica](http://twitter.com/arstechnica) | 713304 | 134
25 | 2361 | Hacker News Network | [@ThisIsHNN](http://twitter.com/ThisIsHNN) | 36302 | 332
26 | 2353 | NASA | [@NASA](http://twitter.com/NASA) | 7330317 | 226
27 | 2351 | Kevin Rose | [@kevinrose](http://twitter.com/kevinrose) | 1471424 | 566
28 | 2338 | marissamayer | [@marissamayer](http://twitter.com/marissamayer) | 650732 | 331
29 | 2309 | Eric Schmidt | [@ericschmidt](http://twitter.com/ericschmidt) | 852540 | 207
30 | 2300 | Y Combinator | [@ycombinator](http://twitter.com/ycombinator) | 169518 | 111
31 | 2272 | Dropbox | [@Dropbox](http://twitter.com/Dropbox) | 3654098 | 102
32 | 2160 | VentureBeat | [@VentureBeat](http://twitter.com/VentureBeat) | 327636 | 1445
33 | 2116 | Robert Scoble | [@Scobleizer](http://twitter.com/Scobleizer) | 410004 | 43534
34 | 2098 | Fast Company | [@FastCompany](http://twitter.com/FastCompany) | 1261958 | 3892
35 | 2058 | Household Hacker | [@householdhacker](http://twitter.com/householdhacker) | 55299 | 120
36 | 2049 | Richard Branson | [@richardbranson](http://twitter.com/richardbranson) | 4364135 | 3848
37 | 2046 | ReadWrite | [@RWW](http://twitter.com/RWW) | 1420148 | 2634
38 | 2032 | Forbes Tech News | [@ForbesTech](http://twitter.com/ForbesTech) | 1315334 | 16407
39 | 2027 | Engadget | [@engadget](http://twitter.com/engadget) | 1051259 | 95
40 | 2006 | Instagram | [@instagram](http://twitter.com/instagram) | 34642373 | 17
41 | 1999 | Fred Wilson | [@fredwilson](http://twitter.com/fredwilson) | 348795 | 897
42 | 1987 | Gizmodo | [@Gizmodo](http://twitter.com/Gizmodo) | 1027214 | 78
43 | 1984 | Ev Williams | [@ev](http://twitter.com/ev) | 1738702 | 1677
44 | 1981 | Harvard Biz Review | [@HarvardBiz](http://twitter.com/HarvardBiz) | 1648398 | 181
45 | 1965 | WikiLeaks | [@wikileaks](http://twitter.com/wikileaks) | 2343719 | 1
46 | 1956 | Medium | [@Medium](http://twitter.com/Medium) | 673992 | 108
47 | 1947 | Biz Stone | [@biz](http://twitter.com/biz) | 2182676 | 624
48 | 1939 | BBC Breaking News | [@BBCBreaking](http://twitter.com/BBCBreaking) | 10964049 | 3
49 | 1912 | Dave McClure | [@davemcclure](http://twitter.com/davemcclure) | 233408 | 13254
50 | 1905 | Google Developers | [@googledevs](http://twitter.com/googledevs) | 1011590 | 137
51 | 1893 | Walt Mossberg | [@waltmossberg](http://twitter.com/waltmossberg) | 599434 | 585
52 | 1892 | The Verge | [@verge](http://twitter.com/verge) | 525973 | 115
53 | 1881 | Breaking News | [@BreakingNews](http://twitter.com/BreakingNews) | 6846181 | 495
54 | 1878 | Forbes | [@Forbes](http://twitter.com/Forbes) | 3506893 | 4727
55 | 1865 | The Onion | [@TheOnion](http://twitter.com/TheOnion) | 6112103 | 12
56 | 1852 | Om Malik | [@om](http://twitter.com/om) | 1393171 | 1482
57 | 1850 | Conan O'Brien | [@ConanOBrien](http://twitter.com/ConanOBrien) | 11566965 | 1
58 | 1848 | Hacker News | [@newsycombinator](http://twitter.com/newsycombinator) | 80316 | 1
59 | 1840 | Facebook | [@facebook](http://twitter.com/facebook) | 13892218 | 89
60 | 1810 | Gigaom | [@gigaom](http://twitter.com/gigaom) | 251664 | 26
61 | 1799 | Guardian Tech | [@guardiantech](http://twitter.com/guardiantech) | 2249638 | 23233
62 | 1797 | Chris Dixon | [@cdixon](http://twitter.com/cdixon) | 139903 | 951
63 | 1793 | Hacker Fantastic | [@hackerfantastic](http://twitter.com/hackerfantastic) | 13275 | 3390
64 | 1789 | CNN | [@CNN](http://twitter.com/CNN) | 13746311 | 975
65 | 1777 | Techmeme | [@Techmeme](http://twitter.com/Techmeme) | 212578 | 3
66 | 1777 | Reuters Top News | [@Reuters](http://twitter.com/Reuters) | 4833004 | 1042
67 | 1741 | Hootsuite | [@hootsuite](http://twitter.com/hootsuite) | 6083682 | 1614005
68 | 1740 | Android | [@Android](http://twitter.com/Android) | 5930546 | 26
69 | 1707 | Dalai Lama | [@DalaiLama](http://twitter.com/DalaiLama) | 9264066 | 0
70 | 1701 | Eric Ries | [@ericries](http://twitter.com/ericries) | 180266 | 731
71 | 1696 | Michael Arrington | [@arrington](http://twitter.com/arrington) | 188864 | 1707
72 | 1684 | TIME.com | [@TIME](http://twitter.com/TIME) | 6112812 | 772
73 | 1664 | 500 Startups | [@500Startups](http://twitter.com/500Startups) | 216829 | 1918
74 | 1618 | BBC News (World) | [@BBCWorld](http://twitter.com/BBCWorld) | 7118939 | 61
75 | 1613 | The New Yorker | [@NewYorker](http://twitter.com/NewYorker) | 3398866 | 268
76 | 1605 | Jeff Atwood | [@codinghorror](http://twitter.com/codinghorror) | 142123 | 160
77 | 1601 | Marc Andreessen | [@pmarca](http://twitter.com/pmarca) | 157463 | 4070
78 | 1601 | Reid Hoffman | [@reidhoffman](http://twitter.com/reidhoffman) | 213855 | 435
79 | 1583 | Chris Anderson | [@TEDchris](http://twitter.com/TEDchris) | 1587947 | 533
80 | 1560 | Microsoft | [@Microsoft](http://twitter.com/Microsoft) | 5232083 | 1165
81 | 1560 | Kara Swisher | [@karaswisher](http://twitter.com/karaswisher) | 964180 | 1013
82 | 1556 | dick costolo | [@dickc](http://twitter.com/dickc) | 1222127 | 490
83 | 1556 | Chris Sacca | [@sacca](http://twitter.com/sacca) | 1466482 | 799
84 | 1554 | Stephen Colbert | [@StephenAtHome](http://twitter.com/StephenAtHome) | 6826374 | 1
85 | 1552 | Smashing Magazine | [@smashingmag](http://twitter.com/smashingmag) | 808219 | 1159
86 | 1552 | DHH | [@dhh](http://twitter.com/dhh) | 119710 | 184
87 | 1545 | Neil deGrasse Tyson | [@neiltyson](http://twitter.com/neiltyson) | 2312490 | 44
88 | 1529 | Mark Suster | [@msuster](http://twitter.com/msuster) | 170710 | 694
89 | 1528 | Anonymous | [@YourAnonNews](http://twitter.com/YourAnonNews) | 1306755 | 873
90 | 1527 | Mark Cuban | [@mcuban](http://twitter.com/mcuban) | 2356613 | 766
91 | 1523 | Google Chrome | [@googlechrome](http://twitter.com/googlechrome) | 4373502 | 85
92 | 1522 | Venture Hacks | [@venturehacks](http://twitter.com/venturehacks) | 119780 | 3
93 | 1506 | MG Siegler | [@parislemon](http://twitter.com/parislemon) | 149725 | 998
94 | 1503 | John Resig | [@jeresig](http://twitter.com/jeresig) | 158058 | 3044
95 | 1496 | Hacker News 100 | [@newsyc100](http://twitter.com/newsyc100) | 6188 | 0
96 | 1484 | News.YC | [@HackerNews](http://twitter.com/HackerNews) | 15775 | 2
97 | 1468 | Hacker News 50 | [@newsyc50](http://twitter.com/newsyc50) | 4981 | 0
98 | 1463 | Google Ventures | [@GoogleVentures](http://twitter.com/GoogleVentures) | 258575 | 199
99 | 1451 | Matt Cutts | [@mattcutts](http://twitter.com/mattcutts) | 366656 | 370
100 | 1451 | Huffington Post | [@HuffingtonPost](http://twitter.com/HuffingtonPost) | 4504186 | 5558

