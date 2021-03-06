from itertools import permutations

with open("input-18.txt") as f:
    input = f.read().splitlines()


class Node:
    def __init__(self, left=None, right=None, value=None):
        self.left = left
        self.right = right
        self.value = value

    @property
    def plain(self):
        return (
            self.value is None
            and self.left.value is not None
            and self.right.value is not None
        )

    @property
    def magnitude(self):
        if self.value is not None:
            return self.value
        return 3 * self.left.magnitude + 2 * self.right.magnitude

    def __repr__(self):
        if self.value is not None:
            return str(self.value)
        return f"[{self.left},{self.right}]"


def find_match(string, left=0):
    depth = 0
    for i, c in enumerate(string[left:]):
        if c == "[":
            depth += 1
        elif c == "]":
            depth -= 1
        if depth == 0:
            return i + left + 1


def parse(string):
    result = Node()
    if string[0] in "0123456789":
        return Node(value=int(string[0]))
    elif string[0] == "[":
        left = 1
        right = find_match(string, left)
        result.left = parse(string[left:right])
        result.right = parse(string[right + 1 :])
    return result


def traverse(root, depth=0):
    yield root, depth
    if root.left:
        yield from traverse(root.left, depth + 1)
    if root.right:
        yield from traverse(root.right, depth + 1)


def traverse_values(root):
    for node, _ in traverse(root):
        if node.value is not None:
            yield node


def explode(tree):
    target = None
    for child, depth in traverse(tree):
        if child.plain and depth >= 4:
            target = child
            break
    if not target:
        return False

    values = traverse_values(tree)
    before = None
    for node in values:
        if node is target.left:
            break
        before = node
    assert next(values) is target.right
    after = next(values, None)
    if before:
        before.value += target.left.value
    if after:
        after.value += target.right.value

    target.right = None
    target.left = None
    target.value = 0
    return True


def split(tree):
    for node in traverse_values(tree):
        if node.value > 9:
            node.left = Node(value=node.value // 2)
            node.right = Node(value=(node.value + 1) // 2)
            node.value = None
            return True
    return False


def reduce(tree):
    while True:
        if explode(tree):
            continue
        if split(tree):
            continue
        return tree


left = parse(input[0])
for right in input[1:]:
    left = reduce(Node(left=left, right=parse(right)))
print("1:", left.magnitude)

m = -9999
for a, b in permutations(input, 2):
    m = max(m, reduce(Node(parse(a), parse(b))).magnitude)
print("2:", m)
