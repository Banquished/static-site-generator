import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_single_prop(self):
        node = HTMLNode(props={"class": "greeting"})
        self.assertEqual(node.props_to_html(), ' class="greeting"')

    def test_props_to_html_multiple_props(self):
        node = HTMLNode(props={
            "href": "https://boot.dev",
            "target": "_blank",
        })

        html = node.props_to_html()

        self.assertIn(' href="https://boot.dev"', html)
        self.assertIn(' target="_blank"', html)

    def test_props_to_html_no_props(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")
        
        
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Boot.dev", props={"href": "https://boot.dev"})
        self.assertEqual(node.to_html(), '<a href="https://boot.dev">Boot.dev</a>')


class TestParentNode(unittest.TestCase):
    def test_parent_to_html_div(self):
        child1 = LeafNode("p", "Hello, world!")
        child2 = LeafNode("a", "Boot.dev", props={"href": "https://boot.dev"})
        parent = ParentNode("div", children=[child1, child2], props={"class": "container"})
        
        expected_html = '<div class="container"><p>Hello, world!</p><a href="https://boot.dev">Boot.dev</a></div>'
        self.assertEqual(parent.to_html(), expected_html)
        
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_parent_without_tag_raises_error(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        
        with self.assertRaises(ValueError):
            parent_node.to_html()
    
    def test_parent_without_children_raises_error(self):
        parent_node = ParentNode("div", [])
        
        with self.assertRaises(ValueError):
            parent_node.to_html()
    
    def test_parent_with_none_children_raises_error(self):
        parent_node = ParentNode("div", None)
        
        with self.assertRaises(ValueError):
            parent_node.to_html()
            
    def test_parent_with_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], props={"class": "container"})
        
        self.assertEqual(
            parent_node.to_html(),
            '<div class="container"><span>child</span></div>',
        )
    
    def test_parent_preserves_child_order(self):
        child1 = LeafNode("span", "first")
        child2 = LeafNode("span", "second")
        child3 = LeafNode("span", "third")

        parent_node = ParentNode("div", [child1, child2, child3])

        self.assertEqual(
            parent_node.to_html(),
            "<div><span>first</span><span>second</span><span>third</span></div>",
        )

    def test_parent_with_raw_text_leaf_child(self):
        child_node = LeafNode(None, "plain text")
        parent_node = ParentNode("p", [child_node])

        self.assertEqual(parent_node.to_html(), "<p>plain text</p>")

if __name__ == "__main__":
    unittest.main()
