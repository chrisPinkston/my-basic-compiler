import itertools
import re

# Define some regular expressions for token matching
# THE CODE BELOW REPRESENTS SYMBOLS SYMBOLS AND EXPRESSIONS THAT WOULD BE USED IN PYTHON
token_exprs = [
    (r'[ \n\t]+', 'space'),  # Whitespace
    (r'#[^\n]*', None),  # Comment
    (r'\(', 'LPAREN'),
    (r'\)', 'RPAREN'),
    (r',', 'comma'),
    (r'\+', 'PLUS'),
    (r'\:', 'then'),
    (r'-', 'MINUS'),
    (r'_', 'dash'),
    (r'\*', 'MULTIPLY'),
    (r'/', 'DIVIDE'),
    (r'=', 'EQUALS'),
    (r'[0-9]+', 'NUMBER'),
    (r'prints [A-Za-z][A-Za-z0-9_]*', 'printSort'),
    (r'print [A-Za-z][A-Za-z0-9_]*', 'print'),
    (r'[A-Za-z][A-Za-z0-9_]*', 'NAME'),
    (r"\'", 'Z'),
    (r'\"', 'Y'),
    (r'\|', 'break')
]


# tokenize() function takes the input text and uses regex to create a token for each expression,
# with a token containing (tag,user text)
def tokenize(text):
    """
    Given some text, return a sequence of tokens.
    Tokens represent pieces of the text. such as characters,operators, and 'prints' statement
    """
    tokens = []
    i = 0
    # while statement goes through each token and prints an error if there is a token not a part of the language
    while i < len(text):
        match = None
        for token_expr in token_exprs:
            pattern, tag = token_expr
            regex = re.compile(pattern)
            match = regex.match(text, i)
            if match:
                value = match.group(0)
                if tag:
                    token = (tag, value)
                    tokens.append(token)
                break
        if not match:
            raise Exception('Illegal character: %s' % text[i])
        else:
            i = match.end(0)

    return tokens


# check_syntax function will go through the generated code and see if
# there is an invalid character at beginning of statement
def check_syntax(tokens):
    split_tokens = [list(group) for k, group in itertools.groupby(tokens, lambda x: x[0] == "break") if not k]
    for token in split_tokens:
        counter = 1
        tag = token[0]
        internal_tag = tag[0]
        if internal_tag == "NAME":
            counter = 0
        if internal_tag == 'space':
            counter = 0
    # first character in statement is false
    if counter == 0:
        return False

    return True


# generate code function takes tokens and then uses syntax function and returns error if false and then
# apends an array called 'code', with each value for the token
def generate_code(tokens):
    """
    Given a sequence of tokens, generate Python code that performs the same
    computation.
    """
    if check_syntax(tokens) == True:
        raise Exception("SYNTAX ERROR: FIRST CHARACTER OF STATMENT SHOULD BE A CHAR/STRING")
    code = []
    for token in tokens:
        # print(token)
        tag, value = token
        if tag == 'NUMBER':
            code.append(value)
        elif tag == 'printSort':
            # arr = sorted(list(value[7:]))
            res = f"text = \"{value[7:]}\"\n" \
                  f"sorted_text = sorted(list(text))\n" \
                  f"print(sorted_text)"
            code.append(res)
        elif tag == 'print':
            printed = f"print(\"{value[6:]}\")"
            code.append(printed)
        elif tag == 'EQUALS':
            code.append('=')
        elif tag == 'then':
            code.append(':')
        elif tag == 'NAME':
            code.append(value)
        elif tag == 'break':
            code.append('\n')
        elif tag == 'dash':
            code.append('_')
        elif tag == 'space':
            code.append(' ')
        elif tag == 'comma':
            code.append(',')
        elif tag == 'PLUS':
            code.append('+')
        elif tag == 'MINUS':
            code.append('-')
        elif tag == 'MULTIPLY':
            code.append('*')
        elif tag == 'DIVIDE':
            code.append('/')
        elif tag == 'LPAREN':
            code.append('(')
        elif tag == 'RPAREN':
            code.append(')')
        elif tag == 'Y':
            code.append('"')
        elif tag == 'Z':
            code.append("'")
    return ''.join(code) + '\n'


# code to use the above functions that will output python code input is text and tokenizes the text to use the
# generate_code function to print as output text that will be working python code.
if __name__ == '__main__':
    text = 'a=b+c|d=2+2'
    tokens = tokenize(text)
    generated_code = generate_code(tokens)
    print(generated_code)


