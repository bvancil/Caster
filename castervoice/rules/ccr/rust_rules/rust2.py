from dragonfly import MappingRule, Choice

from castervoice.lib.actions import Text, Key
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R


class RustNon(MappingRule):
    mapping = {
        "fun <function_name>": R(Text("%(function_name)s()") + Key("left")),
        "mac <macro_name>": R(Text("%(macro_name)s")),
    }
    extras = [
        Choice("return", {"return": " -> TOKEN "}),
        Choice("function_name", {
            "absolute value": "abs",
            "assert equal": "assert_eq!",
            "debug": "dbg!",
            "drop": "drop",
            "format": "format!",
            "from": "from",
            "length": "len",
            "new": "new",
            "panic": "panic!",
            "print": "print!",
            "print line": "println!",
            "push": "push",
            "unwrap": "unwrap",
        }),
        Choice("macro_name", {
            "vector": "vec!",
        }),
    ]
    defaults = {"return": " "}


def get_rule():
    return RustNon, RuleDetails(name="rust companion")
