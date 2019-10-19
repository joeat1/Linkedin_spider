# Linkedin_spider
> some scripts for Linkedin
## basic information
+ LinkedIn platform users are divided into ordinary users and members, each user can publish dynamics, add contacts, view company and other users' file information; can set personal dynamics and friends are announced, in general, LinkedIn Member information cannot be viewed by ordinary non-friend users unless the individual is specifically set to be public on the whole network.
+ Expand your professional social circle and upgrade to a member to view more member information.
+ There is no strict job verification on Linkedin for falsified user identities; although users can report each other, most users are registered based on the purpose of job search, and are relatively willing to accept requests from friends who have fake jobs.
+ If the average friend reaches 30 or more, the platform will increase the user's exposure. If the set company is more attractive, some new users may choose to actively add as friends.

## Personal information characteristics
+ The basic information of each user includes: name, education experience, employment experience, etc. The description of the individual is very detailed;
+ The URL of the profile page is generally `https://www.linkedin.com/in/{username}`;
+ Personal dynamic URL is generally `https://www.linkedin.com/in/{username}/detail/recent-activity/` Some users are not visible or not; `detail/recent-activity/posts/ `For the article `detail/recent-activity/shares/` for sharing;
+ Personal contact URL is generally `https://www.linkedin.com/in/{username}/detail/contact-info/`;
+ Company URL of personal concern `https://www.linkedin.com/in/{username}/detail/interests/companies/`;
+ Most users have less personal activity, don’t update for a long time, or have a small amount of praise or comments

### Crawling protective measures ###

+ The LinkedIn platform page is rendered by Ajax. The URL of the page is accessed one by one, and the information is displayed on the browser. This makes the way of requesting the webpage of the PC to directly obtain valid and valid information.

+ When logging in from a different location, it is often necessary to perform an abnormal login verification of the mailbox, and some areas require mobile phone number verification;

+ The platform uses `https://www.linkedin.com/realtime/connect` to know if it is connecting in real time;
+ Use the `https://www.linkedin.com/li/track` link to record platform operations;
   ```eventInfo: {topicName: "BadgeInteractionActionEvent", eventName: "BadgeInteractionActionEvent",...},...}```
+ The platform uses https://www.linkedin.com/voyager/api/feed/badge?queryAfterTime=1551070345762&countFrom=0 to get the query query time and number of times

+ Each user has a certain amount of search ability every month, if the search result is empty, and the warning content is displayed;
+ Each user browses a large number of user information homepages for a period of time, etc., more than about 125 users, if the speed is too fast, the number will be directly sealed, if the speed is slow, it will be forced to exit, and use automatic warning or request to re-login and Pass the Google verification module.

### moblie phone ###
+ `https://www.linkedin.com/voyager/api/identity/profiles/XXXX/privacySettings`
+ `https://www.linkedin.com/voyager/api/identity/profiles/XXXXX/networkinfo`
+ `https://www.linkedin.com/voyager/api/identity/profiles/XXXXXX/profileContactInfo`
+ `https://www.linkedin.com/voyager/api/growth/normInvitations`
