# Stack Overflow Snippets

One day I came across this reddit post: [How to Program (in four easy steps)](https://www.reddit.com/r/ProgrammerHumor/comments/2xmhh7/how_to_program_in_four_easy_steps/).

That four steps looked a bit complicated... I thought that programming should be easier, so created this:

![Demo](http://i.imgur.com/4bRsv29.gif)

## How to Use It?

**Shift + Ctrl + H**

or Tools > Stack Overflow Snippets

or Command Palette > Stack Overflow Snippets.

## Tips & Tricks

* Programming language is automatically determined by the file syntax, so you don't need to add it to each query.

## Can't Find a Snippet?

In some cases Google can find better results (you know, artificial intelligence and everything), so you may want to try the old school approach in case the plugin didn't return any results.

## What's That Quota Thing?

The plugin uses Stack Exchange API which is limited to 300 queries per day per IP.

Typically one snippet search makes two API queries: one to get questions that match the search query and another to get answers for the selected question.

The plugin caches API responses, so if you search for the same query or select the same question multiple times no additional requests are made.

The remaining quota is displayed in the status bar after each request is sent to the API.
