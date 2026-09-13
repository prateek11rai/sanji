"""Keep maintenance notes out of the served HTML.

Comments in the markdown are instructions for whoever edits the page; they
are not content, and they otherwise ship to every reader in view-source.

`pymdownx.striphtml` is the obvious tool and the wrong one here: it strips
during markdown conversion, which eats the blog plugin's `<!-- more -->`
separator before the excerpt is taken, and every post then renders in full on
the index. Running at on_post_page instead means the blog plugin has already
had its separator.
"""

from __future__ import annotations

import re

_COMMENT = re.compile(r"<!--.*?-->", re.S)


def on_post_page(output, page, config):
    return _COMMENT.sub("", output)
