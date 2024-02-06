from xml.etree import cElementTree as ElementTree

class ProtocolHelper():
    def __init__(self,protocol = None):
        self.protocol = protocol
        self.root = None
        if protocol:
            self.read_protocol(protocol)
    
    def read_protocol(self,protocol):
        try:
            tree = ElementTree.parse(protocol)
            self.root = tree.getroot()
            return True
        except:
            print("Error reading protocol")
            exit(1)

    # ex : 0 , 2 , 4 -> rockets.anirniq.communication.gnss.lat
    # TODO : from_cute_name : rockets.anirniq.communication.gnss.lat -> 0 , 2 , 4"
    def to_cute_name(self, nodeGroupId, nodeId, messageId):
        toCuteName = []
        toCuteName.append(self.root.attrib['name'])
        for node_group in self.root:
            if node_group.attrib["id"] == nodeGroupId:
                toCuteName.append(node_group.attrib['name'])
                for node in node_group:
                    if node.attrib["id"] == nodeId:
                        toCuteName.append(node.attrib['name'])
                        for message in node:
                            if message.tag == 'message_group':
                                for m in message:
                                    if m.attrib["id"] == messageId:
                                        toCuteName.append(message.attrib['name'])
                                        toCuteName.append(m.attrib['name'])
                                        return toCuteName
                            else:
                                if message.attrib["id"] == messageId:
                                    toCuteName.append(message.attrib['name'])
                                    return toCuteName
        return toCuteName