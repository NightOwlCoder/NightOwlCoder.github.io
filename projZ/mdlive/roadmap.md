---
layout: page
title: MDLive Alert App Roadmap
---

# MDLive Alert App Roadmap

## 1 Prime Channels

Expose the trades done on the private channels, off course for additional \$\$\$.

![](2020-08-17-12-49-34.png){:width="250px"}

Each `private channel` owner would need to use the app to submit his trades, with a page to select `ticker`, type (EOD, Swing, Options, etc.), strike and expiration (if options) and values (entry, equity price, etc).
Once a trade is on, it could be selected to be closed, rolled, or "add more".
This was it would be easier on our users to "follow" some trades.

## 2 Integration with Brokers

Brokers like TD-Ameritrade and E-Trade offer an API access, that could be used to submit trades.

It is a connection that needs to be configured by the end user, so we are protected under a "you are the one that connected the app" kind of clause.

The auto-thingy could submit the trades on user's behalf, with some parameters that he could set, like `max of 5% of account value`, `no more that 5 options`, `expiration at least 4 weeks ahead`, etc.

Off course this would need to be tested/validated for a long time, but the whole system is not something hard to create.

## 3 New alerts when app on BG

Android/iOS allows for a background task to fetch some info every 15 minutes.

The plan is to hit the alerts endpoint to see if there are any new alerts. If there is, send a local push notification to alert the user.

The check for new alerts would happen only during market open times.

The user can tap on the alert and open the app, what would cause a refresh.
