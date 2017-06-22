import xml.sax
from collections import OrderedDict
from xml.sax.xmlreader import AttributesNSImpl
from xml.sax import handler

# http://www.theinformationlab.co.uk/wp-content/uploads/2015/07/Step-Three2.png
from metaappscriptsdk.feed.FeedColumn import FeedColumn


class Exact(xml.sax.handler.ContentHandler):
    schema = OrderedDict()
    parser_path = []
    parent_node = None

    def __init__(self):
        super().__init__()

    def startElement(self, name, attrs: AttributesNSImpl):
        self.parser_path.append(name)
        xpath = '/' + ('/'.join(self.parser_path))
        copy_path = list(self.parser_path)
        node_name = ('_'.join(self.parser_path))

        curr_schema = self.schema.get(xpath)  # type: OrderedDict
        if curr_schema is None:
            fc_ = FeedColumn(
                type="TEXT",
                search_path=xpath,
                path=copy_path,
                name=name,
                display_name=node_name
            )
            curr_schema = self.schema.setdefault(xpath, fc_)

        if curr_schema:
            attrs_names = attrs.getNames()
            if attrs_names:
                for attr_name in attrs_names:
                    attr_xpath = xpath + "/@" + attr_name
                    attr_node = self.schema.get(attr_xpath)
                    if attr_node is None:
                        fc_ = FeedColumn(
                            type="TEXT",
                            search_path=attr_xpath,
                            path=copy_path,
                            name=attr_name,
                            display_name=node_name + "_" + attr_name
                        )
                        self.schema.setdefault(attr_xpath, fc_)

    def endElement(self, name):
        self.parser_path.pop()


def parse_xml(file_path):
    """
    :param file_path:
    :rtype: list of FeedColumn
    """
    extract_handler = Exact()
    parser = xml.sax.make_parser()
    parser.setFeature(handler.feature_external_ges, False)
    parser.setContentHandler(extract_handler)
    parser.parse(open(file_path))
    schema = list(extract_handler.schema.values())
    return schema
