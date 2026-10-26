"""Small content format used by every paper module.

A paper is a list of groups (Q.1, Q.2 ...); each group holds sub-questions.
Each sub-question holds an answer made of blocks (P, B, F, T, FIG, NUM ...).
"""
import re

PAPERS = {}          # paper id -> Paper (filled by papers/*.py)


# ---------- answer blocks ----------
def P(t):            return ("p", t)
def H(t):            return ("h", t)
def B(*items):       return ("b", list(items))
def N(*items):       return ("n", list(items))
def F(*lines):       return ("f", list(lines))
def T(head, rows, widths=None, caption=None):
    return ("t", head, rows, widths, caption)
def FIG(name, caption=None, **kw):
    return ("fig", name, caption, kw)
def NUM(cid):        return ("num", cid)
def NOTE(t):         return ("note", t)
def MS(*pairs):      return ("ms", [(a, b) for a, b in pairs])


def mk(s):
    """Light markup: x_{2} -> subscript, x^{2} -> superscript, newline -> <br/>."""
    s = re.sub(r"&(?!(amp|lt|gt|#\d+);)", "&amp;", s)
    s = re.sub(r"_\{([^}]*)\}", r"<sub>\1</sub>", s)
    s = re.sub(r"\^\{([^}]*)\}", r"<super>\1</super>", s)
    return s.replace("\n", "<br/>")


class Question:
    def __init__(self, paper, group, sub, text, concept, chapter, ans, qtype,
                 flag, marks, src_page):
        self.paper, self.group, self.sub = paper, group, sub
        self.text, self.concept, self.chapter = text, concept, chapter
        self.ans, self.qtype, self.flag = ans, qtype, flag
        self.marks, self.src_page = marks, src_page

    @property
    def label(self):
        return f"{self.group['no']}({self.sub})" if self.sub else f"{self.group['no']}"

    @property
    def id(self):
        return f"{self.paper.pid}-Q{self.group['no']}{self.sub or ''}"

    def marks_split_total(self):
        return sum(m for b in self.ans if b[0] == "ms" for _, m in b[1])


class Paper:
    def __init__(self, pid, subj_code, subj_name, subj_short, sess_code, sess_label,
                 scheme, hours, total, printed_id, src_file, pages, in_scope=True,
                 notes=None):
        self.pid, self.subj_code, self.subj_name = pid, subj_code, subj_name
        self.subj_short, self.sess_code, self.sess_label = subj_short, sess_code, sess_label
        self.scheme, self.hours, self.total = scheme, hours, total
        self.printed_id, self.src_file, self.pages = printed_id, src_file, pages
        self.in_scope, self.notes = in_scope, notes or []
        self.groups = []
        PAPERS[pid] = self

    def group(self, no, text, marks, attempt=None):
        g = dict(no=str(no), text=text, marks=marks, attempt=attempt, qs=[])
        self.groups.append(g)
        self._g = g
        return g

    def q(self, sub, text, concept, chapter, ans, qtype="theory", flag=None,
          marks=None, src_page=1):
        g = self._g
        if marks is None:
            marks = g["marks"] // (g["attempt"] or 1) if g["attempt"] else g["marks"]
        qq = Question(self, g, sub, text, concept, chapter, ans, qtype, flag, marks, src_page)
        g["qs"].append(qq)
        return qq

    @property
    def questions(self):
        return [q for g in self.groups for q in g["qs"]]
