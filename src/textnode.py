import re


class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (self.text == other.text and 
            self.text_type == other.text_type and 
            self.url == other.url)
    
    def __repr__(self):
        return f'TextNode{self.text, self.text_type, self.url}'
    

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_list = []
    for oldnode in old_nodes:
        if oldnode.text_type != 'text':
            new_list.append(oldnode)
        else:
            if delimiter in oldnode.text:
                on_split = oldnode.text.split(delimiter)
                if len(on_split)%2 == 1 and len(on_split) > 1:
                    nw_nodes = [TextNode(on_split[i], 'text') if i%2 == 0 else TextNode(on_split[i], text_type) for i in range(len(on_split))]
                    new_list.extend(nw_nodes)
                else:
                    raise Exception(f'Invalid markdown syntax. Use {delimiter} twice')
            else:
                new_list.extend([oldnode])
    return new_list
    

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)


def split_nodes_image(old_nodes):
    new_list = []
    for node in old_nodes:
        extracted_imgs = extract_markdown_images(node.text)
        if extracted_imgs == []:
            new_list.append(node)
        else:
            for (alt, url) in extracted_imgs:
                [first_part, second_part] = node.text.split(f'![{alt}]({url})', 1)
                if first_part != '':
                    new_list.extend([TextNode(first_part, 'text'), TextNode(alt, 'image', url)])
                else:
                    new_list.append(TextNode(alt, 'image', url))
                node = TextNode(second_part, 'text')

            if second_part != '':
                new_list.append(TextNode(second_part, 'text'))
    return new_list
            

def split_nodes_links(old_nodes):
    new_list = []
    for node in old_nodes:
        extracted_links = extract_markdown_links(node.text)
        if extracted_links == []:
            new_list.append(node)
        else:
            for (alt, url) in extracted_links:
                [first_part, second_part] = node.text.split(f'[{alt}]({url})', 1)
                if first_part != '':
                    new_list.extend([TextNode(first_part, 'text'), TextNode(alt, 'link', url)])
                else:
                    new_list.append(TextNode(alt, 'link', url))
                node = TextNode(second_part, 'text')

            if second_part != '':
                new_list.append(TextNode(second_part, 'text'))
    return new_list
