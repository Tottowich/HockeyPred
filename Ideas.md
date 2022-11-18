# Ideas for solving issues in the project.

## Data 


### Data Scraping
As for now data should be scraped from [Hockey-Reference](https://www.hockey-reference.com/)
and maybe [Elite Prospects](https://www.eliteprospects.com/). Primary focus is on the NHL.

The data should be scraped from the following pages:

* [NHL](https://www.hockey-reference.com/)

The data should be formatted as a csv file/files with the following structure:

* Row represents a game
* Column represents a feature

### Data Features
The features should be: (All these features should be hopefully normalized and based on point upon that point of the season)

* Link to the game, should be ignored when training the model
* Date of the game
* Team ID of the home team

Team specific features:

* Powerplay precentage  up to that point in the season
* Boxplay precentage up to that point in the season
* Avg. goals   might not be normalizable. That would be the (ranking of goals scored)/(number of teams).
* Avg. goals against   might not be normalizable. That would be the (ranking of goals against)/(number of teams).
* Shots per game  
* Save percentage  
* Hits per game
* Blocks per game
* Faceoff win percentage
* Ratio of goals scored to goals against
* Ratio of goals scored in even strength to goals scored in powerplay
* Ratio of goals conceded in even strength to goals conceded in boxplay.
* Ranking of penalty minutes taken.
* Ranking of penalty minutes drawn.

All of these features should also be added for the away team.
There should also be the same features as above but for the past "n" games possibly with a different weight for each game (moving average).
Might add more features later as well as player specific features.



### Data cleaning

The data should be cleaned an preferably normalized to make it easier to work with and more appropriate for machine learning.

### Data analysis

The data should be visualizable. This can be done with graphs and tables.

## Machine learning

The data should be used to train a machine learning model. The model should be able to predict the outcome of a game predicting.

### Current Idea
 