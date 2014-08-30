Twitter Most Followed
=====================

Rationale
---------

**How to Find Out Who's Popular on Twitter.** And why there's no point in doing it

> It’s easy if you consider the whole Twitterverse. You just look at the number of followers, and you’ll get @katyperry, @justinbieber, and @BarackObama. No surprise there, right?

> But what if you want to focus on a particular group of Twitter users? Let’s take the Hacker News community. Who’s in the top most followed accounts by the HNers? This is not a trivial exercise, we need a different approach, but if you're a HNer, the result will be just as predictable.

Read the whole story here: https://medium.com/@ducu/d659884fd942


Approach
--------

Let's take the Hacker News community as our target group.

There is a Twitter account named [@newsyc20](https://twitter.com/newsyc20/) (Hacker News 20 - "Tweeting Hacker News stories as soon as they reach 20 points."). We consider this as our **source**, and the followers of @newsyc20 as the HNers, our **target group**. To find out the top most followed accounts by our target group members, we get the complete lists of who each of them is following (aka friends), then we aggregate all those lists, counting the occurrences of each friend.

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
aggregate_friends() # count friend occurrences
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

Aggregating all these sets can be easily done using the [ZUNIONSTORE](http://redis.io/commands/ZUNIONSTORE) command with the default weight of 1. See `RedisStorage.set_most_followed()` method in [storage.py](https://github.com/ducu/twitter-most-followed/blob/master/storage.py). The problem is that for this workload, ZUNIONSTORE took more than 1 hour to execute on my 4GB machine. That was surprisingly slow, having a recent stable release of Redis, ver 2.8.9.

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

Followers and Friends columns show the total count.<br>
Popularity equals the number of followers only from within our HNers target group. The results are ranked by this value. Protected Twitter accounts were not considered, that's where the difference between @newsyc20 popularity (12476) and followers count (13377) is coming from.

I created a Twitter list with this top 100 for your convenience.
You can subscribe to it here - https://twitter.com/ducu/lists/hners-most-followed

[Drop me a line](mailto:alexandru.stanciu@gmail.com?Subject=Twitter%20Most%20Followed) if you want more data, I have the complete top HNers' most followed, or if you need any help running this exercise. You can easily change the starting source, just replace 'newsyc20' in main.py with any other Twitter handle, and find out the results for yourself.

Cheers, [@ducu](https://twitter.com/ducu)

Rank | Popularity | Followers | Friends | Name (@twitter)
--- | --- | --- | --- | ---
1 | 12476 | 13377 | 0 | Hacker News 20 ([@newsyc20](https://twitter.com/newsyc20))
2 | 5266 | 3781036 | 872 | TechCrunch ([@TechCrunch](https://twitter.com/TechCrunch))
3 | 4600 | 17099119 | 165 | Bill Gates ([@BillGates](https://twitter.com/BillGates))
4 | 3921 | 8836866 | 411 | A Googler ([@google](https://twitter.com/google))
5 | 3890 | 3115526 | 72 | WIRED ([@WIRED](https://twitter.com/WIRED))
6 | 3562 | 31793932 | 131 | Twitter ([@twitter](https://twitter.com/twitter))
7 | 3488 | 4289712 | 2773 | Mashable ([@mashable](https://twitter.com/mashable))
8 | 3410 | 151838 | 2197 | The Hacker News ([@TheHackersNews](https://twitter.com/TheHackersNews))
9 | 3219 | 45567454 | 648558 | Barack Obama ([@BarackObama](https://twitter.com/BarackObama))
10 | 2926 | 1436383 | 39 | Lifehacker ([@lifehacker](https://twitter.com/lifehacker))
11 | 2894 | 12847085 | 985 | The New York Times ([@nytimes](https://twitter.com/nytimes))
12 | 2774 | 1789255 | 1234 | Tim O'Reilly ([@timoreilly](https://twitter.com/timoreilly))
13 | 2666 | 5679068 | 111 | The Economist ([@TheEconomist](https://twitter.com/TheEconomist))
14 | 2652 | 2618138 | 1195 | Jack ([@jack](https://twitter.com/jack))
15 | 2615 | 182848 | 107 | Paul Graham ([@paulg](https://twitter.com/paulg))
16 | 2604 | 864374 | 36 | Elon Musk ([@elonmusk](https://twitter.com/elonmusk))
17 | 2528 | 1161272 | 1164 | The Next Web ([@TheNextWeb](https://twitter.com/TheNextWeb))
18 | 2490 | 44628570 | 823 | YouTube ([@YouTube](https://twitter.com/YouTube))
19 | 2464 | 18354871 | 108 | CNN Breaking News ([@cnnbrk](https://twitter.com/cnnbrk))
20 | 2451 | 340889 | 184 | GitHub ([@github](https://twitter.com/github))
21 | 2429 | 3112388 | 299 | TED Talks ([@TEDTalks](https://twitter.com/TEDTalks))
22 | 2414 | 25807 | 0 | Hacker News Bot ([@hackernewsbot](https://twitter.com/hackernewsbot))
23 | 2410 | 4893760 | 914 | Wall Street Journal ([@WSJ](https://twitter.com/WSJ))
24 | 2362 | 713304 | 134 | Ars Technica ([@arstechnica](https://twitter.com/arstechnica))
25 | 2361 | 36302 | 332 | Hacker News Network ([@ThisIsHNN](https://twitter.com/ThisIsHNN))
26 | 2353 | 7330317 | 226 | NASA ([@NASA](https://twitter.com/NASA))
27 | 2351 | 1471424 | 566 | Kevin Rose ([@kevinrose](https://twitter.com/kevinrose))
28 | 2338 | 650732 | 331 | marissamayer ([@marissamayer](https://twitter.com/marissamayer))
29 | 2309 | 852540 | 207 | Eric Schmidt ([@ericschmidt](https://twitter.com/ericschmidt))
30 | 2300 | 169518 | 111 | Y Combinator ([@ycombinator](https://twitter.com/ycombinator))
31 | 2272 | 3654098 | 102 | Dropbox ([@Dropbox](https://twitter.com/Dropbox))
32 | 2160 | 327636 | 1445 | VentureBeat ([@VentureBeat](https://twitter.com/VentureBeat))
33 | 2116 | 410004 | 43534 | Robert Scoble ([@Scobleizer](https://twitter.com/Scobleizer))
34 | 2098 | 1261958 | 3892 | Fast Company ([@FastCompany](https://twitter.com/FastCompany))
35 | 2058 | 55299 | 120 | Household Hacker ([@householdhacker](https://twitter.com/householdhacker))
36 | 2049 | 4364135 | 3848 | Richard Branson ([@richardbranson](https://twitter.com/richardbranson))
37 | 2046 | 1420148 | 2634 | ReadWrite ([@RWW](https://twitter.com/RWW))
38 | 2032 | 1315334 | 16407 | Forbes Tech News ([@ForbesTech](https://twitter.com/ForbesTech))
39 | 2027 | 1051259 | 95 | Engadget ([@engadget](https://twitter.com/engadget))
40 | 2006 | 34642373 | 17 | Instagram ([@instagram](https://twitter.com/instagram))
41 | 1999 | 348795 | 897 | Fred Wilson ([@fredwilson](https://twitter.com/fredwilson))
42 | 1987 | 1027214 | 78 | Gizmodo ([@Gizmodo](https://twitter.com/Gizmodo))
43 | 1984 | 1738702 | 1677 | Ev Williams ([@ev](https://twitter.com/ev))
44 | 1981 | 1648398 | 181 | Harvard Biz Review ([@HarvardBiz](https://twitter.com/HarvardBiz))
45 | 1965 | 2343719 | 1 | WikiLeaks ([@wikileaks](https://twitter.com/wikileaks))
46 | 1956 | 673992 | 108 | Medium ([@Medium](https://twitter.com/Medium))
47 | 1947 | 2182676 | 624 | Biz Stone ([@biz](https://twitter.com/biz))
48 | 1939 | 10964049 | 3 | BBC Breaking News ([@BBCBreaking](https://twitter.com/BBCBreaking))
49 | 1912 | 233408 | 13254 | Dave McClure ([@davemcclure](https://twitter.com/davemcclure))
50 | 1905 | 1011590 | 137 | Google Developers ([@googledevs](https://twitter.com/googledevs))
51 | 1893 | 599434 | 585 | Walt Mossberg ([@waltmossberg](https://twitter.com/waltmossberg))
52 | 1892 | 525973 | 115 | The Verge ([@verge](https://twitter.com/verge))
53 | 1881 | 6846181 | 495 | Breaking News ([@BreakingNews](https://twitter.com/BreakingNews))
54 | 1878 | 3506893 | 4727 | Forbes ([@Forbes](https://twitter.com/Forbes))
55 | 1865 | 6112103 | 12 | The Onion ([@TheOnion](https://twitter.com/TheOnion))
56 | 1852 | 1393171 | 1482 | Om Malik ([@om](https://twitter.com/om))
57 | 1850 | 11566965 | 1 | Conan O'Brien ([@ConanOBrien](https://twitter.com/ConanOBrien))
58 | 1848 | 80316 | 1 | Hacker News ([@newsycombinator](https://twitter.com/newsycombinator))
59 | 1840 | 13892218 | 89 | Facebook ([@facebook](https://twitter.com/facebook))
60 | 1810 | 251664 | 26 | Gigaom ([@gigaom](https://twitter.com/gigaom))
61 | 1799 | 2249638 | 23233 | Guardian Tech ([@guardiantech](https://twitter.com/guardiantech))
62 | 1797 | 139903 | 951 | Chris Dixon ([@cdixon](https://twitter.com/cdixon))
63 | 1793 | 13275 | 3390 | Hacker Fantastic ([@hackerfantastic](https://twitter.com/hackerfantastic))
64 | 1789 | 13746311 | 975 | CNN ([@CNN](https://twitter.com/CNN))
65 | 1777 | 212578 | 3 | Techmeme ([@Techmeme](https://twitter.com/Techmeme))
66 | 1777 | 4833004 | 1042 | Reuters Top News ([@Reuters](https://twitter.com/Reuters))
67 | 1741 | 6083682 | 1614005 | Hootsuite ([@hootsuite](https://twitter.com/hootsuite))
68 | 1740 | 5930546 | 26 | Android ([@Android](https://twitter.com/Android))
69 | 1707 | 9264066 | 0 | Dalai Lama ([@DalaiLama](https://twitter.com/DalaiLama))
70 | 1701 | 180266 | 731 | Eric Ries ([@ericries](https://twitter.com/ericries))
71 | 1696 | 188864 | 1707 | Michael Arrington ([@arrington](https://twitter.com/arrington))
72 | 1684 | 6112812 | 772 | TIME.com ([@TIME](https://twitter.com/TIME))
73 | 1664 | 216829 | 1918 | 500 Startups ([@500Startups](https://twitter.com/500Startups))
74 | 1618 | 7118939 | 61 | BBC News (World) ([@BBCWorld](https://twitter.com/BBCWorld))
75 | 1613 | 3398866 | 268 | The New Yorker ([@NewYorker](https://twitter.com/NewYorker))
76 | 1605 | 142123 | 160 | Jeff Atwood ([@codinghorror](https://twitter.com/codinghorror))
77 | 1601 | 157463 | 4070 | Marc Andreessen ([@pmarca](https://twitter.com/pmarca))
78 | 1601 | 213855 | 435 | Reid Hoffman ([@reidhoffman](https://twitter.com/reidhoffman))
79 | 1583 | 1587947 | 533 | Chris Anderson ([@TEDchris](https://twitter.com/TEDchris))
80 | 1560 | 5232083 | 1165 | Microsoft ([@Microsoft](https://twitter.com/Microsoft))
81 | 1560 | 964180 | 1013 | Kara Swisher ([@karaswisher](https://twitter.com/karaswisher))
82 | 1556 | 1222127 | 490 | dick costolo ([@dickc](https://twitter.com/dickc))
83 | 1556 | 1466482 | 799 | Chris Sacca ([@sacca](https://twitter.com/sacca))
84 | 1554 | 6826374 | 1 | Stephen Colbert ([@StephenAtHome](https://twitter.com/StephenAtHome))
85 | 1552 | 808219 | 1159 | Smashing Magazine ([@smashingmag](https://twitter.com/smashingmag))
86 | 1552 | 119710 | 184 | DHH ([@dhh](https://twitter.com/dhh))
87 | 1545 | 2312490 | 44 | Neil deGrasse Tyson ([@neiltyson](https://twitter.com/neiltyson))
88 | 1529 | 170710 | 694 | Mark Suster ([@msuster](https://twitter.com/msuster))
89 | 1528 | 1306755 | 873 | Anonymous ([@YourAnonNews](https://twitter.com/YourAnonNews))
90 | 1527 | 2356613 | 766 | Mark Cuban ([@mcuban](https://twitter.com/mcuban))
91 | 1523 | 4373502 | 85 | Google Chrome ([@googlechrome](https://twitter.com/googlechrome))
92 | 1522 | 119780 | 3 | Venture Hacks ([@venturehacks](https://twitter.com/venturehacks))
93 | 1506 | 149725 | 998 | MG Siegler ([@parislemon](https://twitter.com/parislemon))
94 | 1503 | 158058 | 3044 | John Resig ([@jeresig](https://twitter.com/jeresig))
95 | 1496 | 6188 | 0 | Hacker News 100 ([@newsyc100](https://twitter.com/newsyc100))
96 | 1484 | 15775 | 2 | News.YC ([@HackerNews](https://twitter.com/HackerNews))
97 | 1468 | 4981 | 0 | Hacker News 50 ([@newsyc50](https://twitter.com/newsyc50))
98 | 1463 | 258575 | 199 | Google Ventures ([@GoogleVentures](https://twitter.com/GoogleVentures))
99 | 1451 | 366656 | 370 | Matt Cutts ([@mattcutts](https://twitter.com/mattcutts))
100 | 1451 | 4504186 | 5558 | Huffington Post ([@HuffingtonPost](https://twitter.com/HuffingtonPost))
