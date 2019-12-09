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

![step1.png](../assets/step1.png)

### Select Gallery, Repositories, Manage Repositories

![step2.png](../assets/step2.png)

### Press Add, paste the URL given above:

![step3.png](../assets/step3.png)

### Make sure the new repository site is selected

![step4.png](../assets/step4.png)

## Plugin

### Now search for `Xaml Styler` and install it

![step6.png](../assets/step6.png)


# PlugIn config

add this file [Settings.XamlStyler](https://www.dropbox.com/s/rghwjhtccuv5tnu/Settings.XamlStyler?dl=1) to you `SLN` root.


\*  until they fix this [bug](https://github.com/Xavalon/XamlStyler/issues/196), we have to live with this, later we can add only one file to root folder of all projects

# PlugIn run

configure key binding of `Cmd-Shit-\` to be your key combination, like so:

![pref1.png](../assets/pref1.png)


Unfortunately also because of another [bug](https://github.com/Xavalon/XamlStyler/issues/161) we can't configure to run on save for now.