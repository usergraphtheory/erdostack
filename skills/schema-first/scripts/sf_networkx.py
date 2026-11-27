"""Snapshot of an in-process graph (NetworkX-style), read from the graph object itself.

This module imports nothing outside the standard library. It is handed the graph that the repository's own
loader builds (or, for a bare file, the graph NetworkX reads from it) and only calls is_directed(),
is_multigraph(), nodes(data=True) and edges(data=True).
"""
from __future__ import annotations

import importlib
import json
import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

from sf_format import SEP, digest, fmt_value, today
from sf_profile import describe, type_name

NODE_KIND_NAMES = ["kind", "type", "label", "labels", "node_type", "ntype", "category", "class", "entity", "entity_type"]
EDGE_KIND_NAMES = ["rel", "kind", "type", "label", "relation", "relationship", "rel_type", "edge_type", "etype", "predicate"]
ONE_NODE_KIND, ONE_EDGE_KIND = "node", "edge"


def load(spec: str | None, file: str | None):
    """Return (graph, description of where it came from, [files the result depends on])."""
    sys.path.insert(0, os.getcwd())
    if spec:
        module_name, _, func = spec.partition(":")
        module = importlib.import_module(module_name)
        graph = getattr(module, func)() if func else module
        deps = [getattr(module, "__file__", "") or ""]
        return graph, f"{spec}()", [d for d in deps if d]
    import networkx as nx  # only for a bare file with no loader in the repository
    path = Path(file)
    suffix = path.suffix.lower()
    if suffix == ".graphml":
        graph = nx.read_graphml(path)
    elif suffix == ".gml":
        graph = nx.read_gml(path)
    elif suffix == ".gexf":
        graph = nx.read_gexf(path)
    elif suffix == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        key = "edges" if "edges" in data else "links"
        try:
            graph = nx.node_link_graph(data, edges=key)
        except TypeError:  # NetworkX before 3.4 has no `edges` argument
            graph = nx.node_link_graph(data)
    else:
        raise SystemExit(f"{file}: no reader for '{suffix}' here. Use the repository's loader with --load module:function.")
    return graph, f"file {file}", [str(path)]


def detect(items: list[dict], names: list[str], ends: list[tuple] | None = None) -> tuple[str | None, str]:
    """The attribute that names the kind, and why it was chosen.

    First a conventional name (kind, type, label, rel ...) that is on nearly every item with repeating text
    values. Failing that, the attribute whose value best predicts an item's shape: which other attributes it
    carries and, for edges, which kinds of node it joins. A category that predicts nothing is not a kind."""
    if not items:
        return None, ""

    def usable(name: str) -> list | None:
        values = [attrs.get(name) for attrs in items if name in attrs]
        if len(values) >= 0.9 * len(items) and all(isinstance(v, str) for v in values):
            return values
        return None

    for name in names:
        values = usable(name)
        if values and (len(set(values)) < len(values) or len(values) == 1):
            return name, "conventional name"

    def purity(name: str | None) -> float:
        groups: dict = defaultdict(Counter)
        for n, attrs in enumerate(items):
            shape = (frozenset(k for k in attrs if k != name), ends[n] if ends else None)
            groups[attrs.get(name) if name else None][shape] += 1
        return sum(max(c.values()) for c in groups.values()) / len(items)

    base, best = purity(None), None
    for name in sorted({k for attrs in items for k in attrs}, key=str):
        values = usable(name)
        if not values or not 2 <= len(set(values)) <= min(60, len(values) // 2):
            continue
        score = purity(name)
        if score >= 0.9 and score - base >= 0.2 and (best is None or (score, -len(set(values))) > (best[0], -best[2])):
            best = (score, name, len(set(values)))
    if best:
        return best[1], "detected: its value predicts which attributes an item has" + (" and which kinds it joins" if ends else "")
    return None, ""


def hashable(value):
    try:
        hash(value)
        return value
    except TypeError:
        return repr(value)


def attribute_lines(items: list[dict], skip: set[str], samples: bool) -> list[str]:
    total = len(items)
    names: dict[str, list] = defaultdict(list)
    for attrs in items:
        for name, value in attrs.items():
            if name not in skip:
                names[str(name)].append(value)
    lines = []
    for name, values in names.items():
        present = [v for v in values if v is not None]
        types = Counter(type_name(v) for v in present)
        kind = "/".join(t for t, _n in types.most_common()) or "null"
        parts = [f"- `{name}` {kind}"]
        if len(values) < total:
            parts.append(f"on {len(values)} of {total} only: handle the ones without it (absent is not zero)")
        if len(present) < len(values):
            parts.append(f"None in {len(values) - len(present)}")
        counts = Counter(hashable(v) for v in present)
        distinct = len(counts)
        scalar = all(isinstance(v, (str, int, float, bool)) for v in present)
        numeric = present and all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in present)
        if samples and present:
            if distinct <= 8 and (len(present) >= 2 * distinct or distinct <= 3):
                parts.append("values: " + ", ".join(f"{fmt_value(v)} ({n})" for v, n in counts.most_common()))
            elif numeric:
                parts.append(f"{distinct} distinct" + SEP + f"{fmt_value(min(present))} to {fmt_value(max(present))}")
            else:
                parts.append(f"{distinct} distinct" + SEP + "e.g. " + ", ".join(fmt_value(v) for v in list(counts)[:3]))
        elif present:
            parts.append(f"{distinct} distinct")
        if scalar:
            found = describe(list(counts)[:400])
            parts += found if samples else [re.sub(r" \(\d{4}-\d{2}-\d{2} to [^)]*\)", "", note) for note in found]
        lines.append(SEP.join(parts))
    return lines


def take(graph, origin: str, inputs: str, node_kind: str | None = None, edge_kind: str | None = None,
         samples: bool = True) -> tuple[dict, list[str], list[str]]:
    directed, multi = bool(graph.is_directed()), bool(graph.is_multigraph())
    nodes = [(n, dict(attrs)) for n, attrs in graph.nodes(data=True)]
    if multi:
        edges = [(u, v, dict(attrs), key) for u, v, key, attrs in graph.edges(keys=True, data=True)]
    else:
        edges = [(u, v, dict(attrs), None) for u, v, attrs in graph.edges(data=True)]
    why_node = why_edge = "given on the command line"
    if node_kind in (None, "auto"):
        node_kind, why_node = detect([a for _n, a in nodes], NODE_KIND_NAMES)
    node_kind = None if node_kind == "none" else node_kind
    lookup = {n: (str(a.get(node_kind)) if node_kind else "") for n, a in nodes}
    if edge_kind in (None, "auto"):
        edge_kind, why_edge = detect([a for _u, _v, a, _k in edges], EDGE_KIND_NAMES,
                                     [(lookup.get(u), lookup.get(v)) for u, v, _a, _k in edges])
    edge_kind = None if edge_kind == "none" else edge_kind
    edge_kind_from_key = False
    if edge_kind is None and multi and edges and all(isinstance(k, str) for *_x, k in edges) \
            and len({k for *_x, k in edges}) < len(edges):
        edge_kind_from_key = True

    def nk(attrs: dict) -> str:
        return str(attrs.get(node_kind, "(no " + node_kind + ")")) if node_kind else ONE_NODE_KIND

    def ek(attrs: dict, key) -> str:
        if edge_kind_from_key:
            return str(key)
        return str(attrs.get(edge_kind, "(no " + edge_kind + ")")) if edge_kind else ONE_EDGE_KIND

    kind_of_node = {n: nk(attrs) for n, attrs in nodes}
    by_node_kind: dict[str, list] = defaultdict(list)
    for n, attrs in nodes:
        by_node_kind[kind_of_node[n]].append((n, attrs))
    by_edge_kind: dict[str, list] = defaultdict(list)
    for u, v, attrs, key in edges:
        by_edge_kind[ek(attrs, key)].append((u, v, attrs))

    index, node_body, rel_body, review, shape, same_kind = [], [], [], [], [], []
    display: dict = {}   # a readable name per node, where its kind has an attribute that is text and unique
    for kind, members in by_node_kind.items():
        for name in list(members[0][1]) if members else []:
            values = [a.get(name) for _n, a in members]
            if name != node_kind and all(isinstance(v, str) for v in values) and len(set(values)) == len(values):
                display.update({n: a[name] for n, a in members})
                break
    for kind in sorted(by_node_kind):
        members = by_node_kind[kind]
        lines = attribute_lines([a for _n, a in members], {node_kind} if node_kind else set(), samples)
        names = [l.split("`")[1] for l in lines]
        ids = [n for n, _a in members]
        id_types = "/".join(sorted({type_name(n) for n in ids}))
        index.append(f"- {kind} ({len(members)} nodes): {', '.join(names) or 'no attributes'}")
        node_body.append(f"### {kind}")
        node_body.append(f"count: {len(members)}{SEP}node id: {id_types}" + (f", e.g. {', '.join(fmt_value(n) for n in ids[:2])}" if samples else ""))
        node_body += lines + [""]
        shape.append(f"N {kind} " + " ".join(sorted(f"{l.split('`')[1]}:{l.split('`')[2].split()[0]}" for l in lines)))
    for kind in sorted(by_edge_kind):
        members = by_edge_kind[kind]
        patterns = Counter()
        for u, v, _a in members:
            a, b = kind_of_node.get(u, "?"), kind_of_node.get(v, "?")
            patterns[(a, b) if directed else tuple(sorted((a, b)))] += 1
        arrow = "->" if directed else "-"
        lines = attribute_lines([a for _u, _v, a in members], {edge_kind} if edge_kind else set(), samples)
        names = [l.split("`")[1] for l in lines]
        rel_body.append(f"### {kind}")
        for (a, b), n in sorted(patterns.items(), key=lambda item: -item[1]):
            example = ""
            if a == b and directed:
                linked = {(u, v) for u, v, _a in members if u != v}
                mostly_twins = 2 * sum(1 for u, v in linked if (v, u) in linked) >= len(linked)
                shown = [(u, v) for u, v, _a in members if kind_of_node.get(u) == a and kind_of_node.get(v) == b and u != v][:3]
                if shown and samples:
                    example = SEP + "stored source→target, e.g. " + ", ".join(
                        f"{fmt_value(display.get(u, u), 24)}→{fmt_value(display.get(v, v), 24)}" for u, v in shown)
                if not mostly_twins:
                    same_kind.append(f"{kind} (:{a})->(:{b}): the arrow is stored source→target; which end depends on, contains or "
                                     f"follows the other is not in the data.")
            rel_body.append(f"- pattern: (:{a})-[:{kind}]{arrow}(:{b}){SEP}{n} edges{example}")
            index.append(f"- (:{a})-[:{kind}]{arrow}(:{b}) ({n} edges)" + (f": {', '.join(names)}" if names else ""))
        if len(patterns) > 1:   # say which patterns carry an attribute that only some edges of this kind have
            for n, line in enumerate(lines):
                name = line.split("`")[1]
                having = Counter()
                for u, v, attrs in members:
                    if name in attrs:
                        a, b = kind_of_node.get(u, "?"), kind_of_node.get(v, "?")
                        having[(a, b) if directed else tuple(sorted((a, b)))] += 1
                if set(having) != set(patterns) and all(having[p] == patterns[p] for p in having):
                    where = ", ".join(f"(:{a})-[:{kind}]{arrow}(:{b})" for a, b in having)
                    head, _, rest = line.partition(SEP)
                    rest = rest.split(SEP, 1)[1] if rest.startswith("on ") and SEP in rest else rest
                    lines[n] = head + SEP + f"only on {where} edges" + (SEP + rest if rest else "")
        rel_body += lines
        pairs = Counter((u, v) for u, v, _a in members)
        parallel = sum(n - 1 for n in pairs.values() if n > 1)
        if parallel:
            rel_body.append(f"- parallel edges: {parallel} edges repeat a (source, target) pair that already has one: counting "
                            f"edges or degree is not counting distinct neighbours")
        if directed:
            twins = [(u, v) for (u, v) in pairs if u != v and (v, u) in pairs]
            if twins:
                first = {}
                for u, v, attrs in members:
                    first.setdefault((u, v), attrs)
                equal = [name for name in names
                         if all(first[(u, v)].get(name) == first[(v, u)].get(name) for u, v in twins)]
                one_way = len(pairs) - len(twins)
                rel_body.append(
                    f"- stored in both directions: {len(twins)} of {len(pairs)} linked pairs also have the opposite edge"
                    + (f", carrying the same {', '.join(equal)}" if equal else "")
                    + f"; {one_way} are one-way. A two-way link is two edges here: count or sum it once, and do not halve "
                      f"a total that includes one-way edges")
                review.append(f"{kind}: two-way links are stored as two edges ({len(twins) // 2} links) next to {one_way} one-way edges.")
        loops = sum(1 for u, v, _a in members if u == v)
        if loops:
            rel_body.append(f"- self-loops: {loops}")
        rel_body.append("")
        shape.append(f"E {kind} " + " ".join(f"{a}>{b}" for a, b in sorted(patterns)) + " | " +
                     " ".join(sorted(f"{l.split('`')[1]}:{l.split('`')[2].split()[0]}" for l in lines)))

    cls = type(graph).__name__
    version = getattr(sys.modules.get("networkx"), "__version__", "unknown")
    facts = {
        "taken": today(),
        "store": f"in-process graph built by {origin}",
        "source": "live store (the graph as loaded today)",
        "refresh": f"schema.py networkx {inputs}",
        "method": "schema.py networkx (walks nodes(data=True) and edges(data=True) of the loaded graph)",
        "read_with": f"networkx {version}",
        "graph_class": f"{cls}: {'directed' if directed else 'undirected'}, parallel edges {'possible' if multi else 'not possible'}",
        "node_kind_attribute": node_kind or f"none found: every node is listed as kind `{ONE_NODE_KIND}`",
        "edge_kind_attribute": ("the edge key" if edge_kind_from_key else edge_kind) or f"none found: every edge is listed as kind `{ONE_EDGE_KIND}`",
        "kinds_chosen_by": f"nodes: {why_node or 'no attribute qualifies'}; edges: {why_edge or 'no attribute qualifies'} (override with --node-kind / --edge-kind)",
        "coverage": f"complete: {len(nodes)} nodes in {len(by_node_kind)} kinds, {len(edges)} edges in {len(by_edge_kind)} kinds",
        "fingerprint": digest(cls, str(node_kind), str(edge_kind), *sorted(shape)),
    }
    graph_attrs = getattr(graph, "graph", None)
    if isinstance(graph_attrs, dict) and graph_attrs:
        facts["graph_attributes"] = ", ".join(f"{k}={fmt_value(v)}" for k, v in list(graph_attrs.items())[:8])
    review += same_kind
    body = ["## Index", "",
            "One line per node kind (attributes) and per relationship pattern as stored (source kind, edge kind, target kind).", ""]
    body += index + ["", "## Nodes", ""] + node_body + ["## Relationships", ""] + rel_body
    return facts, body, review
