import requests
import json
from datetime import datetime
import time

DEFAULT_AREA_ID = 13
DEFAULT_PAGE_SIZE = 20


class ResidentAdvisor:
    def __init__(self):
        self.BASE_URL = "https://ra.co/graphql"
        self.headers = {
            "accept": "*/*",
            "accept-language": "en-GB,en;q=0.5",
            "content-type": "application/json",
            "ra-content-language": "en",
            "referer": f"https://ra.co/events/uk/london",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        }

    def get_ra_events(
        self,
        start_date,
        end_date,
        area_id=DEFAULT_AREA_ID,
        page_size=DEFAULT_PAGE_SIZE,
        page=1,
    ):
        query = """
        query GET_EVENT_LISTINGS($filters: FilterInputDtoInput, $filterOptions: FilterOptionsInputDtoInput, $page: Int, $pageSize: Int, $sort: SortInputDtoInput) {
            eventListings(
                filters: $filters
                filterOptions: $filterOptions
                pageSize: $pageSize
                page: $page
                sort: $sort
            ) {
                data {
                    id
                    listingDate
                    event {
                        ...eventListingsFields
                        artists {
                            id
                            name
                            __typename
                        }
                        __typename
                    }
                    __typename
                }
                filterOptions {
                    genre {
                        label
                        value
                        count
                        __typename
                    }
                    eventType {
                        value
                        count
                        __typename
                    }
                    location {
                        value {
                            from
                            to
                            __typename
                        }
                        count
                        __typename
                    }
                    __typename
                }
                totalResults
                __typename
            }
        }

        fragment eventListingsFields on Event {
            id
            date
            startTime
            endTime
            title
            contentUrl
            flyerFront
            isTicketed
            interestedCount
            isSaved
            isInterested
            queueItEnabled
            newEventForm
            images {
                id
                filename
                alt
                type
                crop
                __typename
            }
            pick {
                id
                blurb
                __typename
            }
            venue {
                id
                name
                contentUrl
                live
                __typename
            }
            __typename
        }
        """

        variables = {
            "filters": {
                "areas": {"eq": area_id},
                "listingDate": {"gte": start_date, "lte": end_date},
            },
            "filterOptions": {"genre": True, "eventType": True},
            "pageSize": page_size,
            "page": page,
            "sort": {
                "listingDate": {"order": "ASCENDING"},
                "score": {"order": "DESCENDING"},
                "titleKeyword": {"order": "ASCENDING"},
            },
        }

        payload = json.dumps({"query": query, "variables": variables})

        response = requests.post(self.BASE_URL, headers=self.headers, data=payload)
        return response.json()

    def extract_event_info(self, response_data: dict) -> list[dict]:
        events = []
        for event_listing in response_data["data"]["eventListings"]["data"]:
            event = event_listing["event"]
            # Extract artist information
            artists = [(artist["id"], artist["name"]) for artist in event["artists"]]

            # Extract venue information
            venue = (event["venue"]["id"], event["venue"]["name"])

            # Extract event image
            image_url = "https://static.ra.co/images/user/av/default.jpg"
            if event["images"]:
                image_url = event["images"][0]["filename"]

            # Parse dates
            date = datetime.fromisoformat(event["date"].replace("Z", ""))
            start_time = datetime.fromisoformat(event["startTime"].replace("Z", ""))
            end_time = datetime.fromisoformat(event["endTime"].replace("Z", ""))

            event_info = {
                "title": event["title"],
                "date": date.date(),
                "start_time": start_time.time(),
                "end_time": end_time.time(),
                "venue": venue,
                "artists": artists,
                "image_url": image_url,
            }
            events.append(event_info)
        return events


if __name__ == "__main__":
    resident_advisor = ResidentAdvisor()
    events_data = resident_advisor.get_ra_events("2024-10-12", "2024-10-13")
    events = resident_advisor.extract_event_info(events_data)
    for event in events:
        print(event)
