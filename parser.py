from lark import Lark, LarkError
from pathlib import Path


class ConfigParser:
    
    def __init__(self, grammar_file='grammar.lark'):
        grammar_path = Path(grammar_file)
        if not grammar_path.exists():
            raise FileNotFoundError(f"Файл грамматики не найден: {grammar_file}")
        
        with open(grammar_path, 'r', encoding='utf-8') as f:
            grammar_text = f.read()
        
        self.parser = Lark(
            grammar_text,
            start='start',
            parser='lalr',
            propagate_positions=True
        )
    
    def parse(self, input_text):
        try:
            tree = self.parser.parse(input_text)
            return tree
        except LarkError as e:
            raise SyntaxError(f"Синтаксическая ошибка: {e}")
    
    def parse_file(self, filepath):
        file_path = Path(filepath)
        if not file_path.exists():
            raise FileNotFoundError(f"Файл не найден: {filepath}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return self.parse(content)


if __name__ == '__main__':
    parser = ConfigParser()
    
    test_code = """
    REM Тестовый файл
    const pi = 3.14;
    const name = @"Test";
    [1.0 2.0 3.0]
    """
    
    try:
        tree = parser.parse(test_code)
        print("✅ Парсинг успешен!")
        print(tree.pretty())
    except SyntaxError as e:
        print(f"❌ {e}")
