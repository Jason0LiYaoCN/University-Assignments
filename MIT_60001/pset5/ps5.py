# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        self.__guid = guid
        self.__title = title
        self.__description = description
        self.__link = link
        self.__pubdate = pubdate
    def get_guid(self):
        return self.__guid
    def get_title(self):
        return self.__title
    def get_description(self):
        return self.__description
    def get_link(self):
        return self.__link
    def get_pubdate(self):
        return self.__pubdate
    


#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
# TODO: PhraseTrigger
class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self.__phrase = phrase
    def get_phrase(self):
        return self.__phrase
    def is_phrase_in(self, text):
        newphraselist = self.__phrase.split()
        newphraselist = [x.lower() for x in newphraselist ]
        newtextlist = []
        onewordlist = []
        for letters in text:
            if letters in string.punctuation or letters == ' ':
                if (len(onewordlist) != 0) and (onewordlist not in newtextlist):
                    newtextlist.append(''.join(onewordlist))
                onewordlist = []
                continue
            letters = letters.lower()
            onewordlist.append(letters)
        if len(onewordlist) != 0:
            newtextlist.append(''.join(onewordlist))
        length_phrase = len(newphraselist)
        compare_result = False
        # print(newphraselist)
        # print(newtextlist)
        for index in range(len(newtextlist)):
            if newtextlist[index] == newphraselist[0]:
                index_of_phrase = 0
                while index + 1 < len(newtextlist) and index_of_phrase + 1 < length_phrase:
                    index = index + 1
                    index_of_phrase = index_of_phrase + 1
                    if newtextlist[index] == newphraselist[index_of_phrase]:
                        if index_of_phrase == length_phrase - 1:
                            compare_result = True
                        continue
                    else:
                        break
        return compare_result
        # def evaluate(self, story):
        #     return self.is_phrase_in(story)

# test = PhraseTrigger("PURPLE COW")
# print(test.is_phrase_in("Purple!!! Cow!!!"))

# Problem 3
# TODO: TitleTrigger

class TitleTrigger(PhraseTrigger):
    def __init__(self, phrase):
        PhraseTrigger.__init__(self, phrase)
    def evaluate(self, story):
        text = story.get_title()
        return self.is_phrase_in(text)

# Problem 4
# TODO: DescriptionTrigger

class DescriptionTrigger(PhraseTrigger):
    def __init__(self, phrase):
        PhraseTrigger.__init__(self, phrase)
    def evaluate(self, story):
        text = story.get_description()
        return self.is_phrase_in(text)
# TIME TRIGGERS

# Problem 5
# TODO: TimeTrigger
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.
class TimeTrigger(Trigger):
    def __init__(self, pubtime):
        format = '%d %b %Y %H:%M:%S'
        pubtime = datetime.strptime(pubtime, format)
        pubtime = pubtime.replace(tzinfo=pytz.timezone("EST"))
        self.__pubtime = pubtime
    def get_pubtime(self):
        return self.__pubtime

# test = TimeTrigger('12 Oct 2016 23:59:59')
# print(test.get_pubtime())
# Problem 6
# TODO: BeforeTrigger and AfterTrigger

class BeforeTrigger(TimeTrigger):
    def evaluate(self, story):
        return self.get_pubtime() > story.get_pubdate().replace(tzinfo=pytz.timezone("EST"))

class AfterTrigger(TimeTrigger):
    def evaluate(self, story):
        return self.get_pubtime() < story.get_pubdate().replace(tzinfo=pytz.timezone("EST"))
# COMPOSITE TRIGGERS

# Problem 7
# TODO: NotTrigger
class NotTrigger(Trigger):
    def __init__(self, trigger1):
        self.trig1 = trigger1
    def evaluate(self, story):
        return not self.trig1.evaluate(story)

# Problem 8
# TODO: AndTrigger
class AndTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trig1 = trigger1
        self.trig2 = trigger2
    def evaluate(self, story):
        return self.trig1.evaluate(story) and self.trig2.evaluate(story)
# Problem 9
# TODO: OrTrigger
class OrTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trig1 = trigger1
        self.trig2 = trigger2
    def evaluate(self, story):
        return self.trig1.evaluate(story) or self.trig2.evaluate(story)

#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    # This is a placeholder
    # (we're just returning all the stories, with no filtering)
    trig_stories = []
    for story in stories:
        for trig in triggerlist:
            if trig.evaluate(story):
                trig_stories.append(story)
                break
    return trig_stories



#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers
    trig_dict = {}
    trig_list = []
    for i in range(len(lines)):
        trig = lines[i].split(',')
        if trig[1] == 'TITLE':
            trig_dict[trig[0]] = TitleTrigger(trig[2])
        elif trig[1] == 'DESCRIPTION':
            trig_dict[trig[0]] = DescriptionTrigger(trig[2])
        elif trig[1] == 'AFTER':
            trig_dict[trig[0]] = AfterTrigger(trig[2])
        elif trig[1] == 'BEFORE':
            trig_dict[trig[0]] = BeforeTrigger(trig[2])
        elif trig[1] == 'NOT':
            trig_dict[trig[0]] = NotTrigger(trig[2])
        elif trig[1] == 'AND':
            trig_dict[trig[0]] = AndTrigger(trig_dict[trig[2]], trig_dict[trig[3]])
        elif trig[1] == 'OR':
            trig_dict[trig[0]] = OrTrigger(trig_dict[trig[2]], trig_dict[trig[3]])
        elif trig[0] == 'ADD':
            for x in range(1, len(trig)):
                trig_list.append(trig_dict[trig[x]])
    return trig_list



SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("election")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Clinton")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        # triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

