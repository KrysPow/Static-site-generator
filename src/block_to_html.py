from htmlnode import ParentNode, LeafNode, text_node_to_html_node
from textnode import text_to_textnodes, markdown_to_blocks, block_to_block_type
import re

def block_to_html(block, block_type):
    if block_type == 'heading':
        hashes = re.findall(r'^#{1,6} ', block)[0].count('#')
        block = block.lstrip('# ')
        return ParentNode(children=list(map(lambda node:text_node_to_html_node(node), text_to_textnodes(block))), tag=f'h{hashes}')
    
    elif block_type == 'code':
        block = block.lstrip('`').rstrip('`')
        return ParentNode(children=[LeafNode(block, tag='code')], tag='pre')
    
    elif block_type == 'quote':
        block = '\n'.join(map(lambda x:x.lstrip('>'), block.split('\n')))
        return LeafNode(block, tag='blockquote')
    
    elif block_type == 'unordered_list':
        block = '\n'.join(map(lambda x:f"<li>{x.lstrip('*- ')}</li>", block.split('\n')))
        return LeafNode(block, tag='ul')
    
    elif block_type == 'ordered_list':
        block = '\n'.join(map(lambda x:f"<li>{x.lstrip('1234567890. ')}</li>", block.split('\n')))
        return LeafNode(block, tag='ol')
    
    elif block_type == 'paragraph':
        return ParentNode(children=list(map(lambda node:text_node_to_html_node(node), text_to_textnodes(block))), tag=f'p')
    

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = [block_to_html(block, block_to_block_type(block)) for block in blocks]
    return ParentNode(children=nodes, tag='div')


def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if re.search(r'^# ', block):
            return block.lstrip('# ')
    raise Exception('All pages need a single <h1>')
    

