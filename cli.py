import argparse
import sys
import xml.etree.ElementTree as ET
from xml.dom import minidom
from pathlib import Path
from parser import ConfigParser
from transformer import XMLTransformer


def prettify_xml(elem):
    rough_string = ET.tostring(elem, encoding='unicode')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def main():
    parser = argparse.ArgumentParser(
        description='Парсер конфигурационного языка в XML'
    )
    parser.add_argument(
        '-i', '--input',
        required=True,
        help='Путь к входному файлу с конфигурацией'
    )
    parser.add_argument(
        '-o', '--output',
        required=True,
        help='Путь к выходному XML файлу'
    )
    
    args = parser.parse_args()
    
    try:
        config_parser = ConfigParser()
        
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"❌ Ошибка: Входной файл не найден: {args.input}")
            sys.exit(1)
        
        with open(input_path, 'r', encoding='utf-8') as f:
            input_text = f.read()
        
        tree = config_parser.parse(input_text)
        
        transformer = XMLTransformer()
        xml_tree = transformer.transform(tree)
        
        xml_string = prettify_xml(xml_tree)
        
        output_path = Path(args.output)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(xml_string)
        
        print(f"✅ Успешно! XML сохранён в: {args.output}")
        
    except SyntaxError as e:
        print(f"❌ {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
