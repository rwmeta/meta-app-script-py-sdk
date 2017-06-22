from metaappscriptsdk.feed.ParseXml import parse_xml


def parse_feed_file(type, file_path):
    if type == 'XML':
        return parse_xml(file_path)
    return []
