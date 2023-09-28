from urllib.parse import urlparse
import xml.etree.ElementTree as ET


class AppUtils:
    @staticmethod
    def is_valid_url(url):
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False
        
        
    @classmethod
    def allowed_channels(cls) -> list:
        with open('whitelisted_channels.txt', 'r') as f:
            return f.read().splitlines()
    
    @classmethod
    def is_channel_allowed(cls, channel_id:str) -> bool:
        return channel_id in cls.allowed_channels()
    
    @classmethod
    def process_xml(cls, xml_content:str):    
        tree = ET.fromstring(xml_content)
        # clean programs
        for program in tree.findall('programme'):
            if not cls.is_channel_allowed(program.attrib['channel']):
                tree.remove(program)

        # clean channels
        for channel in tree.findall('channel'):
            if not cls.is_channel_allowed(channel.attrib['id']):
                tree.remove(channel)

        return ET.tostring(tree, encoding='utf8', method='xml')

    
          


