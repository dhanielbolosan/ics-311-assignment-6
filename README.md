# ics-311-assignment-6

## General Background
Data from a social media network will be provided as a list of users. Each user will have a directional list of connections to other users. These connections have different categories such as  “follows”, “friends”, “co-worker”, “blocked”, and “has read posts by”. You can use any format you want for this data.

Each user also has a list of posts - content they’ve directly posted to the network. Posts in turn have a list of comments added to them. Comments have a user that created them, and users also have a list of comments. Posts also have a list of users that have seen them (a list that is necessarily longer than the list of comments) and users have a list of posts they’ve seen, i.e., views of that post. Posts and comments all have content (a string), and a creation time and date. Views of a post also have a time and date of the view. Again, you may format this data in any manner you wish.

In other words, users have four lists: connections, posts they’ve authored, posts they’ve read, and comments. For simplicity, posts and comments are simple text strings and do not include images, video, or other media.

Users can also have a list of attributes, such as user name, real name, age, gender, nicknames, workplace, location, and more. But each social media network has a different set of attributes. For simplicity, you can assume that networks that have attributes in common are consistent about how they use those attributes. All social network users have a “user name” attribute, and they are consistent across networks. In other words, a user’s user name is the same (and unique) on all social networks and you may use this attribute to identify a user uniquely. This is a simplifying assumption that definitely does not apply in the real world.

## Question 4
Produce a report of trending posts, i.e., ones gaining more attention at the greatest rate. An analyst must be able to characterize which posts are included in the word cloud by using only a subset of the social media data. An analyst must simultaneously be able to restrict which posts are used in the report by providing key words to either eliminate or include posts, e.g. an analyst may want to see a word cloud of all posts containing a specific profanity. Finally, an analyst must simultaneously be able to restrict the word cloud to posts by users with specific attributes (such as age, gender, or geographical region).
