from urllib.parse import urlparse
import xml.etree.ElementTree as ET
from xml.dom import minidom
from lxml import etree as lx_tee

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
    def process_xml(cls, xml_content:str|bytes, logger, extract:bool=False) -> dict:    
        if type(xml_content) == str:
            xml_content = xml_content.encode('ascii')
        
        tree = lx_tee.fromstring(xml_content)
        dom = minidom.parseString(xml_content)
        doctype = dom.doctype 
        doctype = doctype.toxml()
        
        # clean programs
        programs_count = 0
        channels_count = 0
        
        program_data = []
        channel_data = []
        
        for program in tree.findall('programme'):
            if extract:
                program_data.append(
                    {
                    "channel": program.attrib['channel'],
                    "title": program.find('title').text,
                    "start": program.get('start'),
                    "stop": program.get('stop')
                    }
                )
            
            if not cls.is_channel_allowed(program.attrib['channel']):
                tree.remove(program)
            programs_count += 1
            
        # clean channels
        for channel in tree.findall('channel'):
            if extract:
                channel_data.append(
                    {
                    "id": channel.attrib['id'],
                    "name": channel.find('display-name').text
                    }
                )
            if not cls.is_channel_allowed(channel.attrib['id']):
                tree.remove(channel)
            channels_count += 1
        if extract:
            cls.log_channels(
                channel_data,
                logger
            )
            
            cls.log_programs(
                program_data, 
                logger
            )
            
        return {
            # 'xml': ET.tostring(tree, encoding='utf8', method='xml'),
            'xml': lx_tee.tostring(
                tree, 
                encoding='utf8', 
                xml_declaration=True,
                pretty_print=True,
                doctype=doctype
                ),
            'programs_count': programs_count,
            'channels_count': channels_count
        }
        
    @classmethod
    def log_programs(cls, programs:dict, logger):
        for program in programs:
            logger.extract(
                f"CHANNEL={program['channel']}, TITLE={program['title']}, START={program['start']}, STOP={program['stop']}"
            )

    @classmethod
    def log_channels(cls, channels:dict, logger):
        for channel in channels:
            logger.extract(
                f"CHANNEL_ID={channel['id']}, CHANNEL_NAME={channel['name']}"
            )


EXTRACT = 15
def extract(self, message, *args, **kwargs):
    if self.isEnabledFor(EXTRACT):
        self._log(EXTRACT, message, args, **kwargs)