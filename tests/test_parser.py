import pytest
from parser import ConfigParser
from transformer import XMLTransformer
from lark.exceptions import VisitError
import xml.etree.ElementTree as ET


def test_single_line_comment():
    parser = ConfigParser()
    result = parser.parse("REM Это комментарий")
    assert result is not None


def test_multiline_comment():
    parser = ConfigParser()
    result = parser.parse("(comment\nМного\nстрок\n)")
    assert result is not None


def test_number():
    parser = ConfigParser()
    result = parser.parse("123.456")
    assert result is not None


def test_negative_number():
    parser = ConfigParser()
    result = parser.parse("-123.456")
    assert result is not None


def test_positive_number():
    parser = ConfigParser()
    result = parser.parse("+99.99")
    assert result is not None


def test_string():
    parser = ConfigParser()
    result = parser.parse('@"Hello World"')
    assert result is not None


def test_array_empty():
    parser = ConfigParser()
    result = parser.parse('[]')
    assert result is not None


def test_array_with_numbers():
    parser = ConfigParser()
    result = parser.parse('[1.0 2.0 3.0]')
    assert result is not None


def test_array_with_strings():
    parser = ConfigParser()
    result = parser.parse('[@"a" @"b" @"c"]')
    assert result is not None


def test_array_nested():
    parser = ConfigParser()
    result = parser.parse('[[1.0 2.0] [3.0 4.0]]')
    assert result is not None


def test_constant_declaration():
    parser = ConfigParser()
    result = parser.parse('const x = 10.5;')
    assert result is not None


def test_constant_with_string():
    parser = ConfigParser()
    result = parser.parse('const name = @"test";')
    assert result is not None


def test_constant_with_array():
    parser = ConfigParser()
    result = parser.parse('const arr = [1.0 2.0];')
    assert result is not None


def test_constant_expression_add():
    parser = ConfigParser()
    transformer = XMLTransformer()
    code = 'const x = 5.0;\nconst y = 3.0;\n!{x + y}'
    tree = parser.parse(code)
    result = transformer.transform(tree)
    expressions = result.findall('.//expression')
    assert len(expressions) > 0
    assert expressions[0].text == '8.0'


def test_constant_expression_pow():
    parser = ConfigParser()
    transformer = XMLTransformer()
    code = '!{pow(2.0, 3.0)}'
    tree = parser.parse(code)
    result = transformer.transform(tree)
    expressions = result.findall('.//expression')
    assert expressions[0].text == '8.0'


def test_constant_expression_ord():
    parser = ConfigParser()
    transformer = XMLTransformer()
    code = '!{ord(@"A")}'
    tree = parser.parse(code)
    result = transformer.transform(tree)
    expressions = result.findall('.//expression')
    assert expressions[0].text == '65.0'


def test_complex_expression():
    parser = ConfigParser()
    transformer = XMLTransformer()
    code = 'const x = 10.0;\n!{x + pow(2.0, 3.0)}'
    tree = parser.parse(code)
    result = transformer.transform(tree)
    expressions = result.findall('.//expression')
    assert expressions[0].text == '18.0'


def test_nested_expressions():
    parser = ConfigParser()
    transformer = XMLTransformer()
    code = '!{pow(2.0, 3.0) + pow(3.0, 2.0)}'
    tree = parser.parse(code)
    result = transformer.transform(tree)
    expressions = result.findall('.//expression')
    assert expressions[0].text == '17.0'


def test_syntax_error_missing_semicolon():
    parser = ConfigParser()
    with pytest.raises(SyntaxError):
        parser.parse('const x = 10.0')


def test_syntax_error_invalid_name():
    parser = ConfigParser()
    with pytest.raises(SyntaxError):
        parser.parse('const 123invalid = 10.0;')


def test_syntax_error_unclosed_comment():
    parser = ConfigParser()
    with pytest.raises(SyntaxError):
        parser.parse('(comment unclosed')


def test_syntax_error_unclosed_array():
    parser = ConfigParser()
    with pytest.raises(SyntaxError):
        parser.parse('[1.0 2.0')


def test_undefined_constant():
    parser = ConfigParser()
    transformer = XMLTransformer()
    code = '!{undefined_var + 1.0}'
    tree = parser.parse(code)
    with pytest.raises(VisitError):
        transformer.transform(tree)


def test_full_config():
    parser = ConfigParser()
    transformer = XMLTransformer()
    code = """
    REM Полный тест
    const port = 8080.0;
    const timeout = 30.0;
    
    (comment
    Многострочный комментарий
    для теста
    )
    
    @"server"
    !{port + timeout}
    [1.0 2.0 3.0]
    !{pow(2.0, 4.0)}
    !{ord(@"Z")}
    """
    tree = parser.parse(code)
    result = transformer.transform(tree)
    assert result.tag == 'config'
    assert len(result.findall('.//constant')) == 2
    assert len(result.findall('.//expression')) == 3
