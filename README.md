some2501
========

A blog system based on Django.

Write simple blog with simple steps.

1. write markdown file anywhere
2. put markdown file to `ARTICLE_ROOT/your_name/your_markdown.md`
3. wait for auto update (need systemd timer support)

Inspired by python package, `ARTICLE_ROOT/your_name/your_name.md`
will be your home page.

Thanks for python-markdown's meta information supporting,
we can pass some meta data to blog system.

| key |   meaning  |  default   |
|-----|------------|------------|
|title| article title | "████████████████████" |
|pub_time| article publish time | article file update time |
|mail | author's email address | None |
|nickname| author's nickname | None |
