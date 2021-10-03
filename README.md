# ACES-NASA
## Eye Above : Mapping Space Trash in Real Time 

https://aces-nasa.space/

Today, there are more than 128million pieces of debris orbiting our planet that endanger space operations. Each time a collision happens, more debris is generated. The aim of the project is to give an overview of the position of the satellites in actual, past, and future time so we can monitor their trajectories and change them if necessary to avoid collisions. We developed a website that allows users to visualize satellites, sorted by category. The site makes predictions about its future position so the user can go through the time by using a slide bar. Finally, these coordinates are displayed when the user passes the mouse through it on the 3D visualization.

### DETAILED PROJECT DESCRIPTION
### Implementation

We used Python to retrieve the data, and Javascript to use the NASA WorldWind, which was the geo spatial map we used. The use of Flask allowed us to link the Python script to our javascript file. Javascript allowed us to use WorldWind and thanks to the coordinates recovered by the Python script, we can display placemarks corresponding to the debris/satellites. Finally, we run our Python script every second, which allows us to have the future positions of the debris/satellites, which we estimate.

### Features

- The user can see the debris on the map, so he can choose which category of debris/satellites he wants to see. Here is the list of available categories: 



      Special-Interest Satellites
      Weather & Earth Resources Satellites
      Communications Satellites
      Navigation Satellites
      Scientific Satellites
      Miscellaneous Satellites


- The user by placing his cursor on a debris/satellite, the information (id, name, altitude, latitude, longitude) of the debris/satellite are then displayed on the right of the site.

 

- The user can also look at an estimate of where the debris will be in the coming weeks (5 weeks maximum), he can also look at an estimate of where the debris was in the previous weeks (5 weeks before maximum) 

### WEB Infrastructure
Our domain DNS are managed by CloudFlare, this allows us to have several advantages:



   - A Content Delivery Network: it allows us to optimize loading time by caching HTML, JavaScript, CSS & Images.
   - DDOS mitigation: it protects us from denial of service attacks. This is the act of overloading a server (filling all the available space) so that no one can access it.
   - Robot protection: this protects us from bots that try to steal content on the site or do brute force (try lots of passwords on the platform).
   - Possession of a Firewall: it allows us to manage the different types of access, to block certain countries or malicious people, etc.
 

A server has been set up running the Windows Server 2019 operating system. Regarding the configuration of our servers, it consists of 2 virtual cores, 4GB of ram and 70GB of Premium SSD storage.

Our servers are elastic, which means that it is possible to completely change the different components like RAM, processor and storage. This is a considerable advantage on the economic side.

When there is a peak of users, it makes more sense to increase the power of the components and vice versa. Working in this way allows us to pay according to usage compared to Private Cloud where it is necessary to buy the components.

### Saves & Disaster Recovery

Our servers are automatically backed in our Azure storage accounts, everyday at 2am.

Our server is replicated in a second Azure region 100km away, all data is replicated between the two regions. The goal is to avoid the loss of data, it is one of the regions to work due to natural or technical causes, the second will be there to take over.

The data is also kept in an On-Premise server (private cloud/local in an office) in case of complete data loss with our provider.

### Security Summary

Front-End/Back-End Protection:

We have added multiple security layers:



- CloudFlare DNS Server
- DDOS Mitigation: This protects us from denial and services attacks. This is the idea of overloading a server (filling all the space available) so anyone else can access.
- Protection against Bots: This protects us from bots that try to steal site content or that try to break authentication through a brute force by trying lots of passwords on the platform.
- Firewall ownership: This allows us to generate different kinds of access, block certains countries, malicious people, etc.
- FireWall on the NSG (Network Security Group) 

### SPACE AGENCY DATA

We used space-track and celestrack data to retrieve TLE files of the debris/satellites, then parsed through them to get the coordinates and infos of every space object existing in their data base in order to combine it with nasa's worlwind and visualize the data on the 3D map [in real time, past, and predicted future] on the website that we built.

We also tried to merge the new data base that we created through the parsing and a new data base that we built from acquiring conjunction data from space-track with the ESA's collisions data base in order to analyze the data and apply Machine Learning/ Artificial Intelligence techniques on it. But due to the lack of time [and conjunction data], we opted to scrap this part from the website and only leave the files related to it on the project's Github.

https://www.space-track.org/ https://www.celestrak.com/NORAD/elements/
https://kelvins.esa.int/collision-avoidance-challenge/data/
https://worldwind.arc.nasa.gov/web/

### REFERENCES

Data:

    CelesTrack https://celestrak.com/NORAD/elements/

    SpaceTrack https://www.space-track.org/

    Data Collision https://kelvins.esa.int/collision-avoidance-challenge/data/



Python 3:

    PyEpheme

    NumPy

    Flask



JavaScript:

    Nasa WorldWind https://worldwind.arc.nasa.gov/web/
