Title: A Static Site Generator With Gulp, Prose.io, and Travis CI
Date: 2014-11-06 18:45
Category: codings
Tags: static-site, gulp, prose.io, travis-ci, browserify, sass, swig


As I mentioned in my [introductory post](|filename|django-project-blueprints.md),
this is a static site generated with [Pelican](http://blog.getpelican.com/).
Now, for a new project for Lynn, a dog-trainer friend - who's been kind enough
to trade her dog-whispering services for design and web work - I wanted to
create another generated static site.

The benefits are manifest:

- Fast load times.
- Free hosting with Github Pages.
- A simple deployment stack that won't go down.

However, I need this site to be easy for Lynn to edit. She needs blog-like
features, but also needs to easily be able to add new testimonials from
customers, add new images, change her class schedule and service pricing,
update her contact information, etc. Editing a Github repository, rebuilding,
and pushing to the `gh-pages` branch is out of the question.

So how does one create a CMS-like experience for a generated static site?
[Prose.io](http://prose.io)! With [prose.io](http://prose.io), we can edit
Markdown files in a friendly web interface, auto-commit and push to Github.
Then, with a Travis-CI job, the site may be auto-rebuilt and pushed to Github
Pages. Even better, we can hide the non-content sections of the repository to
avoid confusion. Awesomeness! Read more about this strategy
[here](http://www.developmentseed.org/blog/2012/june/25/prose-a-content-editor-for-github/)
and [here](http://www.developmentseed.org/blog/2012/07/27/build-cms-free-websites/).
There are also [several sources](https://www.google.com/search?q=prose.io%20travis%20ci)
for ideas on using [Travis CI](http://travis-ci.org) with [prose.io](http://prose.io).

One more problem, though: all the framework-y static site generators are
heavily geared toward blogs... specifically, blogs for technies. It is painful
to bend a blog data model to an arbitrary content type, much less have many
different data models that are all organized and rendered differently.

This is where [gulp](http://gulpjs.com/) comes in. After some consideration, I
realized that gulp, which I have been enjoying using for client work and a
personal project, would be a perfect fit. It provides a simple way to do
processing on asset pipelines, which is exactly what a static site generator
does. In addition, unlike most generators out there, I would have total control
over the process and wouldn't feel like I was working with a
round-hole-square-peg blackbox. I could easily use
[SASS](http://sass-lang.com/), [npm](https://www.npmjs.org/) with
[Browserify](http://browserify.org/), whatever
[template language](http://paularmstrong.github.io/swig/) I want, etc.
Plus, I could organize the project structure in the most sensible manner for
this site and fully understand how the build process works.

Fortunately, I wasn't the only one who considered this possibility:
Sean Farrell [shared](http://www.rioki.org/2014/06/09/jekyll-to-gulp.html) his
experiences creating such a pipeline, and I was able to steal some of his
ideas. Specifically, the ideas Sean outlined that were useful to me were:

- Use [gulp-front-matter](https://www.npmjs.org/package/gulp-front-matter) to
parse YAML "front matter" from the content documents.
- His method of iterating over content documents and applying front-mater and
processing to each one.
- Also, I decided to follow his lead and use
[SWIG](http://paularmstrong.github.io/swig/) for HTML templating, which was a
pretty natural choice for me due to its similarity to Django and Jinga2.

Beyond that, I wanted my own organization and workflow:

- SASS for styling
- CommonJS modules with Browserify
- My preferred project layout
- Travis CI deployment
- Prose.io configuration

### Getting Started

If you want to follow along with the codebase, you may do so
[here](https://github.com/danielnaab/wunderdog/). The live site is
[here](http://blog.crushingpennies.com/wunderdog/) - be generous, the design
work is pending!

In the following sections, I'll skip over some details of the build process and
just focus on the big things that tie things together.

The project structure looks like this:

- assets/
    - scripts/
    - styles/
    - templates/
- content/
    - pages/
    - posts/
    - testimonials/
- _prose.yml
- gulpfile.js
- package.json
- travis.yml

### Compiling a Content Type: Testimonials

As you can see above, there are three content types in this project: pages,
posts, and testimonials. Pages are just one-off things, like an About or
Contact page. Posts correspond to blog posts, and every testimonial gets
rendered to one testimonials page. Let's take a look at how testimonials are
processed by our [`gulpfile.js`](https://github.com/danielnaab/wunderdog/blob/master/gulpfile.js). This code is largely borrowed from
[Sean Farrell](http://www.rioki.org/2014/06/09/jekyll-to-gulp.html), and the
same format is used for blog posts:

```
var frontMatter = require('gulp-front-matter'),
    marked = require('gulp-marked')

gulp.task('testimonials', function () {
    return gulp.src('content/testimonials/*.md')
        .pipe(frontMatter({property: 'page', remove: true}))
        .pipe(marked())
        // Collect all the testimonials and place them on the site object.
        .pipe((function () {
            var testimonials = []
            return through.obj(function (file, enc, cb) {
                testimonials.push(file.page)
                testimonials[testimonials.length - 1].content = file.contents.toString()
                this.push(file)
                cb()
            },
            function (cb) {
                testimonials.sort(function (a, b) {
                    if (a.author < b.author) {
                        return -1;
                    }
                    if (a.author > b.author) {
                        return 1;
                    }
                    return 0;
                })
                site.testimonials = testimonials
                cb()
            })
        })())
})
```

First, we iterate over all the testimonials, extract the front-matter, and
compile the Markdown to HTML. Next, we create an array of testimonials, sorted
by author name, and store it on the global `site` object.

Notice that we didn't output anything here - we just collected data that we can
render later. We will later pass
the `site` object into our templates. To see how we render them, have a gander
at the source for the
[testimonials page](https://github.com/danielnaab/wunderdog/blob/master/content/pages/testimonials.html).

Now let's take a look at how the
[`pages`](https://github.com/danielnaab/wunderdog/tree/master/content/pages)
are rendered:

```
var frontMatter = require('gulp-front-matter'),
    marked = require('gulp-marked'),
    merge = require('merge-stream')

gulp.task('pages', ['cleanpages', 'testimonials'], function () {
    var html = gulp.src(['content/pages/*.html'])
        .pipe(frontMatter({property: 'page', remove: true}))
        .pipe(through.obj(function (file, enc, cb) {
            var data = {
                site: site,
                page: {}
            }
            var tpl = swig.compileFile(file.path)
            file.contents = new Buffer(tpl(data), 'utf8')
            this.push(file)
            cb()
        }))

    var markdown = gulp.src('content/pages/*.md')
        .pipe(frontMatter({property: 'page', remove: true}))
        .pipe(marked())
        .pipe(applyTemplate('assets/templates/page.html'))
        .pipe(rename({extname: '.html'}))

    return merge(html, markdown)
        .pipe(gulpif(!DEBUG, htmlmin({
            // This option seems logical, but it breaks gulp-rev-all
            removeAttributeQuotes: false,

            removeComments: true,
            collapseWhitespace: true,
            removeRedundantAttributes: true,
            removeStyleLinkTypeAttributes: true,
            minifyJS: true,
            minifyCSS: true,
            minifyURLs: true
        })))
        .pipe(gulp.dest('dist'))
        .pipe(connect.reload())
})
```

Notice that we have two separate asset pipelines which are merged into one gulp
stream with the [merge-stream](https://www.npmjs.org/package/merge-stream)
module. Both pipelines, for HTML and Markdown, extract the front-matter from
each document. All Markdown documents use the `assets/templates/page.html`
template, but the HTML documents are expected to explicitly extend from a
template. The HTML is rendered using the `applyTemplate`, also borrowed from
Sean Farrell. Next, the use of `merge-stream` allows us to apply common
processing to both pipelines - specifically, HTML minification and output to
the `dist` directory.

We can then follow the same process for other asset pipelines. For instance, we
could populate a *services page* with a list of items with corresponding
prices, availability information, etc, all populated with front-matter data and
Markdown content. Who needs a database?

### Deployment

Skipping over the `dist` task that compiles the entire project, let's take a
look at the `deploy` task:

```
var deploy = require('gulp-gh-pages')

gulp.task('deploy', ['dist'], function () {
    return gulp.src('./dist/**/*')
        .pipe(deploy());
})
```

[`gulp-gp-pages`](https://www.npmjs.org/package/gulp-gh-pages) makes this
pretty simple; we can use the defaults, but the documentation allows us to
configure the git remote and origin, if necessary.

### Travis CI Configuration

Now that we have a deploy process, we want to automate it. We should be
pushing a built site every time a commit is pushed upstream. Here's the
`.travis.yml` that handles that for us:

```
branches:
  only:
  - master
language: node_js
node_js:
  - "0.10"
install:
  - npm install -g gulp
  - npm install
before_script:
  - git remote set-url origin "https://${GH_TOKEN}@github.com/danielnaab/wunderdog.git"
  - git config --global user.email "danielnaab@gmail.com"
  - git config --global user.name "Travis-CI"
script:
  - gulp deploy
env:
  global:
  - secure: "jTbRauX2+9E9WbSI6pu4oXO3P60d3KriWQr7sD39JArrXFqs3ZpeT0gdycmE4OlYS/t1MY7yzKFw2MPeyIO2tl5zIBRLx77GZRwqkKi0Y4Uu5nRNkOBiPsrVD7Iq5gLuknQGbLCHf2p+1MmtQbsuEVTSkV/FWzCxk2j0nRUm2ng="
```

Basically, we install our dependencies, set the origin with `https://` rather
than `git://` (because we're pushing), with an included Github auth token.
Then, we run the deploy task.

To set `GH_TOKEN`, we first need a Github auth token. Github
[provides instructions](https://help.github.com/articles/creating-an-access-token-for-command-line-use/)
for how to do that. Next, we need to encrypt the token so it's not committed as
plain text for the world to read; we can use the
[`travis` command line tool](https://rubygems.org/gems/travis) for that:

```shell
gem install travis
travis encrypt GH_TOKEN=<Github auth token>
```

This will output the `secure: XXXXX` line seen above. Add it to your
`.travis.yml`, and you're good to go! Commit, wait a few, and your site will
be updated.

### Prose.io Configuration

Now, onto [prose.io](https://rubygems.org/gems/travis). It's easy enough to
log in to the site, and at this point, we may make edits and things will
*just work*. Remember, though, we want the data-entry UI to be as easy as
possible and not include extraneous crud. We may use the
[`_prose.yml`](https://github.com/prose/prose/wiki/Prose-Configuration) to
defined the kind of interface prose.io should generate for us:

```
prose:
  rooturl: 'content'
  siteurl: 'http://blog.crushingpennies.com/wunderdog/'
  media: 'content/media'
  metadata:
    content/posts:
      - name: "published"
        field:
          element: "checkbox"
          label: "Published"
          help: "Uncheck to make this post hidden."
          value: true
          on: "true"
          off: "false"
      - name: "title"
        field:
          element: "text"
          label: "Title"
          help: "The blog post title"
          placeholder: "Enter title"
      - name: "date"
        field:
          element: "text"
          label: "Publication Date"
          help: "The publication date for this post."
          placeholder: "Enter date in the form YYYY-MM-DD"
      - name: "allowComments"
        field:
          element: "checkbox"
          label: "Allow Comments"
          help: "Allow users to comment with Disqus."
          value: true
          on: "true"
          off: "false"
    content/testimonials:
      - name: "published"
        field:
          element: "checkbox"
          label: "Published"
          help: "Uncheck to make this testimonial hidden."
          value: true
          on: "true"
          off: "false"
      - name: "author"
        field:
          element: "text"
          label: "Author"
          help: "The name of the author of this testimonial."
          placeholder: "Enter author name"
      - name: "authorLocation"
        field:
          element: "text"
          label: "Author Location"
          help: "The location of the author of this testimonial."
          placeholder: "Enter author location"
      - name: "authorUrl"
        field:
          element: "text"
          label: "Author URL"
          help: "A web URL for this author, if available."
          placeholder: "Enter author URL"
      - name: "signees"
        field:
          element: "hidden"
          label: "Signees/signatories"
          help: "If there is more than one author for this testimonial, enter them here."
```

### Summary

`gulp` + `prose.io` + `Travis CI` = awesome. I'm pretty pleased with the gulp
asset workflow, in particular, and intend to follow these patterns for a couple
more content types and hopefully streamline the process a bit.

As this project is finished out with a finalized design and interactivity with
Javascript, I'll update this post with any new ideas. Anyone else out there
using gulp for static site generation?
