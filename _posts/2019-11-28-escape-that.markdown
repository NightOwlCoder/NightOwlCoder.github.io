---
layout: post
title:  "Jekyll and how to escape those fence codes"
date:   2019-11-28 22:32:11 -0800
categories: jekyll markdown highlighting escape
---
Jekyll has a great support for syntax highlighting, but what if you want to escape the fence codes itself?

Meet `{% raw %}{% raw %}{% endraw %}`.

With `raw`, you can escape any Jekyll command, so to print the `raw` command above, I surrounded it with `raw ` and `endraw`.

Unfortunately I can't do it here, but you get the gist?<script src="https://gist.github.com/NightOwlCoder/06e1bbd723852760012048ea6657d8b2.js"></script>

To output the highlight fence, I surrounded it with above and we get:

`{% raw %}{% highlight ruby %}{% endraw %}`

Check out the [Jekyll docs<sup style="font-size: 20px;">⇗</sup>][jekyll-docs]{:target="_blank"} for more info on how to get the most out of Jekyll. File all bugs/feature requests at [Jekyll’s GitHub repo<sup style="font-size: 20px;">⇗</sup>][jekyll-gh]{:target="_blank"}.

[jekyll-docs]: https://jekyllrb.com/docs/home
[jekyll-gh]:   https://github.com/jekyll/jekyll