# -*- coding: utf-8 -*-
from os import system
from os.path import isfile
from random import shuffle, choice

def clean_comments(content: str) -> str:
    return '\n'.join([line for line in content.splitlines() if not line.strip().lower().startswith(('::', 'rem'))])

def generate_substrings() -> dict:
    alphabet = list("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ @=")
    keys = ["VAR" + str(i) for i in range(5)]
    mapping = {}
    for key in keys:
        shuffle(alphabet)
        mapping[key] = ''.join(alphabet)
    return mapping

def obfuscate_with_substrings(content: str, mapping: dict) -> str:
    keys = list(mapping.keys())
    values = list(mapping.values())
    result_lines = []
    for line in content.splitlines():
        if line.startswith(':'):
            result_lines.append(line)
            continue
        new_line = ''
        skip = False
        for ch in line:
            if skip:
                new_line += ch
                if ch in ['%', '!']: skip = False
                continue
            if ch in ['%', '!']:
                skip = True
                new_line += ch
                continue
            for i, val in enumerate(values):
                if ch in val:
                    new_line += f"%{keys[i]}:~{val.find(ch)},1%"
                    break
            else:
                new_line += ch
        result_lines.append(new_line)
    return '\n'.join(result_lines)

def generate_set_lines(mapping: dict) -> list:
    return [f'set "{k}={v}"' for k, v in mapping.items()]

def main():
    print("빠른 배치 난독화 도구")
    filepath = input("배치 파일을 삭제해주세요: ").strip().strip('"')
    if not isfile(filepath):
        print("파일을 찾을 수 없습니다")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    content = clean_comments(content)
    substrs = generate_substrings()
    set_lines = generate_set_lines(substrs)
    obfuscated = obfuscate_with_substrings(content, substrs)

    final_output = "@echo off\n" + '\n'.join(set_lines) + '\n' + obfuscated
    output_path = filepath.rsplit('.', 1)[0] + "-obf.bat"

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_output)

    print("난독화된 배치 파일이 출력되었습니다:", output_path)
    try:
        system('pause >nul')
    except:
        pass

if __name__ == '__main__':
    main()
