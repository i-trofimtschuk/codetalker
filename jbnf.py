"""
jbnf.py -> parse my special falvor of bnf.

defines:
    Grammar(text)

examples
<name> : 'L' | <something> | <other><man>+

-- to do the string "'", use ''
-- suffixes:
* `+` one or more of the preceeding
* `*` zero or more of the preceeding
* `:` check for, but do not consume the preceeding
* `+?` non-greedy version
* `*?` non-greedy version
* `~` no big deal if it's not there

comments start with #

"""

import re
import string

class Grammar:
    '''A tool for parsing and storing a grammar.

    >>> g = Grammar('')
    >>> g = Grammar('<start>:\\'hi\\'')
    >>> g = Grammar("<a>:<b>|'4'\\n<b>:'yo'")
    '''
    def __init__(self, text):
        if type(text) not in (str, unicode) and hasattr(text, 'read'):
            text = text.read()
        self.original = text
        self.parse()

    def parse(self):
        self.rules = {}
        self.firsts = {}
        for i,line in enumerate(self.original.split('\n')):
            if not line.startswith('#') and line.strip():
                if not ':' in line:
                    raise Exception, 'invalid bnf on line %d: %s' % (i, line)
                name,body = line.split(':',1)
                self.rules[name.strip()] = self.rulesplit(body.strip())
        for name in self.rules:
            self.loadfirst(name)

    def loadfirst(self, name):
        if name in self.firsts:return self.firsts[name]
        elif name == "'":return ["'"]
        elif name.startswith("'"):
            return [name.strip("'")[0]]
        elif name == 'e':
            return list(string.printable)
        elif name not in self.rules:
            return [name]

        chars = []
        self.firsts[name] = chars
        for child in self.rules[name]:
            chars.append(flatten(self.loadfirst(child[0])))
        return chars

    def rulesplit(self, body):
        """just made much smaller w/ regex =)"""
        pieces = "('[^']*'|<[^>]+>|\||\+|\*|\?|\s|:|~|e)"
        parts = re.findall(pieces, body)
        if ''.join(parts) != body:
            raise BNFException,'Invalid BNF provided: %s' % body
        options = [[]]
        for part in parts:
            if part == '|':
                options.append([])
            elif part == "'\\t'":
                options[-1].append("'\t'")
            elif part == "'\\n'":
                options[-1].append("'\n'")
            elif part in ' \t':
                continue
            else:
                options[-1].append(part)
        return options

def flatten(lst):
    """flatten a nested list"""
    res = []
    for item in lst:
        if type(item) in (tuple,list):
            res += list(flatten(item))
        else:
            res.append(item)
    return res

if __name__=='__main__':
    import doctest
    doctest.testmod()

# vim: et sw=4 sts=4
