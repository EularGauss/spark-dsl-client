from schema import parse_schema


def test_parse_schema():
    expected_output = {
      "event_id": {
        "type": "string",
        "doc": "Unique identifier for each event (UUID)"
      },
      "user_id": {
        "type": "string",
        "doc": "Unique identifier for the user"
      },
      "session_id": {
        "type": "string",
        "doc": "Session ID for the user's browsing session"
      },
      "event_type": {
        "type": [
          "CLICK",
          "PAGE_VIEW",
          "SCROLL",
          "HOVER",
          "NAVIGATION"
        ],
        "doc": "Type of event (e.g., click, page view, scroll)"
      },
      "timestamp": {
        "type": "long",
        "doc": "Timestamp of the event in microseconds"
      },
      "page_url": {
        "type": "string",
        "doc": "URL of the page where the event occurred"
      },
      "referrer_url": {
        "type": [
          "string",
          "null"
        ],
        "doc": "URL of the referrer page (if any), can be null"
      },
      "user_agent": {
        "type": "string",
        "doc": "Browser's user agent string"
      },
      "browser": {
        "type": [
          "CHROME",
          "FIREFOX",
          "SAFARI",
          "EDGE",
          "OTHER"
        ],
        "doc": "Type of browser used for the session"
      },
      "os": {
        "type": [
          "WINDOWS",
          "MACOS",
          "LINUX",
          "ANDROID",
          "IOS",
          "OTHER"
        ],
        "doc": "Operating system used for the session"
      },
      "device_type": {
        "type": [
          "DESKTOP",
          "MOBILE",
          "TABLET",
          "OTHER"
        ],
        "doc": "Type of device used for the session"
      },
      "screen_resolution": {
        "type": [
          "string",
          "null"
        ],
        "doc": "Screen resolution of the user's device, can be null"
      },
      "latitude": {
        "type": [
          "double",
          "null"
        ],
        "doc": "Latitude of the user's location"
      },
      "longitude": {
        "type": [
          "double",
          "null"
        ],
        "doc": "Longitude of the user's location"
      },
      "geo_location": {
        "type": "record",
        "doc": "Geographical location of the user, based on IP or GPS data"
      },
      "interaction_details": {
        "type": "map",
        "doc": "Additional details of the interaction as key-value pairs (e.g., button clicked, scroll depth)"
      }
    }

    parsed_schema = parse_schema("click_stream")
    print(parsed_schema)
    assert parsed_schema == expected_output


if __name__ == "main":
    test_parse_schema()