import unittest

from textnode import TextNode, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_links


class TestTextNode(unittest.TestCase):
    def test_eq_without_url(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_eq_with_url(self):
        node = TextNode("This is a text node", "bold", 'https://www.dummy.de')
        node2 = TextNode("This is a text node", "bold", 'https://www.dummy.de')
        self.assertEqual(node, node2)

    def test_neq_text_property_diff(self):
        node = TextNode('blblblba', 'bold')
        node2 = TextNode('blblblba', 'italic')
        self.assertNotEqual(node, node2)


    def test_split_nodes_code(self):
        node = TextNode('This text has ´code´ in it', 'text')
        self.assertEqual(split_nodes_delimiter([node], '´', 'code'), [TextNode('This text has ', 'text', None), TextNode('code', 'code', None), TextNode(' in it', 'text', None)])

    def test_split_nodes_bold(self):
        node = TextNode('This text has **bold text** in it', 'text')
        self.assertEqual(split_nodes_delimiter([node], '**', 'bold'), [TextNode('This text has ', 'text', None), TextNode('bold text', 'bold', None), TextNode(' in it', 'text', None)])
    
    def test_split_nodes_italic(self):
        node = TextNode('This text has *italic* in it', 'text')
        self.assertEqual(split_nodes_delimiter([node], '*', 'italic'),[TextNode('This text has ', 'text', None), TextNode('italic', 'italic', None), TextNode(' in it', 'text', None)])

    def test_split_nodes_pure_text(self):
        node = TextNode('This is text', 'text')
        self.assertEqual(split_nodes_delimiter([node], '**', 'bold'), [TextNode('This is text', 'text', None)])

    def test_split_nodes_co_bo_it(self):
        node = TextNode('This text has ´code´ in it, additionally **bold text** and *italic* text.', 'text')
        output = split_nodes_delimiter(
                    split_nodes_delimiter(
                        split_nodes_delimiter([node], '´', 'code'), '**', 'bold'), '*', 'italic')
        self.assertEqual(output, [TextNode('This text has ', 'text', None), TextNode('code', 'code', None), TextNode(' in it, additionally ', 'text', None), TextNode('bold text', 'bold', None), TextNode(' and ', 'text', None), TextNode('italic', 'italic', None), TextNode(' text.', 'text', None)])

    def test_split_nodes_multiple_code(self):
        node =TextNode('This is ´code1´and this is ´code2´, also there is some **bold** and *italic* thrown *in*, **haha**', 'text')
        output = split_nodes_delimiter(
                    split_nodes_delimiter(
                        split_nodes_delimiter([node], '´', 'code'), '**', 'bold'), '*', 'italic')
        self.assertEqual(output, [TextNode('This is ', 'text', None),
                                    TextNode('code1', 'code', None),
                                    TextNode('and this is ', 'text', None),
                                    TextNode('code2', 'code', None),
                                    TextNode(', also there is some ', 'text', None),
                                    TextNode('bold', 'bold', None), 
                                    TextNode(' and ', 'text', None),
                                    TextNode('italic', 'italic', None),
                                    TextNode(' thrown ', 'text', None),
                                    TextNode('in', 'italic', None),
                                    TextNode(', ', 'text', None), 
                                    TextNode('haha', 'bold', None), 
                                    TextNode('', 'text', None)])
        
    def test_split_nodes_markdown_syntax_error(self):
        node = TextNode('This is *wrong.', 'text')
        #print(split_nodes_delimiter([node], '*', 'italic'))
        self.assertRaisesRegex(Exception, 'Invalid', split_nodes_delimiter, [node], '*', 'italic')

    
    def test_extract_md_img(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        self.assertEqual(extract_markdown_images(text), [('image', 'https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png'), ('another', 'https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png')])

    def test_extract_md_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        self.assertEqual(extract_markdown_links(text), [('link', 'https://www.example.com'), ('another', 'https://www.example.com/another')])

    def test_split_text_for_imgs(self):
        text = 'This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)'
        text2 = '![bla](blub.de) nada'
        node = TextNode(text, 'text')
        node2 = TextNode(text2, 'test')
        node3 = TextNode('hallo', 'text')
        self.assertEqual(split_nodes_image([node]), [TextNode('This is text with an ', 'text', None), TextNode('image', 'image', 'https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png'), TextNode(' and another ', 'text', None), TextNode('second image', 'image', 'https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png')])
        self.assertEqual(split_nodes_image([node2]), [TextNode('bla', 'image', 'blub.de'), TextNode(' nada', 'text', None)])
        self.assertEqual(split_nodes_image([node, node2]), [TextNode('This is text with an ', 'text', None), TextNode('image', 'image', 'https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png'), TextNode(' and another ', 'text', None), TextNode('second image', 'image', 'https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png'), TextNode('bla', 'image', 'blub.de'), TextNode(' nada', 'text', None)])
        self.assertEqual(split_nodes_image([node3]), [TextNode('hallo', 'text', None)])

    def test_split_text_for_links(self):
        text = 'This is text with an [link](https://googleapis.com) and another [second link](https://storage.googleapis.com)'
        text2 = '[bla_link](blub.de) nada'
        node = TextNode(text, 'text')
        node2 = TextNode(text2, 'test')
        node3 = TextNode('hallo', 'text')
        self.assertEqual(split_nodes_links([node]), [TextNode('This is text with an ', 'text', None), TextNode('link', 'link', 'https://googleapis.com'), TextNode(' and another ', 'text', None), TextNode('second link', 'link', 'https://storage.googleapis.com')])
        self.assertEqual(split_nodes_links([node2]), [TextNode('bla_link', 'link', 'blub.de'), TextNode(' nada', 'text', None)])
        self.assertEqual(split_nodes_links([node, node2]), [TextNode('This is text with an ', 'text', None), TextNode('link', 'link', 'https://googleapis.com'), TextNode(' and another ', 'text', None), TextNode('second link', 'link', 'https://storage.googleapis.com'), TextNode('bla_link', 'link', 'blub.de'), TextNode(' nada', 'text', None)])
        self.assertEqual(split_nodes_links([node3]), [TextNode('hallo', 'text', None)])

if __name__ == "__main__":
    unittest.main()

