import urllib.request
from base64 import b64decode


LIST_URL = 'https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt'
BLACK_FILE = 'gfw.lst'
WHITE_FILE = 'cn.lst'


def convert_line(line):
    if line[0] == '/' and line[-1] == '/':
        return line[1:-1]
    line = line.replace('\n', '')
    line = line.replace(r'/^https?:\/\/', '')
    line = line.replace('*', '.+')
    line = line.replace('(', r'\(').replace(')', r'\)')
    line = line.replace('http://', '')
    line = line.replace('https://', '')
    if line.startswith('||'):
        return '^.*%s.*' % line[2:]
    elif line.startswith('|'):
        return '^.*%s.*' % line[1:]
    elif line[-1] == '|':
        return '^.*%s$' % line
    else:
        return '^.*%s.*' % line


def convert(gfwlist):
    black = open(BLACK_FILE, 'w')
    white = open(WHITE_FILE, 'w')

    for l in gfwlist.split('\n'):
        l = l[:-1]
        if not l or l[0] == '!' or l[0] == '[':
            continue

        if l.startswith('@@'):
            white.write(convert_line(l[2:]) + '\n')
        else:
            black.write(convert_line(l) + '\n')


def main():
    src = urllib.request.urlopen(LIST_URL).read()
    src = b64decode(src).decode('utf-8')
    convert(src)


main()
