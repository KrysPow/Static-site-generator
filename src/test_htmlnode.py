import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node1 = HTMLNode(props={'href':'www.dummy.de', 'target':'blank', 'other':'testyy'})
        self.assertEqual(node1.props_to_html(), ' href="www.dummy.de" target="blank" other="testyy"')

        
    def test_leafnode_1(self):
        l1 = LeafNode(tag="p", value="This is a paragraph of text.")
        self.assertEqual(l1.to_html(), '<p>This is a paragraph of text.</p>')

    def test_leafnode_2(self):
        l2 = LeafNode(tag="a", value="Click me!", props={"href": "https://www.google.com"})   
        self.assertEqual(l2.to_html(), '<a href="https://www.google.com">Click me!</a>')    

    def test_leafnode_3(self):
        l3 = LeafNode(value='normal text')
        self.assertEqual(l3.to_html(), 'normal text')


    def test_parentnode_1(self):
        p =  ParentNode(
            tag="p", 
                children=[
                    LeafNode(tag="b", value="Bold text"),
                    LeafNode(tag=None, value="Normal text"),
                    LeafNode(tag="i", value="italic text"),
                    LeafNode(tag=None, value="Normal text2"),
                ],
            )
        self.assertEqual(p.to_html(), '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text2</p>')
    
    def test_parentnode_2(self):    
        p2 =  ParentNode(
            tag="html", 
                children= [ParentNode(
                    tag="p", 
                        children=[
                            LeafNode(tag="b", value="Bold text"),
                            LeafNode(tag=None, value="Normal text"),
                            LeafNode(tag="i", value="italic text"),
                            LeafNode(tag=None, value="Normal text2"),
                        ],
                    )]
                )
        self.assertEqual(p2.to_html(), '<html><p><b>Bold text</b>Normal text<i>italic text</i>Normal text2</p></html>')

    def test_parentnode_3(self):
        p3 =  ParentNode(
            tag="html", 
                children= [ParentNode(tag="head", children=[
                                        LeafNode(tag="b", value="Bold text"),
                                        LeafNode(tag=None, value="Normal text"),
                                        LeafNode(tag="i", value="italic text"),
                                        LeafNode(tag=None, value="Normal text2"),
                                                       ],
                                        ),
                            ParentNode(tag="body", children=[
                                        LeafNode(tag="b", value="Bold text"),
                                        LeafNode(tag=None, value="Normal text"),
                                        LeafNode(tag="i", value="italic text"),
                                        LeafNode(tag=None, value="Normal text2"),
                                                       ],
                                        )
                            ]
                      )       
        self.assertEqual(p3.to_html(), '<html><head><b>Bold text</b>Normal text<i>italic text</i>Normal text2</head><body><b>Bold text</b>Normal text<i>italic text</i>Normal text2</body></html>')


    def test_parentnode_4(self):
        p4 =  ParentNode(
            tag="p", 
                children=[
                    LeafNode(tag="b", value="Bold text"),
                    LeafNode(tag=None, value="Normal text"),
                    LeafNode(tag="i", value="italic text"),
                    LeafNode(tag=None, value="Normal text2"),
                ],
            props={'key':'value'}
            )
        self.assertEqual(p4.to_html(), '<p key="value"><b>Bold text</b>Normal text<i>italic text</i>Normal text2</p>')
    
    def test_text_to_html_func(self):
        t1 = TextNode('text', 'text')
        t2 = TextNode('text', 'bold')
        t3 = TextNode('text', 'italic')
        t4 = TextNode('text', 'code')
        t5 = TextNode('text', 'link', url='www.test.de')
        t6 = TextNode('text', 'image', url='www.test.de')

        self.assertEqual(text_node_to_html_node(t1).to_html(), 'text')
        self.assertEqual(text_node_to_html_node(t2).to_html(), '<b>text</b>')
        self.assertEqual(text_node_to_html_node(t3).to_html(), '<i>text</i>')
        self.assertEqual(text_node_to_html_node(t4).to_html(), '<code>text</code>')
        self.assertEqual(text_node_to_html_node(t5).to_html(), '<a href="www.test.de">text</a>')
        self.assertEqual(text_node_to_html_node(t6).to_html(), '<img src="www.test.de"></img>')

