
This is the folder of data analysis: Goal analysis and Conceded goal analysis:

1."goal_analysis" folder contains following code:

mongo_attending_time.py:
This module makes statistics of market value, time played and other data of all the players in Premier league during last three seasons.


mongo_goal_type.py:
This module makes statistics the composition of goal types for all the clubs of Premier League during last three seasons.

mongo_height.py:
This module makes statistics of the players detailed information such as name, height, market value and other technical statistics.
If the player is a goalkeeper, his technical statistics will include goals, conceded goals, clean sheets, yellow cards and red cards.
Otherwise, the technical statistics will be goals, assists, yellow cards and red cards.

mongo_partner.py:
This module calculates the total cooperating goals between two player (one player assisted, the other made goals) in order to find out the top duos of the league

2. "conceded_goal" folder contains following code:

goalkeeper.py:
This module calculates the total number of conceded goals, the corresponding goalscoring player as well as the player's height, nationality, goal type.