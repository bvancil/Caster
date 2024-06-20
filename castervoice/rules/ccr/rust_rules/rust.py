from symtable import Symbol
from dragonfly import Choice, ShortIntegerRef

from castervoice.rules.core.alphabet_rules import alphabet_support # Manually change import path if in user directory.
from castervoice.lib.actions import Text, Key
from castervoice.rules.ccr.standard import SymbolSpecs
from castervoice.lib.const import CCRType
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.merge.state.short import R


class Rust(MergeRule):

    pronunciation = "rust"

    mapping = {
        SymbolSpecs.IF:
            R(Text("if ")),
        SymbolSpecs.ELSE:
            R(Text("else ")),
        #
        SymbolSpecs.SWITCH:
            R(Text("match ")),
        SymbolSpecs.CASE:
            R(Text(" => ")),
        SymbolSpecs.BREAK:
            R(Text("break;")),
        SymbolSpecs.DEFAULT:
            R(Text("_")),
        #
        SymbolSpecs.DO_LOOP:
            R(Text("loop ")),
        SymbolSpecs.WHILE_LOOP:
            R(Text("while ")),
        SymbolSpecs.FOR_LOOP:
            R(Text("for ")),
        "in": R(Text("in ")),
        SymbolSpecs.FOR_EACH_LOOP:
            R(Text("for ")),
        #
        SymbolSpecs.TO_INTEGER:
            R(Text("parse::<i32>().unwrap()")),
        SymbolSpecs.TO_FLOAT:
            R(Text("parse::<f64>().unwrap()")),
        SymbolSpecs.TO_STRING:
            R(Text("to_string()")),
        #
        SymbolSpecs.AND:
            R(Text(" && ")),
        SymbolSpecs.OR:
            R(Text(" || ")),
        SymbolSpecs.NOT:
            R(Text("!")),
        #
        SymbolSpecs.SYSOUT:
            R(Text("println!()") + Key("left")),
        #
        SymbolSpecs.IMPORT:
            R(Text("use ")),
        #
        # function moved to ncmap
        SymbolSpecs.CLASS:
            R(Text("struct ")),
        #
        SymbolSpecs.COMMENT:
            R(Text("// ")),
        SymbolSpecs.LONG_COMMENT:
            R(Text("/// ")),
        #
        SymbolSpecs.NULL:
            R(Text("None")),
        #
        SymbolSpecs.RETURN:
            R(Text("return ")),
        #
        SymbolSpecs.TRUE:
            R(Text("true")),
        SymbolSpecs.FALSE:
            R(Text("false")),

        # Rust specific
        "value some":
            R(Text("Some()") + Key("left")),
        "enumerate for loop [of <a> [in <n>]]":
            R(Text("for (%(a)s, TOKEN) in (0..%(n)d).enumerate() {}") + Key("left")),
        "enumerate for each [<a> <b>]":
            R(Text("for (%(a)s, %(b)s) in TOKEN.enumerate() {}") + Key("left")),
        "(let|bind) [<mutability>]":
            R(Text("let %(mutability)s")),
        "of type":
            R(Text(": ")),
        "with elements of": R(Text("<>") + Key("left")),
        "array [of] size <n>":
            R(Text("[TOKEN; %(n)d]")),
        "macro vector":
            R(Text("vec![]") + Key("left")),
        "refer to [<mutability>]":
            R(Text("&%(mutability)s")),
        "lifetime":
            R(Text("'")),
        "static":
            R(Text("static ")),
        "struct": R(Text("struct ")),
        "as": R(Text("as ")),
        "implement": R(Text("impl ")),
        "self":
            R(Text("self")),
        "super": R(Text("super")),
        "brace pan":
            R(Key("escape, escape, end, left, enter, enter, up, tab")),
        "enum":
            R(Text("enum ")),
        "await":
            R(Text(".await")),
        "async":
            R(Text("async ")),
        "clone":
            R(Text(".clone()")),
        "name space|quad":
            R(Key("colon, colon")),
        "public|publish": R(Text("pub ")),
        "module": R(Text("mod ")),
        "crate": R(Text("crate")),

        # Data types
        "boolean": R(Text("bool")),
        "[<unsigned>] integer [<ibits>]": R(Text("%(unsigned)s%(ibits)s")),
        "float [<fbits>]": R(Text("f%(fbits)s")),
        "character": R(Text("char")),
        "type <type_name>": R(Text("%(type_name)s")),
    }

    extras = [
        Choice("ibits", {
            "eight": "8",
            "sixteen": "16",
            "thirty two": "32",
            "sixty four": "64",
            "one [hundred] twenty eight": "128",
            "arch|size": "size",
        }),
        Choice("fbits", {
            "thirty two": "32",
            "sixty four": "64",
        }),
        Choice("type_name", {
            "alias": "type ",
            "self": "Self",
            "string": "String",
            "vector": "Vec",
        }),
        Choice("unsigned", {"unsigned": "u"}),
        Choice("mutability", {"mute ah | mute": "mut "}),
        ShortIntegerRef("n", 0, 1000),
        alphabet_support.get_alphabet_choice("a"),
        alphabet_support.get_alphabet_choice("b"),
    ]
    defaults = {
        "fbits": "64",
        "ibits": "32",
        "unsigned": "i",
        "mutability": "",
        "a": "i",
        "b": "j",
        "n": 1
    }


def get_rule():
    return Rust, RuleDetails(ccrtype=CCRType.GLOBAL)
