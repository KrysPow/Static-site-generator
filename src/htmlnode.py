class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        output = ''
        if self.props==None:
            return output
        for key, value in self.props.items():
            output += f' {key}="{value}"'
        return output
    
    def __repr__(self):
        return f'HTMLNode({self.tag, self.value, self.children, self.props})'
    

class LeafNode(HTMLNode):
    def __init__(self, value, tag=None, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value == None:
            raise ValueError('No value provided')
        if self.tag == None:
            return self.value
        if self.props == None:
            return f'<{self.tag}>{self.value}</{self.tag}>'
        else:
            key, value = [(k, self.props[k]) for k in self.props][0]
            return f'<{self.tag} {key}="{value}">{self.value}</{self.tag}>'
        
    def __repr__(self):
        return f'LeafNode({self.tag, self.value, self.props})'
    

class ParentNode(HTMLNode):
    def __init__(self, children, tag=None, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag == None:
            raise ValueError('No tag provided')
        if self.children == None:
            raise ValueError('No children provided')
        output = ''
        for child in self.children:
            output += child.to_html()
        return f'<{self.tag}{self.props_to_html()}>{output}</{self.tag}>'

    def __repr__(self):
        return f'ParentNode({self.tag, self.children, self.props})'
    

def text_node_to_html_node(text_node):
    if text_node.text_type == 'text':
        return LeafNode(value=text_node.text)
    if text_node.text_type == 'bold':
        return LeafNode(tag='b', value=text_node.text)
    if text_node.text_type == 'italic':
        return LeafNode(tag='i', value=text_node.text)
    if text_node.text_type == 'code':
        return LeafNode(tag='code', value=text_node.text)
    if text_node.text_type == 'link':
        return LeafNode(tag='a', value=text_node.text, props={'href':text_node.url})
    if text_node.text_type == 'image':
        return LeafNode(tag='img', value='', props={'src':text_node.url, 'alt':text_node.text})
    raise Exception('text type not valid')