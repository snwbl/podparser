# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/02_item.ipynb.

# %% auto 0
__all__ = ['foo', 'Item', 'Episode']

# %% ../nbs/02_item.ipynb 3
def foo(): pass

# %% ../nbs/02_item.ipynb 5
from datetime import datetime
from bs4 import BeautifulSoup
from dateutil import parser
import lxml

# %% ../nbs/02_item.ipynb 6
class Item(object):
    """Parses an xml rss feed

    RSS Specs http://cyber.law.harvard.edu/rss/rss.html
    iTunes Podcast Specs http://www.apple.com/itunes/podcasts/specs.html

    Args:
        soup (bs4.BeautifulSoup): BeautifulSoup object representing a rss item

    Note:
        All attributes with empty or nonexistent element will have a value of None

    Attributes:
        author (str): The author of the item
        comments (str): URL of comments
        creative_commons (str): creative commons license for this item
        description (str): Description of the item.
        enclosure_url (str): URL of enclosure
        enclosure_type (str): File MIME type
        enclosure_length (int): File size in bytes
        guid (str): globally unique identifier
        itunes_author_name (str): Author name given to iTunes
        itunes_block (bool): It this Item blocked from itunes
        itunes_closed_captioned: (str): It is this item have closed captions
        itunes_duration (str): Duration of enclosure
        itunes_explicit (str): Is this item explicit. Should only be yes or clean.
        itune_image (str): URL of item cover art
        itunes_order (str): Override published_date order
        itunes_subtitle (str): The item subtitle
        itunes_summary (str): The summary of the item
        link (str): The URL of item.
        published_date (str): Date item was published
        title (str): The title of item.
        date_time (datetime): When published
        transcripts (list): URLs to transcripts of the podcast provided by the publisher
    """

    def __init__(self, soup):
        #super(Item, self).__init__()

        self.soup = soup
        self.set_rss_element()
        self.set_itunes_element()

        self.set_time_published()
        self.set_dates_published()

    def set_time_published(self):
        if self.published_date is None:
            return
        try:
            self.time_published = parser.parse(self.published_date)
        except TypeError:
            self.time_published = None

    def set_dates_published(self):
        if self.published_date is None:
            self.date_time = None
            return
        
        try:
            temp_datetime = parser.parse(self.published_date)
        except TypeError:
            self.date_time = None
            return
        self.date_time = temp_datetime

    def to_dict(self):
        item = {}
        item['author'] = self.author
        item['comments'] = self.comments
        item['creative_commons'] = self.creative_commons
        item['enclosure_url'] = self.enclosure_url
        item['enclosure_type'] = self.enclosure_type
        item['enclosure_length'] = self.enclosure_length
        item['guid'] = self.guid
        item['itunes_author_name'] = self.itunes_author_name
        item['itunes_block'] = self.itunes_block
        item['itunes_closed_captioned'] = self.itunes_closed_captioned
        item['itunes_duration'] = self.itunes_duration
        item['itunes_explicit'] = self.itunes_explicit
        item['itune_image'] = self.itune_image
        item['itunes_order'] = self.itunes_order
        item['itunes_subtitle'] = self.itunes_subtitle
        item['itunes_summary'] = self.itunes_summary
        item['itunes_episode'] = self.itunes_episode
        item['description'] = self.description
        item['link'] = self.link
        item['published_date'] = self.published_date
        item['title'] = self.title
        item["podcast_transcripts"] = self.transcripts
        item["podcast_season"] = self.podcast_season
        item["podcast_episode"] = self.podcast_episode
        item["podcast_chapters"] = self.podcast_chapters
        item["podcast_person"] = self.podcast_person
        item["podcast_locked"] = self.podcast_locked
        item["podcast_funding"] = self.podcast_funding
        item["podcast_location"] = self.podcast_location
        item["podcast_soundbite"] = self.podcast_soundbite
        return item

    def set_rss_element(self):
        """Set each of the basic rss elements."""
        self.set_author()
        self.set_categories()
        self.set_comments()
        self.set_creative_commons()
        self.set_description()
        self.set_enclosure()
        self.set_guid()
        self.set_link()
        self.set_published_date()
        self.set_title()
        ## separate for podcast 2.0?
        self.set_transcripts()
        self.set_season()
        self.set_episode()
        self.set_chapters()
        self.set_person()
        self.set_locked()
        self.set_funding()
        self.set_location()
        self.set_soundbite()

    def set_author(self):
        """Parses author and set value."""
        try:
            self.author = self.soup.find('author').string
        except AttributeError:
            self.author = None

    def set_categories(self):
        """Parses and set categories"""
        self.categories = []
        temp_categories = self.soup.findAll('category')
        for category in temp_categories:
            category_text = category.string
            self.categories.append(category_text)

    def set_comments(self):
        """Parses comments and set value."""
        try:
            self.comments = self.soup.find('comments').string
        except AttributeError:
            self.comments = None

    def set_creative_commons(self):
        """Parses creative commons for item and sets value"""
        try:
            self.creative_commons = self.soup.find(
                'creativecommons:license').string
        except AttributeError:
            self.creative_commons = None

    def set_description(self):
        """Parses description and set value."""
        try:
            self.description = self.soup.find('description').string
        except AttributeError:
            self.description = None

    def set_enclosure(self):
        """Parses enclosure_url, enclosure_type then set values."""
        try:
            self.enclosure_url = self.soup.find('enclosure')['url']
        except:
            self.enclosure_url = None
        try:
            self.enclosure_type = self.soup.find('enclosure')['type']
        except:
            self.enclosure_type = None
        try:
            self.enclosure_length = self.soup.find('enclosure')['length']
            self.enclosure_length = int(self.enclosure_length)
        except:
            self.enclosure_length = None

    def set_guid(self):
        """Parses guid and set value"""
        try:
            self.guid = self.soup.find('guid').string
        except AttributeError:
            self.guid = None

    def set_link(self):
        """Parses link and set value."""
        try:
            self.link = self.soup.find('link').string
        except AttributeError:
            self.link = None

    def set_published_date(self):
        """Parses published date and set value."""
        self.published_date = self.soup.find('pubDate')
        if not self.published_date:
            self.published_date = self.soup.find('pubdate')
        if self.published_date:
            self.published_date = self.published_date.text

    def set_title(self):
        """Parses title and set value."""
        try:
            self.title = self.soup.find('title').string
        except AttributeError:
            self.title = None

    def set_itunes_element(self):
        """Set each of the itunes elements."""
        self.set_itunes_author_name()
        self.set_itunes_block()
        self.set_itunes_closed_captioned()
        self.set_itunes_duration()
        self.set_itunes_explicit()
        self.set_itune_image()
        self.set_itunes_order()
        self.set_itunes_subtitle()
        self.set_itunes_summary()

    def set_itunes_author_name(self):
        """Parses author name from itunes tags and sets value"""
        try:
            self.itunes_author_name = self.soup.find('itunes:author').string
        except AttributeError:
            self.itunes_author_name = None

    def set_itunes_block(self):
        """Check and see if item is blocked from iTunes and sets value"""
        try:
            block = self.soup.find('itunes:block').string.lower()
        except AttributeError:
            block = ""
        if block == "yes":
            self.itunes_block = True
        else:
            self.itunes_block = False

    def set_itunes_closed_captioned(self):
        """Parses isClosedCaptioned from itunes tags and sets value"""
        try:
            self.itunes_closed_captioned = self.soup.find(
                'itunes:isclosedcaptioned').string
            self.itunes_closed_captioned = self.itunes_closed_captioned.lower()
        except AttributeError:
            self.itunes_closed_captioned = None

    def set_itunes_duration(self):
        """Parses duration from itunes tags and sets value"""
        try:
            self.itunes_duration = self.soup.find('itunes:duration').string
        except AttributeError:
            self.itunes_duration = None

    def set_itunes_explicit(self):
        """Parses explicit from itunes item tags and sets value"""
        try:
            self.itunes_explicit = self.soup.find('itunes:explicit').string
            self.itunes_explicit = self.itunes_explicit.lower()
        except AttributeError:
            self.itunes_explicit = None

    def set_itune_image(self):
        """Parses itunes item images and set url as value"""
        try:
            self.itune_image = self.soup.find('itunes:image').get('href')
        except AttributeError:
            self.itune_image = None

    def set_itunes_order(self):
        """Parses episode order and set url as value"""
        try:
            self.itunes_order = self.soup.find('itunes:order').string
            self.itunes_order = self.itunes_order.lower()
        except AttributeError:
            self.itunes_order = None

    def set_itunes_subtitle(self):
        """Parses subtitle from itunes tags and sets value"""
        try:
            self.itunes_subtitle = self.soup.find('itunes:subtitle').string
        except AttributeError:
            self.itunes_subtitle = None

    def set_itunes_summary(self):
        """Parses summary from itunes tags and sets value"""
        try:
            self.itunes_summary = self.soup.find('itunes:summary').string
        except AttributeError:
            self.itunes_summary = None

    
    def set_transcripts(self):
        """Parses transcript type and url"""
        self.transcripts = []
        transcripts = self.soup.find_all("transcript")
        if transcripts:
            for transcript in transcripts:
                self.transcripts.append(
                    {
                        "type": transcript["type"],
                        "url": transcript["url"],
                    }
                )

    
    def set_episode(self):
        """Parses episode number"""
        try:
            self.itunes_episode = self.soup.find('itunes:episode').string
        except AttributeError:
            self.itunes_episode = None
        try:
            self.podcast_episode = self.soup.find('podcast:episode').string
        except AttributeError:
            self.podcast_episode = None

    
    def set_chapters(self):
        """Parses episode chapteers"""
        try:
            chapters = self.soup.find('podcast:chapters')
            self.podcast_chapters = {"type": chapters["type"], "url": chapters["url"]} 
        except TypeError:
            self.podcast_chapters = None
        except KeyError:
            self.podcast_chapters = None  
        if not self.podcast_chapters:
            try:
                self.podcast_chapters = {"type": chapters["type"], "url": chapters["href"]}
            except TypeError:
                self.podcast_chapters = None

    
    def set_season(self):
        """Parses episode season"""
        try:
            self.podcast_season = self.soup.find('podcast:season').string
        except AttributeError:
            self.podcast_season = None

    def set_person(self):
        """Parses episode person"""
        try:
            self.podcast_person = self.soup.find('podcast:person').string
        except AttributeError:
            self.podcast_person = None


    def set_locked(self):
        """Parses episode locked"""
        try:
            self.podcast_locked = self.soup.find('podcast:locked').string
        except AttributeError:
            self.podcast_locked = None

    def set_funding(self):
        """Parses episode funding"""
        try:
            self.podcast_funding = self.soup.find('podcast:funding').string
        except AttributeError:
            self.podcast_funding = None

    def set_location(self):
        """Parses episode location"""
        try:
            self.podcast_location = self.soup.find('podcast:location').string
        except AttributeError:
            self.podcast_location = None


    def set_soundbite(self):
        """Parses episode soundbite"""
        try:
            self.podcast_soundbite = self.soup.find('podcast:soundbite').string
        except AttributeError:
            self.podcast_soundbite = None


# %% ../nbs/02_item.ipynb 7
from pydantic import BaseModel
from pydantic import field_validator
from datetime import datetime
from typing import List, Optional, Union
import justext
import re

# %% ../nbs/02_item.ipynb 8
class Episode(BaseModel):
    episode_id: Optional[str] = None
    feed_id: Optional[str] = None
    author: Optional[str] = None
    comments: Optional[str] = None
    creative_commons: Optional[str] = None
    enclosure_url: Optional[str] = None
    enclosure_type: Optional[str] = None
    enclosure_length: Optional[int] = None
    guid: Optional[str] = None
    itunes_author_name: Optional[str] = None
    itunes_block: Optional[bool] = None
    itunes_closed_captioned: Optional[bool] = None
    itunes_duration: Optional[int] = 0
    itunes_explicit: Optional[bool] = None
    itune_image: Optional[str] = None
    itunes_order: Optional[str] = None
    itunes_subtitle: Optional[str] = None
    itunes_summary: Optional[str] = None
    itunes_episode: Optional[Union[int, str]] = None
    description: Optional[str] = None
    link: Optional[str] = None
    published_date: Optional[datetime] = None
    title: Optional[str] = None
    podcast_transcripts: Optional[List] = None
    podcast_season: Optional[int] = None
    podcast_episode: Optional[Union[int, str]] = None
    podcast_chapters: Optional[dict] = None
    podcast_person: Optional[str] = None
    podcast_locked: Optional[bool] = None
    podcast_funding: Optional[str] = None
    podcast_location: Optional[str] = None
    podcast_soundbite: Optional[str] = None


    @field_validator('itunes_duration', mode='before')
    @classmethod
    def format_duration(cls, duration):
        _duration = 0
        if duration:
            try:
                _duration = int(duration)
            except ValueError:
                duration = duration.replace(";", ":")
                if ":" in duration:
                    duration = duration.replace("::", ":")
                    if duration.count(":") == 1:
                        duration = duration.replace("h", "")
                        duration = duration.replace("H", "")
                        duration = duration.replace("Min", "")
                        duration = duration.replace("min", "")
                        duration = duration.strip()
                        min, sec = duration.split(":")
                        try:
                            _duration += float(re.sub("[^0-9]", "", min)) * 60
                        except ValueError:
                            print(duration)
                        try:
                            _duration += float(re.sub("[^0-9]", "", sec))
                        except ValueError:
                            print(duration)
                    if duration.count(":") == 2:
                        hour, min, sec = duration.split(":")
                        try:
                            _duration += int(re.sub("[^0-9]", "", hour)) * 60 * 60
                        except ValueError:
                            print(duration)
                        try:
                            _duration += int(re.sub("[^0-9]", "", min)) * 60
                        except ValueError:
                            print(duration)
                        try:
                            _duration += int(re.sub("[^0-9]", "", sec))
                        except ValueError:
                            print(duration)
            return int(_duration)
        else:
            return 0

    
    @field_validator("itunes_summary", "description", mode="before")
    @classmethod
    def clean_text(cls, text):
        try:
            paragraphs = justext.justext(text, justext.get_stoplist("English"))
        except ValueError:
            return text
        except lxml.etree.ParserError:
            return text
        except TypeError:
            return text
        _text = ""
        for paragraph in paragraphs:
            _text += f"{paragraph.text} "
        return _text.strip()


    @field_validator('published_date', mode='before')
    @classmethod
    def parse_date(cls, published_date):
        if published_date:
            published_date = parser.parse(published_date)
            return published_date.isoformat()
        else:
            return published_date


    @field_validator('itunes_explicit', mode='before')
    @classmethod
    def parse_itunes_explicit(cls, itunes_explicit):
        if itunes_explicit == "clean":
            return False
        else:
            return itunes_explicit
