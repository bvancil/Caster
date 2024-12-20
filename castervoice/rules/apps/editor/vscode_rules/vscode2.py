from dragonfly import Function, Repeat, Choice, Dictation, MappingRule, Pause, ShortIntegerRef

from castervoice.lib.actions import Key, Mouse

from castervoice.lib import navigation
from castervoice.lib.actions import Text
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R


def _find_nth_token(text, n, direction):
    Key("c-f").execute()
    Text("%(text)s").execute({"text": text})
    if direction == "reverse":
        print("yeah? %(n)d")
        Key("s-enter:%(n)d").execute({"n": n})
    else:
        Key("enter:%(n)d").execute({"n": n})
        print("no? %(n)d")
    Key('escape').execute()


class VSCodeNonCcrRule(MappingRule):
    """
    https://code.visualstudio.com/docs/getstarted/keybindings
    https://code.visualstudio.com/shortcuts/keyboard-shortcuts-windows.pdf
    """
    mapping = {
        # General
        "[(open|show)] command palette [<text>]":
            R(Key("cs-p") + Text("%(text)s"), rdescript="VS Code: Command Palette"),
        "(open file | go to [tab]) [<text>]":
            R(Key("c-p") + Text("%(text)s"), rdescript="VS Code: Go to File without using dialogbox"),
        "new window":
            R(Key("cs-n")),
        "close window":
            R(Key("cs-w")),
        "settings":
            R(Key("c-comma"), rdescript="VS Code: User/workspace Settings"),
        "keyboard shortcuts":
            R(Key("c-k, c-s")),

        # Basic editing
        "move <vertical_direction> [<n>]": R(Key("a-%(vertical_direction)s") * Repeat(extra='n')),
        "copy <vertical_direction> [<n>]": R(Key("sa-%(vertical_direction)s") * Repeat(extra='n')),
        "delete line": R(Key("cs-k")),
        "insert line below": R(Key("c-enter")),
        "insert line above": R(Key("cs-enter")),
        "jump to matching bracket": R(Key("cs-backslash")),
        "indent line": R(Key("c-rbracket")),
        "outdent line": R(Key("c-lbracket")),
        "scroll <vertical_direction> [<n>]":
            R(Key("c-%(vertical_direction)s") * Repeat(extra='n')),
        "scroll page <vertical_direction> [<n>]":
            R(Key("a-pg%(vertical_direction)s") * Repeat(extra='n')),
        ## Collapsing
        "(fold | collapse) region":
            R(Key("cs-lbracket")),
        "(unfold | uncollapse) region":
            R(Key("cs-rbracket")),
        "(fold | collapse) [all] subregions":
            R(Key("c-k, c-lbracket")),
        "(unfold | uncollapse) [all] subregions":
            R(Key("c-k, c-rbracket")),
        "(fold | collapse) [all] regions":
            R(Key("c-k, c-0")),
        "(unfold | uncollapse) [all] regions":
            R(Key("c-k, c-j")),
        ##
        "add line comment": R(Key("c-k, c-c")),
        "remove line comment": R(Key("c-k, c-u")),
        "toggle line comment": R(Key("c-slash")),
        "toggle block comment": R(Key("sa-a")),
        "toggle word wrap":
            R(Key("a-z")),
        
        # Navigation
        "show all symbols":
            R(Key("c-t")),
        "[(go to | jump [to])] line <n>":
            R(Key("c-g") + Text("%(n)d") + Key("enter")),
        "go to symbol":
            R(Key("cs-o")),
        "toggle problems [panel]":
            R(Key("cs-m")),
        "next error":
            R(Key("f8")),  # doesn't seem to be working properly
        "(prior | previous) error":
            R(Key("s-f8")),
        "navigate editor group history": R(Key("cs-tab")),
        "go back [<n>]":
            R(Key("a-left") * Repeat(extra='n')),
        "go forward [<n>]":
            R(Key("a-right")) * Repeat(extra="n"),
        "toggle tab moves focus":
            R(Key("c-m")),
        
        # Search and replace
        "(search | find)":
            R(Key("c-f")),
        "replace":
            R(Key("c-h")),
        "next find":
            R(Key("f3")),
        "(prior | previous) find":
            R(Key("s-f3")),
        "select all occurrences":
            R(Key("a-enter")),
        "add selection to next find match": R(Key("c-d")),
        "move last selection to next find match": R(Key("c-k, c-d")),
        "toggle case sensitive":
            R(Key("a-c"), rdescript="VS Code: Toggle Find Case Sensitive"),
        "toggle regex":
            R(Key("a-r"), rdescript="VS Code: Toggle Find Regular Expressions"),
        "toggle whole word":
            R(Key("a-w"), rdescript="VS Code: Toggle Find Whole Word"),

        "(find | jump [to]) next <text>":
            R(Function(_find_nth_token, n=1, direction="forward")),
        "(find | jump [to]) previous <text>":
            R(Function(_find_nth_token, n=1, direction="reverse")),
        
        # Multi-cursor and selection
        "(insert cursor|altar kick)":
            R(Key("alt:down") + Mouse("left") + Key("alt:up")),
        "insert cursor <vertical_direction> [<n>]": R(Key("ca-%(vertical_direction)s") * Repeat(extra='n')),
        "undo cursor": R(Key("c-u")),
        "insert cursors at line ends": R(Key("sa-i")),
        "select current line": R(Key("c-l")),
        "select all occurrences of selection": R(Key("cs-l")),
        "select all occurrences of word": R(Key("c-f2")),
        "expand selection": R(Key("sa-right")),
        "shrink selection": R(Key("sa-left")),
        "(column|box) selection <direction> [<n>]": R(Key("csa-%(direction)s") * Repeat(extra='n')),
        "(column|box) selection page <vertical_direction> [<n>]": R(Key("csa-pg%(vertical_direction)s") * Repeat(extra='n')),

        # Rich languages editing
        "trigger suggestion": R(Key("c-space, c-i")),
        "trigger parameter hints": R(Key("cs-space")),
                # Languages Editing
        "format (doc | document)":
            R(Key("sa-f")),
        "format (that | selection)":
            R(Key("c-k, c-f")),
        "go to definition":
            R(Key("f12")),
        # REVIEWME: Check that this is working properly
        "go to required definition":
            R(Key("c-f12:2, c-right:5, left/50, f12")),
        "peek definition":
            R(Key("a-f12")),
        "(definition to side | side def)":
            R(Key("c-k, f12")),
        "quick fix": R(Key("c-period")),
        "show references":
            R(Key("s-f12")),
        "rename symbol":
            R(Key("f2")),
        "trim [trailing] whitespace":
            R(Key("c-k, c-x")),
        "change file language":
            R(Key("c-k, m")),

        # Editor Management
        "close editor":
            R(Key("c-w")),
        "close folder":
            R(Key("c-k, f")),
        "split editor":
            R(Key("c-backslash")),
        "(group|pane) <n>":
            R(Key("c-%(n)s")),
        "next (pane|group)":
            R(Key("c-k, c-right")),
        "previous (pane|group)":
            R(Key("c-k, c-left")),
        "move (tab|editor) (left|lease)":
            R(Key("ca-pgup"),
            rdescript="VS Code: Move the current tab to the editor pane on the left."),
        "move (tab|editor) (right|ross)":
            R(Key("ca-pgdown"),
            rdescript="VS Code: Move the current tab to the editor pane on the right."),
        "move group left":
            R(Key("c-k, (left|lease)"),
              rdescript="VS Code: Move Current Group of Tabs to the Left E.g. Swap with Pane to the Left"),
        "move group right":
            R(Key("c-k, (right|ross)"),
              rdescript="VS Code: Move Current Group of Tabs to the Right E.g. Swap with Pane to the Right"
              ),
        ## Custom
        "tab <n>":
            R(Key("a-%(n)s")),
        
        # File management
        "new file":
            R(Key("c-n")),
        "open dialogue":
            R(Key("c-o"), rdescript="VS Code: open file dialogbox"),
        "save as":
            R(Key("cs-s")),
        "save all":
            R(Key("c-k, s")),
        "close (tab|editor) [<n>]":
            R(Key("c-f4/20") * Repeat(extra='n')),
        "close all": R(Key("c-k, c-w")),
        "reopen (tab|editor) [<n>]":
            R(Key("cs-t") * Repeat(extra='n')),
        "keep open":
            R(Key("c-k, enter")),
        "open next [<n>]":
            R(Key("c-tab") * Repeat(extra='n')),
        "open previous [<n>]":
            R(Key("cs-tab") * Repeat(extra='n')),
        "copy path":
            R(Key("c-k, p")),
        "reveal in explorer":
            R(Key("c-k, r")),
        "show active file in new window":
            R(Key("c-k, o")),
        ## older
        "open project [<text>]":
            R(Key("c-r") + Pause("30") + Text("%(text)s")),
        "open folder":
            R(Key("c-k, c-o"), rdescript="VS Code: Open folder"),
        "close workspace":
            R(Key("c-k, f")),
        "next tab [<n>]":
            R(Key("c-pgdown") * Repeat(extra='n')),
        "previous tab [<n>]":
            R(Key("c-pgup") * Repeat(extra='n')),
        
        # Display
        # note that most of these can be turned on/off with the same command
        "[toggle] full screen":
            R(Key("f11")),
        "toggle editor layout":
            R(Key("sa-0")),
        "zoom in [<n>]":
            R(Key("c-equal") * Repeat(extra='n')),
        "zoom out [<n>]":
            R(Key("c-minus") * Repeat(extra='n')),
        "sidebar":
            R(Key("c-b")),
        "explorer":
            R(Key("cs-e")),
        "search|find in files":
            R(Key("cs-f")),
        "source control":
            R(Key("cs-g/10, g")),
        "debug": R(Key("cs-d")),
        "extensions":
            R(Key("cs-x")),
        "replace in files":
            R(Key("cs-h")),
        "search details":
            R(Key("cs-j")),
        "output panel":
            R(Key("cs-u")),
        "markdown preview":
            R(Key("cs-v")),
        "markdown preview side":
            R(Key("c-k, v")),
        "Zen mode":
            # note: use esc esc to exit
            R(Key("c-k, z")),
        "snippets":
            R(Key("a-f, p, down:4, enter"), rdescript="VS Code: User Snippets"),

        # Debugging
        "[toggle] breakpoint":
            R(Key("f9")),
        "continue":
            R(Key("f5"), rdescript="VS Code: Start/Continue"),
        "stopper":
            R(Key("s-f5")),
        "step into":
            R(Key("f11")),
        "step out [of]":
            R(Key("s-f11")),
        "step over [<n>]":
            R(Key("f10/50") * Repeat(extra='n')),
        "(show hover|mouse hover|hover mouse)":
            R(Key("c-k, c-i"),
              rdescript="Show the little box as if you are hovering your mouse over the place where the cursor (As opposed to the mouse pointer) currently is"
              ),
        
        # Integrated Terminal
        "show terminal": R(Key("c-backtick")),
        "new terminal":
            R(Key("cs-backtick")),
        "terminal <vertical_direction> [<n>]": R(Key("c-%(vertical_direction)s") * Repeat(extra='n')),
        "terminal page <vertical_direction> [<n>]": R(Key("s-pg%(vertical_direction)s") * Repeat(extra='n')),

        # requires gitlens extension
        "toggle blame":
            R(Key("cs-g, b")),
        "lens commit details":
            R(Key("cs-g, c")),
        "lens file history":
            R(Key("cs-g, h")),
        "lens repo status":
            R(Key("cs-g, s")),
        "toggle git lens":
            R(Key("cs-g, s-b")),

        # requires bookmark extension
        "mark (prev | prior | previous)":
            R(Key("ca-j")),
        "mark next":
            R(Key("ca-l")),
        
        # Copilot
        "in-line chat": R(Key("c-i")),
        "open chat": R(Key("ca-i")),
        "open copilot edits": R(Key("cs-i")),
        "quick chat": R(Key("csa-l")), 
        
        # Moving around a file
        "<action> [line] <ln1> [by <ln2>]":
            R(Function(navigation.action_lines)),
        "join line":
            R(Key("f1") + Text("join lines") + Key("enter")),

        # custom
        "run build":
            R(Key("cs-b")),
        "toggle console": R(Key("c-j")),
        "initial warning or error": R(Text("^(WARNING|ERROR):")),

    }
    extras = [
        Dictation("text"),
        Dictation("mim"),
        ShortIntegerRef("ln1", 1, 1000),
        ShortIntegerRef("ln2", 1, 1000),
        ShortIntegerRef("n", 1, 1000),
        Choice("action", navigation.actions),
        Choice(
            "nth", {
                "first": "1",
                "second": "2",
                "third": "3",
                "fourth": "4",
                "fifth": "5",
                "sixth": "6",
            }),
        Choice("vertical_direction", {
            "sauce": "up",
            "dunce": "down",
        }),
        Choice("direction", {
            "sauce": "up",
            "dunce": "down",
            "lease": "left",
            "ross": "right",
        }),
    ]
    defaults = {"n": 1, "ln2": "",  "mim": "", "text": ""}


def get_rule():
    details = RuleDetails(name="Visual Studio Code",
                          executable="code",
                          title="Visual Studio Code")
    return VSCodeNonCcrRule, details
