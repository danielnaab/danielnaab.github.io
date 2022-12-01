Title: Creating a Landing Page With npm Scripts
Date: 2015-12-13 19:21
Category: codings
Tags: npm, gulp, grunt


I've been putting off creating a new landing page for my on-going project,
[soil.io](https://www.soil.io), and decided to finally take care of it this
afternoon. While the site is simply a lead generation tool, I wanted to take
the opportunity to set up the build process using `npm run` scripts rather than
a `gulp` or `grunt` workflow.

Considering that my standard collection of `gulp` tasks (which I've built up
over time) took a fair amount of trial and error to get right, the
`npm run TASK` workflow was much simpler to configure. I've encountered a few
problems, but I must say I much prefer its simplicity over sometimes opaque
gulp plugins.

Keith Cirkel has
[a great post](https://blog.keithcirkel.co.uk/how-to-use-npm-as-a-build-tool/)
on this topic that is a good read. I don't want to repeat the general ideas so
will avoid turning this into a tutorial post. However, I've published the
source code for my landing page project
[on Github](https://github.com/danielnaab/soilio-landing).
