---
layout: post
title:  "Jekyll and syntax highlighting"
date:   2019-11-27 20:52:25 -0800
categories: jekyll githubpages markdown highlighting
---
Jekyll has a great support for syntax highlighting, by default, Jekyll utilizes [Rouge](http://rouge.jneen.net/), which is a pure ruby-based code highlighter. Rouge can highlight 100 different [languages](https://github.com/rouge-ruby/rouge/wiki/List-of-supported-languages-and-lexers). 

Code formatting can be done with `{% raw %}{% highlight ruby %}{% endraw %}`.

As you can see, you especify the language right there, even line numbers are supported by adding `linenos`, ending with something like like:

 ```
 {% raw %}{% highlight ruby linenos%}{% endraw %}
 ```
 
 A full run would be like:

{% highlight ruby linenos %}
def print_hi(name)
  puts "Hi, #{name}"
end
print_hi('Tom')
#=> prints 'Hi, Tom' to STDOUT.
{% endhighlight %}

Check out the [Jekyll docs][jekyll-docs] for more info on how to get the most out of Jekyll. File all bugs/feature requests at [Jekyll’s GitHub repo][jekyll-gh].

[jekyll-docs]: https://jekyllrb.com/docs/home
[jekyll-gh]:   https://github.com/jekyll/jekyll