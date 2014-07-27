Title: Hello, World!
Date: 2014-07-26 16:04
Category: codings
Tags: python, pelican


I decided to create a blog. It was built with the Python Pelican static site
generator and is hosted by Github Pages. *Nice!*

For the interested, the project is [available on Github][1]. The general
process was:

* Install dependencies into a virtualenv:
```shell
mkvirtualenv --no-site-packages blog
pip install fabric markdown ghp-import pelican typogrify
```
* Create project shell:
```shell
pelican-quickstart
```
* Update a few settings in `pelicanconf.py` and `publishconf.py`.
* Create a theme. I based this off [SoMA2][2].
* `make github`

There are many tutorials on this process around the interwebs, but I am amazed
at the clean design and ease of use that Pelican provides. I highly recommend
it!

[1]: https://github.com/danielnaab/danielnaab.github.io-code
[2]: https://github.com/getpelican/pelican-themes/tree/master/SoMA2
