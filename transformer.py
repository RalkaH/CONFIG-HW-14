from lark import Transformer
import xml.etree.ElementTree as ET
import math


class XMLTransformer(Transformer):
    
    def __init__(self):
        super().__init__()
        self.constants = {}
        self.root = ET.Element('config')
    
    def start(self, items):
        for item in items:
            if item is not None:
                if isinstance(item, ET.Element):
                    self.root.append(item)
                else:
                    elem = ET.Element('value')
                    elem.text = str(item)
                    self.root.append(elem)
        return self.root
    
    def statement(self, items):
        return items[0] if items else None
    
    def comment(self, items):
        return None
    
    def REM_COMMENT(self, token):
        return None
    
    def MULTILINE_COMMENT(self, token):
        return None
    
    def const_decl(self, items):
        name = str(items[0])
        value = items[1]
        
        if isinstance(value, (int, float)):
            value_text = str(value)
            self.constants[name] = float(value_text)
        elif isinstance(value, ET.Element):
            value_text = value.text if value.text else "0.0"
            self.constants[name] = float(value_text)
        else:
            value_text = str(value)
            try:
                self.constants[name] = float(value_text)
            except ValueError:
                self.constants[name] = value_text
        
        elem = ET.Element('constant')
        elem.set('name', name)
        elem.text = value_text
        return elem
    
    def value(self, items):
        item = items[0]
        if isinstance(item, ET.Element):
            return item
        else:
            elem = ET.Element('value')
            elem.text = str(item)
            return elem
    
    def array(self, items):
        elem = ET.Element('array')
        for item in items:
            if isinstance(item, ET.Element):
                child = ET.SubElement(elem, 'item')
                child.text = item.text
            else:
                child = ET.SubElement(elem, 'item')
                child.text = str(item)
        return elem
    
    def const_expr(self, items):
        result = items[0]
        elem = ET.Element('expression')
        elem.text = str(result)
        return elem
    
    def add(self, items):
        left = float(items[0])
        right = float(items[1])
        return left + right
    
    def pow(self, items):
        base = float(items[0])
        exponent = float(items[1])
        return math.pow(base, exponent)
    
    def ord(self, items):
        string_token = items[0]
        string_value = str(string_token).strip('@"').strip('"')
        if len(string_value) > 0:
            return float(ord(string_value[0]))
        return 0.0
    
    def var(self, items):
        var_name = str(items[0])
        if var_name in self.constants:
            val = self.constants[var_name]
            if isinstance(val, (int, float)):
                return val
            return float(val)
        raise NameError(f"Константа '{var_name}' не определена")
    
    def number(self, items):
        return float(items[0])
    
    def parens(self, items):
        return items[0]
    
    def NUMBER(self, token):
        return str(token)
    
    def STRING(self, token):
        return str(token)
    
    def NAME(self, token):
        return str(token)


if __name__ == '__main__':
    from parser import ConfigParser
    
    parser = ConfigParser()
    transformer = XMLTransformer()
    
    test_code = """
    REM Тест трансформации
    const x = 5.0;
    const y = 10.0;
    !{x + y}
    [@"hello" @"world"]
    !{pow(2.0, 3.0)}
    """
    
    tree = parser.parse(test_code)
    xml_result = transformer.transform(tree)
    
    xml_string = ET.tostring(xml_result, encoding='unicode', xml_declaration=True)
    print("✅ XML сгенерирован!")
    print(xml_string)
