#!/usr/bin/env python
"""
Quest 3: building and reading "melody trees".

THE PUZZLE IN BRIEF
-------------------
We are given a list of "nodes". Each node is a little connector piece with:

  * an id        - a unique number
  * a plug       - a colour + shape, e.g. "BLUE HEXAGON"
  * two sockets  - a left socket and a right socket, each a colour + shape
  * some data    - which we can ignore completely

Nodes are assembled one at a time into a tree:

  * The first node in the list is the root (drawn at the bottom).
  * Every later node "circles" the existing tree clockwise, starting at the
    root, and plugs into the first socket it is allowed to connect to.
    Going clockwise from the root means: left socket first, then over the
    top, then the right socket. When a socket is already occupied, the
    walk continues into the node that is plugged in there (its own left
    socket, its own right socket, and so on).

Once the tree is built, a "reading node" circles the tree the same way and
records each node's id as it passes the top of that node (the spot between
its left and right sockets). That produces an ordered list of ids.

The answer ("checksum") is: multiply each id by its 1-based position in that
list, then add everything up.

THE THREE PARTS
---------------
Part 1: A plug only fits a socket if BOTH colour and shape match
        exactly ("strong" bond).
Part 2: A plug also fits if only the colour OR only the shape matches
        ("weak" bond). The node takes the first socket, in clockwise
        order, that gives either kind of bond.
Part 3: Same as part 2, plus one extra rule: if a node meets a socket where
        it could form a STRONG bond, but that socket is currently held by a
        node that only has a WEAK bond there, the newcomer kicks it out.
        The evicted node (carrying anything attached beneath it) goes back
        to circling the tree, resuming just after the new strong bond.
        This can cause chain reactions.

INPUT FORMAT
------------
The file "03.in" holds three blocks of notes, one per part, separated by a
blank line. Each line looks like:

    id=1, plug=BLUE HEXAGON, leftSocket=GREEN CIRCLE, rightSocket=BLUE PENTAGON, data=...

DATA REPRESENTATION
-------------------
No classes are used. Each node is a plain dict:

    {
        "id":    int,        # the node's unique id
        "plug":  str,        # e.g. "BLUE HEXAGON"
        "lsock": str,        # the left socket's colour + shape
        "rsock": str,        # the right socket's colour + shape
        "left":  dict|None,  # node plugged into the left socket, if any
        "right": dict|None,  # node plugged into the right socket, if any
    }

The tree is simply the root node's dict, with children nested via
"left" and "right".

A NOTE ON RECURSION
-------------------
Tree walks below use explicit stacks (plain lists) instead of recursive
function calls. A long, lopsided tree could otherwise exceed Python's
recursion limit.
"""

import re

# Matches one node line and captures four things: id, plug, left socket, right
# socket. The "data=..." part is deliberately ignored.
#   (\d+)       -> the id (digits)
#   ([A-Z ]+)   -> a colour and shape, e.g. "BLUE HEXAGON" (capitals + space)
NODE_RE = re.compile(
    r"id=(\d+),\s*plug=([A-Z ]+),\s*leftSocket=([A-Z ]+),\s*rightSocket=([A-Z ]+),"
)


def read_puzzle_input() -> list[str]:
    """Read the puzzle file and split it into one text block per part.

    Returns:
        A list of strings. Index 0 is the notes for part 1, index 1 for
        part 2, and index 2 for part 3.
    """
    with open("03.in", "r", encoding="utf-8") as file:
        # strip() removes stray whitespace at the file's start/end; splitting
        # on a blank line ("\n\n") separates the parts from each other.
        return file.read().strip().split("\n\n")


def parse_nodes(block: str) -> list[dict]:
    """Turn one block of text into a list of node dicts.

    Args:
        block: The notes for one part, one node per line.

    Returns:
        Node dicts in the same order as the input. Order matters: the first
        one becomes the root and the rest are attached in sequence.
        Every node starts with nothing plugged into either socket.
    """
    nodes = []
    for line in block.splitlines():
        m = NODE_RE.search(line)
        if m:  # skip any line that isn't a node definition
            nodes.append(
                {
                    "id": int(m[1]),
                    "plug": m[2].strip(),
                    "lsock": m[3].strip(),
                    "rsock": m[4].strip(),
                    "left": None,
                    "right": None,
                }
            )
    return nodes


def match_strong(plug: str, socket: str) -> bool:
    """True only if colour AND shape both match (a strong bond).

    Both values are strings like "BLUE HEXAGON", so a strong bond is simply
    the two strings being identical.
    """
    return plug == socket


def match_any(plug: str, socket: str) -> bool:
    """True if the plug fits the socket at all: strong OR weak bond.

    A weak bond means only the colour matches or only the shape matches.
    Anything that is a strong bond also passes this test, because in that
    case both parts match.
    """
    # "BLUE HEXAGON".split() -> ["BLUE", "HEXAGON"] (colour, shape)
    plug_colour, plug_shape = plug.split()
    socket_colour, socket_shape = socket.split()
    return plug_colour == socket_colour or plug_shape == socket_shape


def insert(root: dict, new: dict, matches) -> None:
    """Attach `new` to the tree at the first suitable free socket.

    The new node walks the tree clockwise from the root. At each node the
    order of visiting is:

        1. the left socket (and, if it is occupied, everything below it)
        2. the right socket (and, if it is occupied, everything below it)

    Occupied sockets are never replaced here; the walk just continues into
    the node plugged in there. The first free socket whose shape/colour
    satisfies `matches` is where the new node connects.

    Args:
        root:    The root node of the tree built so far.
        new:     The node to attach (its own left/right must be empty).
        matches: A function (plug, socket) -> bool deciding if a plug fits
                 a socket. Part 1 passes `match_strong`, part 2 `match_any`.

    Raises:
        ValueError: if no socket in the tree accepts the node. The puzzle
                    guarantees this never happens with valid input.
    """
    # The stack holds "to do" items, and the LAST item pushed is handled
    # FIRST. Each item is (what_to_do, node):
    #   "node"  -> visit this node: schedule its left side, then right side
    #   "left"  -> deal with this node's left socket
    #   "right" -> deal with this node's right socket
    work = [("node", root)]
    while work:
        kind, n = work.pop()

        if kind == "node":
            # Push "right" first so that "left" is popped (handled) first.
            work.append(("right", n))
            work.append(("left", n))

        elif kind == "left":
            if n["left"] is None:
                # Free socket: take it if the plug fits, otherwise move on.
                if matches(new["plug"], n["lsock"]):
                    n["left"] = new
                    return
            else:
                # Occupied: walk into the node sitting there. It gets
                # explored before this node's right side, because "right"
                # for this node is still waiting lower on the stack.
                work.append(("node", n["left"]))

        else:  # kind == "right"; same logic as the left side
            if n["right"] is None:
                if matches(new["plug"], n["rsock"]):
                    n["right"] = new
                    return
            else:
                work.append(("node", n["right"]))

    raise ValueError(f"node {new['id']} found no matching socket")


def list_slots(root: dict) -> list[tuple]:
    """Flatten the tree into the clockwise sequence of all its sockets.

    Each socket is described as a pair (parent_node, side), where side is
    "left" or "right". For the socket that is occupied, the sockets of the
    node plugged into it come right after it in the list, mirroring the
    order in which a circling node would meet them.

    Example: root has A on its left, nothing on its right, and A has nothing
    attached. The result is:
        [(root, "left"), (A, "left"), (A, "right"), (root, "right")]

    Args:
        root: The root node of the tree.

    Returns:
        A list of (parent_node, side) pairs in clockwise order.
    """
    out = []
    # Stack items are ("node", node, None) or ("slot", node, side).
    work: list[tuple[str, dict, str | None]] = [("node", root, None)]
    while work:
        kind, n, side = work.pop()

        if kind == "node":
            # Schedule both sockets; push right first so left is handled first.
            work.append(("slot", n, "right"))
            work.append(("slot", n, "left"))
        else:
            out.append((n, side))
            # If something is plugged in here, its sockets are met next,
            # before we move on to this node's other socket.
            if n[side] is not None:
                work.append(("node", n[side], None))
    return out


def subtree_size(root: dict) -> int:
    """Count how many nodes are in the tree below (and including) `root`.

    Order doesn't matter for counting, so the traversal is a simple
    "pop a node, count it, push its children" loop.
    """
    count = 0
    work = [root]
    while work:
        n = work.pop()
        count += 1
        if n["left"] is not None:
            work.append(n["left"])
        if n["right"] is not None:
            work.append(n["right"])
    return count


def insert_breaking(root: dict, new: dict) -> None:
    """Attach `new` to the tree, allowing strong bonds to break weak ones.

    Rules applied at each socket, in clockwise order:

      * Socket is EMPTY: the circling node takes it if its plug fits at all
        (strong or weak).
      * Socket is OCCUPIED: the circling node takes it only if it would form
        a STRONG bond there AND the current occupant's bond is only WEAK.
        The occupant is detached. Strong bonds are never broken, and a weak
        newcomer never displaces anyone.

    A detached node keeps everything that was plugged into it (its whole
    subtree) and goes back to circling the tree. It resumes searching from
    the first socket after the newly placed node and that node's own
    subtree, wrapping back around to the root if it reaches the end.
    That detached node may in turn displace someone else (a chain
    reaction), which is why this is a loop.

    Args:
        root: The root node of the tree built so far.
        new:  The node to attach.

    Raises:
        ValueError: if a circling node finds nowhere to connect. The puzzle
                    guarantees this never happens with valid input.
    """
    cur = new  # the node currently circling the tree looking for a home
    start = 0  # index in the slot list where its search begins

    while cur is not None:
        # Rebuild the slot list each round, because the tree changes
        # whenever a node is placed or displaced.
        slots = list_slots(root)
        total = len(slots)
        displaced = None  # becomes the evicted node, if there is one

        # Try every socket once, starting at `start` and wrapping around.
        for k in range(total):
            idx = (start + k) % total
            parent, side = slots[idx]
            # The socket's colour+shape, taken from the parent node.
            sock = parent["lsock" if side == "left" else "rsock"]
            occupant = parent[side]

            if occupant is None:
                # Free socket: any fitting plug (strong or weak) will do.
                if match_any(cur["plug"], sock):
                    parent[side] = cur
                    break  # placed; nobody was displaced
            elif match_strong(cur["plug"], sock) and not match_strong(
                occupant["plug"], sock
            ):
                # Occupied, and we'd bond strongly where the occupant only
                # bonds weakly: take over its place.
                parent[side] = cur
                displaced = occupant
                # Where does the evicted node resume? Slots in the
                # (rebuilt) list, in order, are:
                #   idx                    -> this socket (now holding `cur`)
                #   idx+1 ... idx+2*size   -> `cur`'s subtree sockets (each
                #                             node contributes two)
                # so the first socket beyond all of that is:
                start = idx + 1 + 2 * subtree_size(cur)
                break
        else:
            # The for-loop finished without a `break`: no socket accepted
            # this node anywhere in the tree.
            raise ValueError(f"node {cur['id']} found no matching socket")

        # If someone was evicted they become the next circling node;
        # otherwise this is None and the while-loop ends.
        cur = displaced


def read_order(root: dict) -> list[int]:
    """Return the node ids in the order the "reading node" would read them.

    The reader circles the tree clockwise and reads each node at its top,
    which lies between the left and right sockets. So for every node we
    read everything hanging off its left socket first, then the node
    itself, then everything off its right socket. This is the standard
    "in-order traversal" of a binary tree.

    Args:
        root: The root node of the finished tree.

    Returns:
        The list of ids in reading order.
    """
    ids = []
    stack = []  # nodes we have descended through but not yet read
    n = root
    while stack or n is not None:
        # Go as far left as possible, remembering the path on the way down.
        while n is not None:
            stack.append(n)
            n = n["left"]
        # Nothing further left: read this node...
        n = stack.pop()
        ids.append(n["id"])
        # ...then continue with whatever hangs off its right socket.
        n = n["right"]
    return ids


def checksum(block: str, matches, breaking: bool = False) -> int:
    """Build the tree for one block of notes and compute the checksum.

    Args:
        block:    The text notes for one part (one node per line).
        matches:  The plug/socket matching rule (used when `breaking` is
                  False; part 3 has its own built-in rules).
        breaking: If True, use the part 3 rules where strong bonds can
                  displace weak ones.

    Returns:
        The sum of (position * id) over the reading order, where position
        starts at 1.
    """
    nodes = parse_nodes(block)
    root = nodes[0]  # the first node in the list is always the root

    # Attach every remaining node, one at a time, in list order.
    for node in nodes[1:]:
        if breaking:
            insert_breaking(root, node)
        else:
            insert(root, node, matches)

    # enumerate(..., start=1) pairs each id with its 1-based position.
    return sum(pos * node_id for pos, node_id in enumerate(read_order(root), start=1))


def part_one(data: list) -> int:
    """Part 1: strong bonds only (colour and shape must both match)."""
    return checksum(data[0], match_strong)


def part_two(data: list) -> int:
    """Part 2: strong or weak bonds, first socket that fits wins."""
    return checksum(data[1], match_any)


def part_three(data: list) -> int:
    """Part 3: strong or weak bonds, and strong bonds can break weak ones."""
    return checksum(data[2], match_any, breaking=True)


if __name__ == "__main__":
    data = read_puzzle_input()
    print("Part 1:", part_one(data))  # 5983
    print("Part 2:", part_two(data))  # 319911
    print("Part 3:", part_three(data))  # 398153
