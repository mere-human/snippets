# Twitter API Experiments

## user_tweets.py
* Gets user ID by name.
* Obtains tweets data of the user.
* Optionally, dumps tweets data JSON.
* Creates a HTML result page with all the obtained tweets.
* HTML result page can be printed to PDF for offline usage.

To create a bearer token, you need to register your project and app here:
https://developer.twitter.com/en/portal/projects-and-apps

There is also a workaround for bearer token: authorize and copy from playground:
https://oauth-playground.glitch.me/

## TODO
* Big video fit to page.
* Load media content on demand.
* Add start date argument.
* Make date human-friendly.
* Remove replies from result.

## Links

API Reference:
* https://developer.twitter.com/en/docs/twitter-api/tweets/timelines/api-reference/get-users-id-tweets
* https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/tweet

API playground:
* https://oauth-playground.glitch.me/
* https://developer.twitter.com/apitools/downloader

Code Examples:
* https://github.com/twitterdev/Twitter-API-v2-sample-code/blob/main/User-Lookup/get_users_with_user_context.py
* https://github.com/twitterdev/Twitter-API-v2-sample-code/blob/main/User-Tweet-Timeline/user_tweets.py

Print HTML to PDF:
* https://stackoverflow.com/questions/19249053/paginating-html-document-for-printing-with-webkit-based-browsers
* https://developer.mozilla.org/en-US/docs/Web/CSS/Media_Queries/Using_media_queries
* https://stackoverflow.com/questions/58084276/make-embedded-youtube-video-thumbnail-printable-media-print
