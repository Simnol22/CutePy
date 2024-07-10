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

    # Contraire de to_cute_name. Ici va servir a retrouver les id a partir du nom, dans le but
    # d'envoyer des commandes via une connection serial.
    # rockets.anirniq.communication.gnss.lat -> 0 , 2 , 4
    # TODO : Gerer les erreurs.
    def from_cute_name(self, name):
        parts = name.split('.')
        nodeGroupId = None
        nodeId = None
        messageId = None
        id = 1
        for node_group in self.root:
            if node_group.attrib['name'] == parts[id]:
                id += 1
                nodeGroupId = node_group.attrib['id']
                for node in node_group:
                    if node.attrib['name'] == parts[id]:
                        id += 1
                        nodeId = node.attrib['id']
                        for message in node:
                            if message.tag == 'message_group':
                                if message.attrib['name'] == parts[id]:
                                    id += 1
                                for m in message:   
                                    if m.attrib['name'] == parts[id]:
                                        messageId = m.attrib['id']
                            else:
                                if message.attrib['name'] == parts[id]:
                                    messageId = message.attrib['id']

        return int(nodeGroupId), int(nodeId), int(messageId)                   
          
    def to_cute_name(self, nodeGroupId, nodeId, messageId):
        cuteName = self.parse_to_cute_name(nodeGroupId, nodeId, messageId)
        return '.'.join(cuteName)
    
    def to_cute_path(self, nodeGroupId, nodeId):
        cutePath = self.parse_to_cute_path(nodeGroupId, nodeId)
        return '.'.join(cutePath)
    
    # Parser du protocol.xml vers les nums standards utilisés dans l'application
    # ex : 0 , 2 , 4 -> rockets.anirniq.communication.gnss.lat
    # TODO : gestion d'erreur. Si on donne mettons 0,2,40 ou patate,1,-5 ca devrait retourner une erreur
    def parse_to_cute_name(self, nodeGroupId, nodeId, messageId):
        nodeGroupId = str(nodeGroupId) # In case it's an int
        nodeId = str(nodeId)
        messageId = str(messageId)
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
    
    def parse_to_cute_path(self, nodeGroupId, nodeId):
        nodeGroupId = str(nodeGroupId) # In case it's an int
        nodeId = str(nodeId)
        toCutePath = []
        toCutePath.append(self.root.attrib['name'])
        for node_group in self.root:
            if node_group.attrib["id"] == nodeGroupId:
                toCutePath.append(node_group.attrib['name'])
                for node in node_group:
                    if node.attrib["id"] == nodeId:
                        toCutePath.append(node.attrib['name'])
        return toCutePath  