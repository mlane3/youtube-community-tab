from urllib.parse import parse_qs, unquote, urlparse
import json

# lots of returned objects are full of tracking params, client data, duplicate info, etc. this sorta trims the fat.
def clean_content_text(content):
    for item in content["runs"]:
        if "navigationEndpoint" in item:
            # traditional links
            if "urlEndpoint" in item["navigationEndpoint"]:
                url = item["navigationEndpoint"]["urlEndpoint"]["url"]
                # replace redirects with direct links
                if url.startswith("https://www.youtube.com/redirect"):
                    parsed_url = urlparse(item["navigationEndpoint"]["urlEndpoint"]["url"])
                    redirect_url = parse_qs(parsed_url.query)["q"][0]
                    item["urlEndpoint"] = {"url": unquote(redirect_url)}
                item.pop("navigationEndpoint")
            # hashtags
            elif "browseEndpoint" in item["navigationEndpoint"]:
                item.pop("loggingDirectives")
                item["navigationEndpoint"]["browseEndpoint"].pop("params")
                item["browseEndpoint"] = item["navigationEndpoint"]["browseEndpoint"]
                item["browseEndpoint"]["url"] = item["navigationEndpoint"]["commandMetadata"]["webCommandMetadata"]["url"]
                item.pop("navigationEndpoint")
    return content

def clean_backstage_attachement(attachment):
    if attachment:
        if "pollRenderer" in attachment:
            for choice in attachment["pollRenderer"]["choices"]:
                for value in ["selectServiceEndpoint", "deselectServiceEndpoint",
                    "voteRatioIfSelected", "votePercentageIfSelected",
                    "voteRatioIfNotSelected", "votePercentageIfNotSelected"]:
                    choice.pop(value)
        elif "videoRenderer" in attachment:
            attachment["videoRenderer"]["navigationEndpoint"]["watchEndpoint"].pop("watchEndpointSupportedOnesieConfig")
            attachment["videoRenderer"]["watchEndpoint"] = attachment["videoRenderer"]["navigationEndpoint"]["watchEndpoint"]
            attachment["videoRenderer"]["watchEndpoint"]["url"] = attachment["videoRenderer"]["navigationEndpoint"]["commandMetadata"]["webCommandMetadata"]["url"]
            for long_by_line in attachment["videoRenderer"]["longBylineText"]["runs"]:
                long_by_line["browseEndpoint"] = long_by_line["navigationEndpoint"]["browseEndpoint"]
                long_by_line.pop("navigationEndpoint")
            for short_by_line in attachment["videoRenderer"]["shortBylineText"]["runs"]:
                short_by_line["browseEndpoint"] = short_by_line["navigationEndpoint"]["browseEndpoint"]
                short_by_line.pop("navigationEndpoint")
            for author in attachment["videoRenderer"]["ownerText"]["runs"]:
                author["browseEndpoint"] = author["navigationEndpoint"]["browseEndpoint"]
            for value in ["publishedTimeText", "navigationEndpoint", "trackingParams", "showActionMenu", "menu",
                "channelThumbnailSupportedRenderers", "thumbnailOverlays"]:
                attachment["videoRenderer"].pop(value)
        return attachment
    return None

