![alt text](http://library.columbia.edu/content/libraryweb/locations/business/_jcr_content/layout_featuredcontent/image.img.jpg/1369336790208.jpg)
#What do we know about Density's data?

---

##[CUIT](https://cuit.columbia.edu/) has supplied us with our data set.


###We receive device counts from specific routers aggregated into 15 minute intervals

Devices connect to wifi routers across Columbia's campus.  CUIT aggregates device collection data by building and by floor and supplies with a live count of the number of devices connected at each location every 15 minutes.

---

#What spaces do we have?

###We have various libraries, John Jay, and Lerner.

---

#Just how full is a study space?



![alt text](http://www.hercampus.com/sites/default/files/2013/12/02/4192655241_df21ba1706.jpg)


There's an obvious difference beteween a space that is unusually crowded like during orgo night, and a typical busy day.

![alt text](http://library.columbia.edu/content/libraryweb/locations/butler/_jcr_content/layout_featuredcontent/image.img.jpg/1368472856821.jpg)

Density assumes that capacity is relative to fullness on an average day, not on outlier days.  How do we do that? By considering what the average day like at each space.

###On an average day at Columbia, device count grows until it stablizes for the day

![alt text](avg_day.png)
#Capacity is the level at which population growth stabilizes

###For the capacity of whole campus of Columbia, it would be 2248

---

#Different spaces have different properties

##For example, Butler library behaves very differently from John Jay:

###This is Butler:

![alt text](Butler_day.png)

People tend to come in after lunch, take a break for dinner, and work late into the night.

###This is John Jay:
![alt text](JJ_day.png)

The dining halls are most crowded around mealtimes.

---

#How does campus population vary over time?

###We can find differences in population based on changes in semesters, exams, and holidays
![alt text](dev_series.png)
There's a clear weekly cycle in the number of devices connected across campus.  Let's remove the weekly cycle by grouping the data into weeks. Smoothing out the data by grouping by week allows us to see differences in semesters and holidays more clearly e.g. the big drop around Thanksgiving and the following spike for Finals.
![alt text](weekly_count.png)

Aggregating the data by week allows us to see that there's a jump in the number of devices when the semester starts.  We also see dips for fall break, spring break, and Thanksgiving.  Thanksgiving is followed by a spike for finals.  Winter break is also visible following the dramatic drop in device count.

---

##How does day of the week affect study habits?

###People don't study on weekends:

![alt text](dayofweek.png)

---

##We can also find days with unusually high number of devices

Our plots show the days with the max. number of devices recorded at any time at that location.  Using these graphs, we can identify special days during the school year.

##Like NSOP
![alt text](nsop.png)

We see multiple spikes in Roone Arledge Auditorium around the same time as orientation.

##And Orgo Night!
![alt text](orgonight.png)

Notice the spike in Butler 2 around midnight.

##For more tools with the Density API, check out Chris Mulligan's [Relative Density App!](https://chmullig.shinyapps.io/relative_density/)


#To see the code that generated our visuals check out our [ipython notebook!](http://nbviewer.ipython.org/github/jzf2101/density/blob/master/datasci/density_demo.ipynb)

#Check out our [API](http://density.adicu.com/docs) to use our data!