# Captain’s Log

![Guaranteed to run on versions of Python 3](https://img.shields.io/badge/python-v3.x-blue)

For [NaNoGenMo 2016][1].

_Captain’s Log_ generates an arbitrary number of words of luckless captains and their endeavours in
the style of [Emily Short][2]’s superlative [Annals of the Parrigues][3].

To generate output you can type `python captains_log.py` in the command line and you will be
prompted to provide a wordcount. _Captain’s Log_ then does the following:

1. Picks a random captain and ship from curated lists.
2. Picks a random starting location from a collection of geo-tagged East India Company ports.
3. Searches through all the other locations for the nearest one and calculate the cardinal direction.
4. Sets sail!
    * occasionally encountering hostile OurShips
    * usually arriving at the specified destination
    * always ending with tragedy
5. Rinses, repeats.
6. Outputs it all to an HTML file.

You can see the latest output [here][4], but I don’t recommend you read through it in its entirety.
Instead, I’ve picked out some key pieces below:

![January, 1767 My name is Jacob Collaart, captain of the pinnace “San Nicolás”. We set sail from Bangka Island, heading northwest to Sulu. This is my log.][5]

![January, 1770 Able seaman Jones did his best, but his impersonation of a particularly attractive albatross did not succeed in luring a meal out of the skies.][6]

![February, 1768 We set sail from Tapian Nauli, heading north to Thanlyin. We arrived at Thanlyin after 2 days’ sailing. The people here are purposeful and thorough, recognised for their curious pickles.][7]

![April, 1770 We set sail from Tamsui, heading east to Keelung. We arrived at Keelung after 1 days’ sailing. The people here are tardy and heedless, famed for their imbecilic librarians.][8]

![December, 1768 I’m deeply concerned about the crew, some of them are coming to the end of multi-year hangovers in the beating midday sun and remembering they’re still on my ship. I worry they might unionise… We came across a threatening galleon with dozens of cannon, flying a Portuguese flag, seeming to fly towards us. We passed across their line and commenced a very severe action, with the result that the entire mizzen mast, the aft most of the ship’s three masts, is shot away along with all the standing & running rigging sails etc. Look at what I have done…][9]

![March, 1767 We set sail from Dhaka, heading southwest to Simon’s Bay. Thus ends the tale of the “San Nicolás” and her captain, Jacob Collaart – lost to either cannibalism or sobriety, pray we never discover which…][10]

I am grateful to [firesign24-7][11] for the use of her [Aged paper texture][12].

[1]: <https://github.com/NaNoGenMo/2016>
[2]: <https://emshort.blog/>
[3]: <https://drive.google.com/file/d/0B97d5C256qbrOHFwSUhsZE4tU0k/view?usp=sharing>
[4]: <https://github.com/eoinnoble/captains-log/blob/master/output/captains-log.html>
[5]: <https://github.com/eoinnoble/captains-log/blob/master/output/images/cl1.jpg>
[6]: <https://github.com/eoinnoble/captains-log/blob/master/output/images/cl2.jpg>
[7]: <(https://github.com/eoinnoble/captains-log/blob/master/output/images/cl3.jpg)>
[8]: <https://github.com/eoinnoble/captains-log/blob/master/output/images/cl4.jpg>
[9]: <https://github.com/eoinnoble/captains-log/blob/master/output/images/cl5.jpg>
[10]: <https://github.com/eoinnoble/captains-log/blob/master/output/images/cl6.jpg>
[11]: <http://firesign24-7.deviantart.com/>
[12]: <http://firesign24-7.deviantart.com/art/Aged-paper-texture-159950888>
