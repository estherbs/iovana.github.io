# iovana.github.io
This project's purpose is to perform sentiment analysis on Reddit posts (Reddimment - Reddit sentiment). Due to a high number of comments
one could find what is the general reaction of the users: positive or negative.

How to use:
Run python reddiment.py in the console.
Open up a browser and point it to the given IP address.
On the first page there's a field where a link to a reddit post can be inserted (e.g. https://www.reddit.com/r/science/comments/4pt3ed).
If the link is valid the page will direct the user to a second page which shows the top 10 most used positive vs negative words. There is
also a percentage at the top which is the percentage of negative words in the top 10 most found words. The colour of the background changes
according to the percentage of positive to negative words, if there's a high number of positive words the background will turn green, while
if there is a high percentage of negative words the background colour will turn red. 

This was developed as a project for an Advanced Python CodeFirst project. I will continue my work on the website as at the moment it lacks
some of the functionality I initially intended to add such as scraping all comments of a post (at the moment it doesn't scrape the
children of a comment or the hidden comments).

Note: unfortunately due to the reddit servers a link might sometimes work or the application will throw a "nonetype object is not subscriptable" error
or a 429 error (even if the url is valid). If this happens just stop the python script and restart it.
