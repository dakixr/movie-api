Here are the specific steps you need to follow:

# 1 Implement database

• Create a database. Implement migration scripts.

• Create database tables by provided description:Movies table:

• MovieID (unique identifier)
• Title (title of the movie)
• ReleaseYear (year of release)
• Director (name of the director)
• Genre (genre of the movie)
• Rating (rating of the movie)

Actors table:
• ActorID (unique identifier)
• Name (name of the actor)
• BirthYear (year of birth)
• Nationality (actor's nationality)

Directors table:
• DirectorID (unique identifier)
• Name (name of the director)
• BirthYear (year of birth)
• Nationality (director's nationality)

MovieActor table (to establish a many-to-many relationship between movies and actors):
• MovieID (foreign key referencing the Movies table)
• ActorID (foreign key referencing the Actors table)

# 2 Implement data import endpoint
• Modify the code to include an import endpoint that loads the movie data csv and xlsx files - IMDBMovies2000-2020.csv and IMDBMovies2000-2020.xlsx.
• Implement data export endpoint:
• Implement the code to retrieve data from SQLite database and expose all fields available. If possible, implement some filters.

Note: Ensure that you handle any necessary data cleaning and transformation steps to obtain the desired movie data.

Deliverables:

• Working movie api application with migration scripts executed on startup.
• Implemented endpoint to load data from csv and xlsx files to SQLite database.
• Modified data export endpoint generating csv and xlsx files from SQLite database. Filtering functionality will be considered as a plus.
• The SQLite database contains the relevant movie release data from two provided files csv and xlsx files.

Evaluation Criteria:
You will be evaluated based on the following:

• Working application.
• Correctness and completeness of the code fixes and modifications.
• Accuracy of fetching and storing the movie release data in the SQLite database.
• Pytest covering business logic (Nice to have).
• Proper handling of any data cleaning or transformation steps (Nice to have).
• Adherence to Python coding conventions and best practices (Nice to have).
• Clarity and organisation of the code (Nice to have).
• Filtering options in api (Nice to have).
• Small instructions how to run the application, adjustments in current readme.

If there are questions/problems we can meet at google meet. When the time comes to share the code, please upload it to your private git repo and give access to my user. My git username is zawich.

Please confirm you received this email and started the assessment.

Good luck and enjoy!
Zawich recruitment