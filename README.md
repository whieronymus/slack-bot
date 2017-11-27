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

Right now Zora is just using mostly the same code from the Starter bot, with a few added
basic commands, but we will be adding to this all the time. 

If you'd like to get involved just DM me @kill.will on the Slack Channel and I'll you 
some ideas to get started!

### Adding new commands
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
ToDo -- Add a list of Commands to implement 