# Data Visualization and D3.js

#### Project 5 - Udacity Nanodegree 
#### Fernando Hernandez

###**Summary**

This visualization follows the awarding of [Nobel Prizes] [nobel_org] from the first in 1901 to the most recent in 2015 in every field awarded.

It traces a path between the city of birth to current location when each Nobel Laureate was awarded the Nobel Prize showing migration over time.

It also shows the impact of World War II as a turning point in making the United States a world leader and destination spot for those who acquired Nobel Prizes.


[Current Visualization] [data_viz]
[Source code] [source_code]
[Current Nanodegree Projects] [projects]

###**Data**

Nobel data was scraped from [NobelPrize.org] [nobel_org] using [Python] [python]. 

Troublesome or erroneous records were validated using [Wikipedia] [wiki] and [New York Times] [NYTimes] articles.

Geo-coordinate data was queried using [Google Maps API] [maps_api]. 

*Source code:*
 [nobel.py] [nobel_py] 
 [wrangle.py] [wrangle.py]
 [latlon.py] [latlon.py]

###**Design** 

The initial idea was inspired by a data visualization featured on [Flowing Data] [1] entitled ['Cultural history via where notable people died'] [2], which visualized the births and deaths of  over 150,000 intellectuals over a 2000-year span.  

My goal was to visualize Nobel Laureates from birth to attainment, while making it interactive to explore. 

Design choices were influenced by on-going feedback. Particular examples are discussed in more detail in the feedback section, with links to the [Github] [3] commits containing the implementations. 

The initial visualization code is provided in the [initial index.html] [initial_commit] commit.

###**Feedback** 

Feedback has been graciously provided by fellow students and an instructor in the Udacity forums, as well as from former co-workers and personal friends.

Feedback sections are provided in chronological order, but the Feedback #1 commits are from various people in the beginning stages, and are in no particular order.

Github commit links for each section's changes based on feedback are provided in the footnotes.

#### **Feedback #1 Commits** [1][^1] [2][^2] [3][^3] [11][^11] [12][^12]

Various Initial Changes during initial first design/commits during on-going dialogue.
___
Footnotes #1, 2, 3:
> It would be cool to be able to filter by nobel fields to find people I know like Einstein and Mother Theresa.

Footnote #4:

> I'd like to be able to make the animation faster.

Footnote #5:

> Blue water for the earth might be a nice touch (smile)


__________

#### **Feedback #2 Commits** [4][^4]

Overall Changes Commit:
>Removed 'elastic' bounce on new entries, sped up transition on enters; Bar text spacing: Add spacing so it hovers a bit over each bar; Circle color/opacity: Change from 0.4 opacity to 0.8. Change Chemistry, Physiology, Economics colors to be more distinctly different from the land mass color.;

Based on the following feedback:

> The bar chart transition doesn't seem to be as smooth as it could be. This is more noticeable if you increase the seconds between years. It seems like a new chart is just placed over the old chart (I'm sure that's precisely what the code is doing), but maybe there is a way to make animation look a bit smoother.

- Bar transitions: I've removed the 'elastic' bounce on new entries.

*The code currently uses the enter/update/exit sequence in D3.js. It's calculating new counts each year, then entering any new bars, and exiting any old unneeded ones. If the count remains the same, it just transforms/moves the bar to new location or height (which I think looks kinda cool wink ). The tricky part is the 'same-country/place, new-count' bars. Those still have to exit old bars with old counts, and enter new ones with new data. I couldn't really find a good way to show that the country just changed its count. But I think you may be right, the bounce to show the same countries just added some new prizes that year seems a bit distracting.*

>This is a small nitpick, but I'll mention it anyway. I think the text above each bar would like slightly better if there was some additional vertical spacing between the bar and the text. Maybe just a few pixels. I'm referring to the text such as US - 366, GB - 111, etc.

- Bar text spacing: Added a few pixels so it hovers a bit over each bar.

*It does look better with a little space. Thanks!*

>Some of the yellows dots seem to kind of blend in with the map. Its kind of hard to distinguish the colors. To me they all seem like different shades of blue or yellow unless you look really carefully. Maybe you can try a different color pallet with brighter colors or ones that show more contrast. This might get trick as there many dots overlapping each other in Europe and America, so maybe someone else can suggest an alternative strategy.
Circle color/opacity: Changed from 0.4 opacity to 0.8. Changed Chemistry, Physiology, Economics colors to be more distinctly different from the land mass color.

*This one really helps see some patterns! I think I had lowered the opacity first to combat overplotting, before I had a jitter to the lon/lat coordinates. Here I can now much better notice clustering of hard sciences around certain universities, while Peace and Literature almost always only gave country when awarded, with no city or university affiliation so they're clustered around country center coordinates.*

> I really like the cool looking path animations, but didn't know they were encoding birth city to the location of the award. My first hunch was that they were moving from one nobel prize winner to the next, but after further inspection I found that wasn't the case. Maybe you can encode the birth city using a different shape or maybe that would be overkill and would lead to too much noise. I now look at the individual info pop-ups again and see that you list both birth city and location of award, but it might not "click" to the average viewer right away or it could just be me (smile) Let's see if others have similar feedback.

*This one I'm not sure of yet either. Right now I pop in the circles with a slight animation on the birth city, then move it to the award city. Drawing more shapes would be around 880 more objects to put on screen by the end. :/ I did have a working version of svg markers (much faster draws than creating shapes) that could put shapes (like directional arrows!) on each ends of the paths, but markers don't have any on/off hover/click calls available. =( I found it a bit less fun not being able to have any interactivity when trying to hover over a start/end shape. (Plus there were some issues with the enter/update/exit sequence and filters not working well with markers.)*
____________
#### **Feedback #3 Commits** [5][^5] [6][^6] [7][^7] [8][^8] [9][^9]

> Well done on finding and representing an interesting data story! I think the title and the graphic itself do a good job of communicating how the distribution of Nobel laureates has shifted over the last century or so. It's striking to see how many have moved from their homelands.

> My comments are ideas or points for you to reflect on rather than instructions! smile

> My biggest worry about this visualisation is overplotting. I don't think the overplotting detracts a lot from the overall message of the graphic (you could argue that it visually demonstrates the trend that you're trying to show), but it does make it difficult to interact with the plotted circles and hence to access the additional information that you've included in the tooltips. I don't have a clear recommendation for you on how to 'solve' this issue - it might end up being a compromise that you decide to make, and it may take some ingenuity to avoid the problem.

- Overplotting

*Overplotting is difficult when looking at the high level default zoom with all people. I'm still not sure how this can be dealt with well. :/ But I did find that I could allow greater zooming now. It was limited a bit before I added dynamic resizing of the circles and lines, since they got to be too huge! But now, zooming in only helps to create more space between close circles.*

*I also added some working zoom buttons to explicitly show that zooming in is an option for exploring the visualization further.*

> I, too, was at first confused about the meaning of the circles' movement. It was not intuitively obvious what was being represented by that movement and animation. However, once I figured it out it did seem to be a sensible way to show migration of these individuals.

> I recommend that you reflect on the options that you give your viewer in controlling the plot. In my opinion, there are too many details provided (we don't need to know or decide the exact amount of time taken for each year, a sense of 'slower' or 'faster' would suffice) and some of the options do not lead to better plots (for example, drawing paths without circles is pretty hard to read). Don't be shy to exert your editorial control and make decisions about what you want your viewer to see.

- Simplify

*I also took your advice and simplified the slider. Thanks! I left the migration lines as an option though since it can show overall trends at a glance without the clutter of circles.*

*I also added full names to bar chart bars, and removed the mouseover hover tooltip since it was no longer needed.*

*Since there are almost 900 entries, I wasn't quite sure how to effectively display multiple biographies. I'm hoping the extended zoom helps alleviate this in exploring the map. They should not be overlapping if you zoom in to a continent or country level.*

*But since there's a random jitter of coordinates (since many people ended up at the same institutions), it's still slightly possible that circles can appear very near each other. I had to limit the jitter since too much jitter could move them way out of their intended areas. The lines can also be selected if two are on top of each other, so hopefully that can help a bit.*

- Birth city

*I added a small note quickly explaining the circles' movements.*

>Now on to smaller issues.

>On the bar plot, it would be better to include the country names on or above the bars, rather than relying on a mouseover to reveal this information. Many people are not familiar with the country codes you used, so you can make life easier for them. You should be able to fit this text in the space you have.

>As I'm sure you're aware, it can be a bit tricky to use the mouseover for circles and especially the lines. It's a shame, because this is a fun way to make the visualisation more exploratory for the viewer, but if a viewer cannot access every point, it becomes difficult and somewhat frustrating.
Perhaps you could find alternative ways to display the biographical details for the Nobel laureates. Profiles displayed and filtered by year, continent or subject might be a nice addition.

>I like the title that you've used! smile I know what to look for in the visualization without being 'told' the answer.

- Title

*I also changed the title a bit to better reflect the overall story being told. I too was surprised at how many moved from their homelands (and where) over time!*

> I notice that Ivo Andric (Literature, 1961) is plotted in South America: this is probably a mistake as the information states he lived in Yugoslavia when he was awarded the Nobel prize. I noticed that there were problems with plotting Yugoslavia in the Data Visualization and D3.js course too, because it is not a current country. There may be other mistakes like this as you are dealing with historical geographical data - you should check for other instances of this.

- Historical Data

*Yea, historical data can be a pain! The coordinates are grabbed from a google API lookup. Yugoslavia not being a current country sent google to find a 'route' curiously named Yugoslavia in Argentina!*

*Thank you for pointing out this record.  I've had to manually correct at least 10 former countries/biography records so far due to country changing or even missing data from NobelPrize.org. Luckily, wikipedia and/or news articles usually have some relevant info. (smile)*

*For Mr. Andrić, "After the war, Andrić spent most of his time in his home in Belgrad... Andrić lived quietly in Belgrade, completing three of his most famous novels (there)... Died 13 March 1975 (aged 82) Belgrade, Yugoslavia"*

*This seemed close enough to place him in Belgrade at the time.. for this visualization at least, and use those coordinates. (smile) Literature/Peace prizes can be ambiguous since there's generally no institution they are tied to at the time, or even an explicit specific time period! :-o*

*Again, thank you so much for the valuable feedback! I tried to incorporate some changes to help where possible. I'm still not sure how to approach displaying more bio info, but I'll think about it some more. And please do let me know if I misunderstood anything, or if you have anymore questions, comments, or concerns. It's all much appreciated! (smile)*
____________

#### **Feedback #4 Commits** [10][^10]

Overall Changes Commit:

>DataVis - index.html: (Feedback changes) Change font sizes and color and button sizes for better readability, add 'Nobel Field' title for fields buttons and legend, add more instruction above map

Based on the following feedback:

- What do you notice in the visualization?

> Pretty cool how it visualizes. I can see that the location of the ball is where prize was awarded but would be cool to show in the line from A to B (like from light to dark) that this is going from this to there. Especially once the map has dots all over hard to tell whose gone where.

- What questions do you have about the data?

> Data is pretty straightforward but maybe having a header over the nobel types would help and making the box a little bigger since the text is pretty squeezed in there. On only look like oi so at first couldn't tell what it was.

- What relationships do you notice?

> Got nothing for this one...

- What do you think is the main takeaway from this visualization?

> A lot of foreign born winners got prizes in the US

- Is there something you don’t understand in the graphic?

> Came to understand everything but maybe some instruction would be nice or making the * note a different color so it stands out


### ***Resources*** 

- https://flowingdata.com/2014/08/04/cultural-history-via-where-notable-people-died/
- https://www.udacity.com/course/data-visualization-and-d3js--ud507
- https://www.udacity.com/course/intro-to-html-and-css--ud304
- https://www.udacity.com/course/javascript-basics--ud804 
- http://getbootstrap.com/
- http://d3js.org
- http://www.nobelprize.org 
- http://bost.ocks.org/mike/bar/
- https://www.dashingd3js.com/table-of-contents
- https://github.com/mbostock/d3/wiki/Tutorials
- http://alignedleft.com/tutorials/d3
- http://bl.ocks.org/patricksurry/6621971
- https://groups.google.com/forum/#!topic/d3-js/z9kqLRj7Puo
- http://christopheviau.com/d3_tutorial/
- http://stackoverflow.com/questions/14167863/how-can-i-bring-a-circle-to-the-front-with-d3
- http://stackoverflow.com/questions/7279567/how-do-i-pause-a-window-setinterval-in-javascript/7282347#7282347
- http://alvarotrigo.com/blog/firing-resize-event-only-once-when-resizing-is-finished/
- http://bost.ocks.org/mike/constancy/
- http://zeroviscosity.com/d3-js-step-by-step/step-5-adding-tooltips 
- http://stackoverflow.com/questions/21153074/d3-positioning-tooltip-on-svg-element-not-working

[1]: http://flowingdata.com/

[2]: https://flowingdata.com/2014/08/04/cultural-history-via-where-notable-people-died/

[3]: http://www.github.com

[nobel_org]: http://www.nobelprize.org/nobel_prizes/

[data_viz]: http://fch808.github.io/Data%20Visualization/Project/index.html

[source_code]: https://github.com/FCH808/FCH808.github.io/tree/dataViz/Data%20Visualization/Project

[projects]: http://fch808.github.io/

[initial_commit]: https://github.com/FCH808/FCH808.github.io/blob/bad1f602700664dd9cb150fe5f1bea9a8cb9e25c/Data%20Visualization/Project/index.html

[maps_api]: https://developers.google.com/maps/documentation/business/geolocation/

[python]: https://www.python.org/

[wiki]: https://www.wikipedia.org/

[NYTimes]: http://www.nytimes.com/

[nobel_py]: https://github.com/FCH808/FCH808.github.io/blob/master/Data%20Visualization/Project/wrangle/nobel_scrape_version2.py

[wrangle.py]: https://github.com/FCH808/FCH808.github.io/blob/master/Data%20Visualization/Project/wrangle/wrangle.py

[latlon.py]: https://github.com/FCH808/FCH808.github.io/blob/master/Data%20Visualization/Project/wrangle/latlon.py

[^1]: https://github.com/FCH808/FCH808.github.io/commit/bad1f602700664dd9cb150fe5f1bea9a8cb9e25c

[^2]: https://github.com/FCH808/FCH808.github.io/commit/4cdbd0548eafdf7c558191032819420d1e7aca75

[^3]: https://github.com/FCH808/FCH808.github.io/commit/ee260ecf24f2b5795022a32dfed4726cb8363cc4

[^4]: https://github.com/FCH808/FCH808.github.io/commit/238709080a6c3d11e01dbb158e2829f4b76ed81b

[^5]: https://github.com/FCH808/FCH808.github.io/commit/f0dcbbdabc3a34588a6e36d9e08d2bfb9a85a2b0

[^6]: https://github.com/FCH808/FCH808.github.io/commit/fa93937581d3c89e95f929dcfedb41dc814d066f

[^7]: https://github.com/FCH808/FCH808.github.io/commit/32e9108a727dd40a65c531c80b526c8cdbab4828

[^8]: https://github.com/FCH808/FCH808.github.io/commit/f59ffbdd5de6685223ffd23993f31175ae4ced37

[^9]: https://github.com/FCH808/FCH808.github.io/commit/65fcbc046006ded88eb4ae67ad9168fe7857d3a4

[^10]: https://github.com/FCH808/FCH808.github.io/commit/50683ec27ee055dcb8fad770d88282f1b0b72f77 

[^11]: https://github.com/FCH808/FCH808.github.io/commit/e38cc3bf33053ed585945612cd078e076a107d80

[^12]: https://github.com/FCH808/FCH808.github.io/commit/e680ae572aea1b784f534a3df432e639bf0e7c77

- And countless more stackoverflow and google queries when troubleshooting!


