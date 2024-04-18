import unittest

from block_to_html import block_to_html, markdown_to_html_node

class TestBlock(unittest.TestCase):
    def test_block_to_html_heading(self):
        heading = '##### heading'
        self.assertEqual(block_to_html(heading, 'heading').to_html(), '<h5>heading</h5>')


    def test_block_to_html_code(self):
        code = '```this is codeblock```'
        self.assertEqual(block_to_html(code, 'code').to_html(), '<pre><code>this is codeblock</code></pre>')

    def test_block_to_html_quote(self):
        quote = '>this is a quote\n>with to two rows'
        self.assertEqual(block_to_html(quote, 'quote').to_html(), '''<blockquote>this is a quote
with to two rows</blockquote>''')
        
    def test_block_to_html_unord_lst(self):
        un_or_lst = '- item 1\n* item 2'
        self.assertEqual(block_to_html(un_or_lst, 'unordered_list').to_html(), '<ul><li>item 1</li>\n<li>item 2</li></ul>')

    def test_block_to_html_ord_lst(self):
        ord_lst = '1. item 1\n2. item 2\n3. item 3'
        self.assertEqual(block_to_html(ord_lst, 'ordered_list').to_html(), '''<ol><li>item 1</li>
<li>item 2</li>
<li>item 3</li></ol>''')
        
    def test_block_to_html_paragraph(self):
        paragraph = 'blabedi blub blbla **bold** oder auch *italic*'
        self.assertEqual(block_to_html(paragraph, 'paragraph').to_html(), '<p>blabedi blub blbla <b>bold</b> oder auch <i>italic</i></p>')


    def test_markdown_to_html_node(self):
        markdown = '''# header

paragraph

```code block```'''
        self.assertEqual(markdown_to_html_node(markdown).to_html(), '<div><h1>header</h1><p>paragraph</p><pre><code>code block</code></pre></div>')
