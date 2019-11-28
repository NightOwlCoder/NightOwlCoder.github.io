---
layout: post
title:  "XAML Formatting on VS Mac"
date:   2019-11-23 22:52:25 -0800
categories: xaml vsmac 
---
Please follow this to make sure your VS Mac formats the code correctly.

# PlugIn install

## Repository

Install the repository into VS Mac, using these url: http://addins.monodevelop.com/Stable/Mac/8.2.6/
To do that, follow these steps:

### Open Extensions

![step1.png](../assets/step1.png){:width="300px"}

### Select Gallery, Repositories, Manage Repositories

![step2.png](../assets/step2.png){:width="400px"}

### Press Add, paste the URL given above:

![step3.png](../assets/step3.png){:width="400px"}

### Make sure the new repository site is selected

![step4.png](../assets/step4.png){:width="400px"}

## Plugin

### Now search for `Xaml Styler` and install it

![step6.png](../assets/step6.png){:width="400px"}


# PlugIn config

add this file [Settings.XamlStyler](https://www.dropbox.com/s/rghwjhtccuv5tnu/Settings.XamlStyler?dl=1) to you `SLN` root.


\*  until they fix this [bug](https://github.com/Xavalon/XamlStyler/issues/196), we have to live with this, later we can add only one file to root folder of all projects

# PlugIn run

configure key binding of `Cmd-Shit-\` to be your key combination, like so:

![pref1.png](../assets/pref1.png){:width="400px"}


Unfortunately also because of another [bug](https://github.com/Xavalon/XamlStyler/issues/161) we can't configure to run on save for now.



<br>
<br>
<br>

See `.Sergio` is you have issues or doubts, about above info only. :)


You’ll find this post in your `_posts` directory. Go ahead and edit it and re-build the site to see your changes. You can rebuild the site in many different ways, but the most common way is to run `jekyll serve`, which launches a web server and auto-regenerates your site when a file is updated.

Jekyll requires blog post files to be named according to the following format:

`YEAR-MONTH-DAY-title.MARKUP`

Where `YEAR` is a four-digit number, `MONTH` and `DAY` are both two-digit numbers, and `MARKUP` is the file extension representing the format used in the file. After that, include the necessary front matter. Take a look at the source for this post to get an idea about how it works.

Jekyll also offers powerful support for code snippets:

{% highlight ruby %}
def print_hi(name)
  puts "Hi, #{name}"
end
print_hi('Tom')
#=> prints 'Hi, Tom' to STDOUT.
{% endhighlight %}

Check out the [Jekyll docs][jekyll-docs] for more info on how to get the most out of Jekyll. File all bugs/feature requests at [Jekyll’s GitHub repo][jekyll-gh]. If you have questions, you can ask them on [Jekyll Talk][jekyll-talk].

[jekyll-docs]: https://jekyllrb.com/docs/home
[jekyll-gh]:   https://github.com/jekyll/jekyll
[jekyll-talk]: https://talk.jekyllrb.com/
