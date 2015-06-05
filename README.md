# dekuuru
How to make a worse booru. And probably fail at it.

Create a board. Invite users. Add and comment on images. Make your own tags. Choose who to follow. Choose what you want to see - at work, and at home.

Search instructions (WIP):
- **item1** **item2** contains both
- **item1** **-item2** contains item1 but not item2
- **/board_tag/:tag** standard search item
- **tag** tag match, any board
- **/board_tag/** board match, any tag
- **,** as delim, merge querysets (?)

Django version 1.8.1
Using django-thumbs
::

	$ pip install django-thumbs

Dependencies:
::

	$ sudo apt-get install zlib1g-dev libjpeg-turbo8-dev libfreetype6-dev
	$ sudo pip install pillow
	
