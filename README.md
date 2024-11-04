headsplitter
============

> Split markdown files on ATX-style or SETEXT-style headers.

Status
------

Pre-Alpha: In-development.

Usage
-----

Given the a file named `my-markdown-file.md` that contains the following:

```markdown
Example Markdown File
=====================

Example A
---------

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus fringilla, leo
et blandit euismod, mauris lacus iaculis arcu, eget venenatis nisi lacus eget
massa. Aliquam at ultricies lectus.

Example B
---------

Sed sed finibus velit. Ut enim arcu, sagittis eget mollis a, dictum ut justo.
Vestibulum consectetur, elit non posuere finibus, nunc neque vehicula ante, et
pretium turpis nisi at nibh. Duis ac porta justo, sit amet luctus diam.

Example C
---------

Phasellus sit amet tristique ligula. Vestibulum sit amet nulla in purus feugiat
aliquam placerat ullamcorper erat. Aliquam interdum dui lorem, eu pellentesque
velit consectetur in. Aenean eleifend est ac justo cursus consequat. 
```

The command:

```bash
headsplit my-markdown-file.md
```

Will create three files:

`01-example-a.md`

```markdown
Example A
---------

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus fringilla, leo
et blandit euismod, mauris lacus iaculis arcu, eget venenatis nisi lacus eget
massa. Aliquam at ultricies lectus.
```

---

`02-example-b.md`

```markdown
Example B
---------

Sed sed finibus velit. Ut enim arcu, sagittis eget mollis a, dictum ut justo.
Vestibulum consectetur, elit non posuere finibus, nunc neque vehicula ante, et
pretium turpis nisi at nibh. Duis ac porta justo, sit amet luctus diam.
```

---

`03-example-c.md`

```markdown
Example C
---------

Phasellus sit amet tristique ligula. Vestibulum sit amet nulla in purus feugiat
aliquam placerat ullamcorper erat. Aliquam interdum dui lorem, eu pellentesque
velit consectetur in. Aenean eleifend est ac justo cursus consequat.
```

Alternatives
------------

* Python-based [mdsplit](https://github.com/markusstraub/mdsplit) -- A stable and fully featured alternative. Does not support SETEXT style headings.
* [python-mdsplit](https://github.com/prismv/python-mdsplit) -- A fork of the above. Does not support SETEXT style headings.
* C++ based tool [mdsplit](https://github.com/alandefreitas/mdsplit) -- Designed for splitting up `README.md` files on a github repo.
* Node-based [markdown-split](https://github.com/marceljs/markdown-split) -- A node library that produces JSON.
* Node-based [split-md](https://github.com/accraze/split-md) -- Uses patterns like `'### v'` to split up a file. 
* Python-based [mdsaw](https://gitlab.com/hydrargyrum/mdsaw) -- splits on multiple ATX-style `H1` headers in a single file.
* [Split File](https://www.markdowntoolbox.com/tools/split-file/) -- a web-based tool where you can upload or paste markdown then download the resulting files.
* Node-based [markdown-splitter](https://github.com/romainbou/markdown-splitter) -- splits markdown files on annotations in comments.
* Python-based [split_markdown4gpt](https://github.com/twardoch/split-markdown4gpt?tab=readme-ov-file) -- splits files based on size (via markdown token limit) and a delimiter.

There are also various ways to do this on the command line using more
general-purpose tools that you may already have installed if your needs are
simple.

* GNU Coreutils [gcsplit](https://christiantietze.de/posts/2019/12/markdown-split-by-chapter/).

  ```bash
  gcsplit --prefix="NAME-" --suffix-format='%03d.md' FILENAME.md '/##/' "{*}"
  ```
* Linux-based [csplit](https://www.reddit.com/r/Markdown/comments/8sjeui/splitting_markdown_files/) (I haven't tried this one.)
  ```bash
  csplit FILENAME.md /#/ {*}
  ```
  [gawk/awk](https://github.com/dxcore35/obs-md-header-spliter)
  I wrote a bash script using `sed`, but it's complicated and unreliable.
