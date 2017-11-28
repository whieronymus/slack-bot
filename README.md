## Contents:
1. Setup Instructions
2. Bots
3. Adding new commands
4. ToDo

### Setup Instructions
ToDo -- Add Setup Instructions


### Bots
#### Tutorial Starter Bot
This contains the untouched code from the Tutorial I followed here:
https://www.fullstackpython.com/blog/build-first-slack-bot-python.html

#### Zora
Zora will become the ClubPython official bot. She will have all sorts of great commands.
Some just for fun, and others to help organize and administer our community.

If you'd like to get involved just DM me @kill.will on the Slack Channel and I'll you
some ideas to get started!

#### RookieBot
Zora's development took off a little faster than I had anticipated. Her structure and setup
is a bit more advanced and I'm afraid it will scare off newbies from thinking they have the
skills to contribute.

And thus... RookieBot was born!

RookieBot's development will use fairly simple and fairly basic techniques, that will be
easier for beginners to follow. So if you're new but still want to practice/contribute
RookieBot is there for you! RookieBot will always be there for you.



##### Adding new commands
Create a new function before `class Command`.
The function should take in one argument, that is whole message that user sends (except the bot tag).
It should return one value, that is text to be sent back.
Then add a new line in `define_commands()`.

Content should be:
```python
Command(func,  # function that you defined earlier, without parenthesis
        "name",  # what shall the user enter to call that function
        "help text")  # what shall be displayed when help command is called
```

### ToDo

#### Store User Information (OS, TextEditor, PyVersion, Interests, Projects, etc)
- Add a Database to Store information
- Create Schema for User Info
- Add a Class to Connect to and Query the Database
- Add Commands to Add User Info
- Add Commands to Get User Info

#### Schedule/Queue Mentoring Sessions, Livestreams, Code Reviews
- Create Schema for Calander**
- Create Schema for Mentoring Sessions, LiveStreams and CodeReviews
- Add Command to View Schedule
- Add Command to Schedule Session/CodeReview
- Add Command to Assign Code Reviews
- Add Command (and decide workflow) for pulling a Code Review, performing it and providing feedback

#### Commands for retrieving helpful stuff
- Add Command to List all of Zora's commands
- Add Command to get info about a Specific command (what it does, acceptable inputs, command format, etc)
- Add Commands for pulling cheatsheets (Like starting a new project, pushing to github, etc)

#### Funny and Misc Commands
- Commands for Pictures/GIFs
- Add your own ideas!!
