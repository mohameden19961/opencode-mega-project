from codeguard.utils.ast_utils import ASTUtils


class TestASTUtils:
    def test_parse_valid(self):
        tree = ASTUtils.parse_safe("x = 1")
        assert tree is not None

    def test_parse_invalid(self):
        tree = ASTUtils.parse_safe("x = ")
        assert tree is None

    def test_get_functions(self):
        tree = ASTUtils.parse_safe("def foo(): pass\ndef bar(): pass")
        funcs = ASTUtils.get_functions(tree)
        assert len(funcs) == 2

    def test_get_classes(self):
        tree = ASTUtils.parse_safe("class A: pass\nclass B: pass")
        classes = ASTUtils.get_classes(tree)
        assert len(classes) == 2
