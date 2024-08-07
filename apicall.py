import os
import re

import requests
from twelvelabs import TwelveLabs

from metadata.trail_metadata import TrailMetadata

def download_image(url, filename):
    url = re.sub(r"&t.*", "", url)
    response = requests.get(url)
    file = open(filename, "wb")
    file.write(response.content)
    file.close()


def get_local_thumbnail(thumbnail_url):
    local_filename = "thumbnail.jpg"
    download_image(thumbnail_url, local_filename)
    abs_path = os.path.abspath(local_filename)

    return abs_path

class SearchResult:
    def __init__(self, item, youtube_link):
        self.thumbnail_url = item.thumbnail_url
        self.local_thumbnail_path = get_local_thumbnail(self.thumbnail_url)
        self.youtube_link = f"{youtube_link}&t={item.start}s"
        self.metadata = item.metadata
        self.start_time = item.start
        self.youtube_embed = f"""
        <embed width=“320” height=“240”
        source src=“{self.youtube_link}” title=“YouTube video player” frameborder=“0” allow=“accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture” allowfullscreen>
        """

        trail_metadata = TrailMetadata()
        trail_info = trail_metadata.get_trail_by_timestamp(self.start_time)
        self.trail_info = trail_info

    def __repr__(self):
        str_repr = ""
        str_repr += f"thumbnail_url={self.thumbnail_url}\n"
        str_repr += f"youtube_link={self.youtube_link}\n"
        str_repr += f"metadata={self.metadata}\n"
        str_repr += f"local_thumbnail_path={self.local_thumbnail_path}\n"
        str_repr += f"youtube_embed={self.youtube_embed}\n"
        str_repr += f"start_time={self.start_time}\n"
        str_repr += f"trail_info={self.trail_info}\n"
        return str_repr

    def for_model(self):
        return f"""{self.metadata}
{self.trail_info}
"""


TL_INDEX_ID = os.getenv("TL_INDEX_ID")


def search(
    query,
    index_id=TL_INDEX_ID,
    options=["visual", "conversation", "text_in_video"],
    youtube_link="https://www.youtube.com/watch?v=KKeZPA-Gvs4",
    n=1,
) -> SearchResult:
    client = TwelveLabs(api_key=os.getenv("TL_API_KEY"))
    result = client.search.query(
        index_id=index_id,
        query=query,
        options=options,
        page_limit=n,
    )

    top_hit = result.data[0]

    search_result = SearchResult(top_hit, youtube_link)

    return search_result