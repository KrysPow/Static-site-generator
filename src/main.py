from textnode import TextNode
import os
import shutil
from block_to_html import markdown_to_html_node, extract_title

def main():
    # textnode = TextNode('dummy text', 'bold', 'http://www.dummy-site.de')
    # print(textnode)
    copy_contents_from_to('static', 'public')
    generate_pages_recursively('content', 'template.html', 'public')


def copy_contents_from_to(origin_directory:str, destination_directiory:str):
    #check if origin directory exists
    if not os.path.exists(origin_directory):
        raise Exception('origin directory does not exist')
    if os.path.exists(destination_directiory):
        shutil.rmtree(destination_directiory)
    if not os.path.exists(destination_directiory):
        os.mkdir(destination_directiory)
    for item in os.listdir(origin_directory):
        new_or_path = os.path.join(origin_directory, item)
        new_dest_path = os.path.join(destination_directiory, item)
        if os.path.isfile(new_or_path):
            print(new_dest_path)
            shutil.copy(new_or_path, new_dest_path)  
        else:
            print(new_or_path, 'folder')
            os.mkdir(new_dest_path)
            copy_contents_from_to(new_or_path, new_dest_path)


def generate_page(from_path, template_path, dest_path):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')
    f1 = open(from_path)
    f2 = open(template_path)
    f3 = open(dest_path, 'w')
    if not os.path.exists(dest_path):
        os.makedirs(os.path.dirname(dest_path))
    md = f1.read()
    template = f2.read()
    title, content = extract_title(md), markdown_to_html_node(md).to_html()
    f3.write(template.replace('{{ Title }}', title).replace('{{ Content }}', content))
    
    f1.close()
    f2.close()
    f3.close()


def generate_pages_recursively(dir_path_content, template_path, dest_dir_path):
    for item in os.listdir(dir_path_content):
        new_or_path = os.path.join(dir_path_content, item)
        new_dest_path = os.path.join(dest_dir_path, item)
        if os.path.isfile(new_or_path):
            name = new_or_path.split('/')[-1].split('.')[0]
            generate_page(new_or_path, template_path, os.path.join(dest_dir_path, f'{name}.html'))
        else:
            os.mkdir(new_dest_path)
            generate_pages_recursively(new_or_path, template_path, new_dest_path)
    

main()

