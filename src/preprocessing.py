## Preprocessing functions

import ast
import os
import pandas as pd
import requests
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

# Define the genre mappings globally 
GENRE_MAPPING = {
    "Action/Adventure": [
        "Action", "Adventure", "Supernatural", "Space western", "Action/Adventure", 
        "War film", "Epic", "Period piece", "Wuxia", "Martial Arts Film", 
        "Western", "Adventure Comedy", "Historical Epic", "Action Comedy", 
        "Gangster Film", "Epic Western", "Action Thrillers", "Sword and sorcery", 
        "Heist", "Survival", "Sword and Sandal", "Spy", "Superhero movie", "Combat Films", "Fantasy Adventure", 
        "Sword and sorcery", "Time travel", "Doomsday film", "Escape Film", 
        "Prison", "Hybrid Western", "Costume Adventure", "Roadshow theatrical release",
        "Spaghetti Western", "Women in prison films", "Road movie", "Heist", "Biker Film", 
        "Swashbuckler films", "Cavalry Film", "Space opera", "Tokusatsu", 
        "Extreme Sports", "Apocalyptic and post-apocalyptic fiction", 
        "Chase Movie", "Revisionist Western", "Caper story", "Jungle Film", 
        "B-Western", "Travel", "Auto racing", "Roadshow/Carny", "Exploitation", "Sword and Sandal", "Star vehicle", 
        "Alien invasion", "Revenge", "Foreign legion", "Indian Western", 
        "Road-Horror", "Outlaw biker film", "Prison escape", "Acid western", 
        "War effort", "Horse racing", "Movies About Gladiators", "Beach Film",
        "Outlaw", "Ninja movie", "Buddy Picture", "Singing cowboy", 
        "Beach Party film", "Adventure", "Action/Adventure", "Epic Western", "War film", "Epic", "Period piece",
        "Disaster", "Ensemble Film", "War film", "Samurai cinema", "Live action"
    ],
    "Comedy": [
        "Comedy", "Romantic comedy", "Satire", "Slapstick", "Parody", "Black comedy", 
        "Mockumentary", "Adventure Comedy", "Comedy-drama", "Comedy film", 
        "Comedy horror", "Screwball comedy", "Comedy of Errors", "Romantic comedy", 
        "Domestic Comedy", "Musical comedy", "Crime Comedy", "Fantasy Comedy", "Comedy of Errors", "Comedy Western", 
        "Screwball comedy", "Domestic Comedy", "Musical comedy", "Comedy horror", 
        "Buddy film", "Sex comedy", "Parody", "Media Satire", "Gross-out film", 
        "Gross out", "Dogme 95", "Backstage Musical", "Heavenly Comedy", "Stand-up comedy", "Comedy Thriller", 
        "Workplace Comedy", "Humour", "Camp", "Mondo film", "Bloopers & Candid Camera", "Comdedy", 
        "Ealing Comedies", "Female buddy film", "Breakdance", "Kafkaesque", "Buddy Picture", "Chick flick",
        "Comedy", "Comedy-drama", "Parody", "Satire", "Musical", "Slapstick", "Comedy ", "Comedy film",
        "Comedy of manners", "Courtroom Comedy", " Comedy"
    ],
    "Drama": [
        "Drama", "Crime Drama", "Crime Fiction", "Biographical film", 
        "Historical fiction", "Family Drama", "Romantic drama", "Costume drama", 
        "Marriage Drama", "Political drama", "Courtroom Drama", "Legal drama", 
        "Historical drama", "Coming of age", "Culture & Society", "History", 
        "Social issues", "Tragicomedy", "Avant-garde", "Experimental film", 
        "New Hollywood", "Childhood Drama", "Melodrama", "Art film", "Political cinema", 
        "Tragedy", "Feminist Film", "Juvenile Delinquency Film", "Christian film",
        "Educational", "Language & Literature", "Linguistics", "Film à clef", 
        "Rockumentary", "Medical fiction", "Buddy cop", "Docudrama", 
        "Anthology", "Existentialism", "Social problem film", 
        "Slice of life story", "Kitchen sink realism", "British New Wave", 
        "Addiction Drama", "Inspirational Drama", "Illnesses & Disabilities", 
        "Interpersonal Relationships", "Expressionism", "Early Black Cinema", 
        "British Empire Film", "Northern", "Filmed Play", "Nature", "Mumblecore", "Boxing", "Business", "Journalism", 
        "Conspiracy fiction", "Crime", "Master Criminal Films", 
        "Feature film", "Cold War", "World History", "School story", "Patriotic film", "Statutory rape", "New Queer Cinema", "Neorealism", 
        "The Netherlands in World War II", "Homoeroticism", "Drama ", "Romantic drama", "Historical Epic", "Romance Film", "Family Film", "Biopic [feature]",
        "Social issues", "Bollywood", "Crime Fiction", "Television movie", "Filipino Movies", "Film adaptation", "Teen",
        "Blaxploitation", "Sexploitation", "Tollywood", "Erotic Drama", "Pre-Code", "Anti-war", "Anti-war film", "Surrealism", 
        "Bengali Cinema", "Race movie", "Hip hop movies", "Czechoslovak New Wave"
    ],
    "Thriller/Suspense": [
        "Thriller", "Mystery", "Psychological thriller", "Erotic thriller", 
        "Suspense", "Crime Thriller", "Psychological horror", "Noir", "Film noir", 
        "Future noir", "Crime Comedy", "Political thriller", "Detective fiction", "Detective", "Film", 
        "Film & Television History", "Propaganda film", "Political satire", 
        "Natural disaster", "Remake", "Plague", "Giallo", "Whodunit", "Demonic child",
        "Neo-noir", "Private military company", "Psycho-biddy", 
        "Psychological horror", "Sci-Fi Thriller", "Z movie", "Romantic thriller", "Point of view shot",
        "Thriller", "Psychological thriller", "Crime Thriller", "Crime Fiction"
    ],
    "Horror": [
        "Horror", "Zombie Film", "Slasher", "Monster movie", "Supernatural", 
        "Sci-Fi Horror", "Erotic Horror", "Gothic Film", "Natural horror films", 
        "Haunted House Film", "Horror Comedy", "Monster movie", "Natural horror films", "Creature Film", 
        "Gothic Film", "Costume Horror", "Haunted House Film", "Monster", "Demonic child",
        "Splatter film", "Werewolf fiction", "Period Horror", 
        "Albino bias", "Vampire movies", "Revisionist Fairy Tale", "Goat gland",
        "Horror", "Sci-Fi Horror", "Erotica", "Sexploitation"
    ],
    "Science Fiction (Sci-Fi)": [
        "Science Fiction", "Sci-Fi", "Space western", "Alien", "Cyberpunk", 
        "Dystopia", "Sci-Fi Horror", "Apocalyptic and post-apocalyptic fiction", 
        "Alien invasion", "Time travel", "Dystopia", "Time travel", "Sci-Fi Adventure", "Alien Film", 
        "Apocalyptic and post-apocalyptic fiction", "Science fiction Western", "Cyberpunk", "Steampunk",
        "Sci Fi Pictures original films", "Therimin music", "Science Fiction", "Sci-Fi", "Reboot" 
    ],
    "Fantasy": [
        "Fantasy", "Magical", "Mythical", "Urban Fantasy", "Children's Fantasy", 
        "Sword and sorcery", "Fairy tale", "Mythological Fantasy", "Fantasy Adventure",
        "Romantic fantasy", "Fairy tale", "Sword and sorcery films", "Mythological Fantasy", 
        "Fantasy Drama", "Heaven-Can-Wait Fantasies", "Revisionist Fairy Tale",
        "Fantasy", "Magical"
    ],
    "Romance": [
        "Romantic", "Romance Film", "Romantic comedy", "Romantic drama", "Gay", 
        "Gay Interest", "Gay Themed", "Romantic fantasy", "Interpersonal Relationships",
        "Family & Personal Relationships", "Romantic thriller", "Romance Film", "Romantic drama",
        "Music", "LGBT", "Gay pornography", "Romance Film", "Punk rock", "Pornographic movie", "Adult",
        "Pornography", "Hardcore pornography", "Dance"
    ],
    "Documentary": [
        "Documentary", "Biography", "Biographical film", "Historical Account", 
        "Docudrama", "History", "Educational", "Inspirational Drama",
        "Educational", "Language & Literature", "Rockumentary", "Anthropology", 
        "Religious Film", "Environmental Science", "Essay Film", "Graphic & Applied Arts", 
        "Libraries and librarians", "Historical Documentaries", "Political Documetary", "Education", 
        "World History", "News", "Archives and records", "Media Studies", 
        "Inventions & Innovations", "Instrumental Music", "The Netherlands in World War II",
        "Documentary", "Social issues", "Documentary", "Music", "Concert film", "Sports",
        "Sponsored film", "Docudrama "
    ],
    "Animation/Family": [
        "Animation", "Family Film", "Children's/Family", "Children's Fantasy", 
        "Cartoon", "Animated", "Musical comedy", "Family-Oriented Adventure",
        "Anime", "Children's", "Computer Animation", "Stop motion", "Animated Musical", 
        "Animated cartoon", "Tamil cinema", "Animals", "Anima l Picture", "Pinku eiga",
        "Children's Entertainment", "Children's Issues", "Clay animation", 
        "Supermarionation", "Silhouette animation", "Jukebox musical", 
        "Operetta", "Parkour in popular culture", "Family Film", "Children's/Family",
        "Chinese Movies", "Christmas movie", "Animation "
    ]
}

FALLBACK_MAPPING = {
     "Short Film": "Drama",
    "Indie": "Drama",
    "Black-and-white": "Drama",
    "Silent film": "Drama",
    "Fan film": "Fantasy",
    "Cult": "Thriller/Suspense",
    "Experimental film": "Drama",
    "Satire": "Comedy",
    "Erotic": "Drama",
    "Softcore Porn": "Romance",
    "Historical Epic": "Action/Adventure",
    "Educational": "Documentary",
    "Japanese Movies": "Animation/Family",
    "World cinema": "Drama",
    "Musical": "Animation/Family",
    "Bollywood": "Drama",
    "Epic Western": "Action/Adventure",
}

EXTENDED_FALLBACK_MAPPING = {
    **FALLBACK_MAPPING,
    "Anthology": "Drama",
    "Existentialism": "Drama",
    "Social problem film": "Documentary",
    "Sci-Fi Adventure": "Science Fiction (Sci-Fi)",
    "Fantasy Adventure": "Fantasy",
    "Horror Comedy": "Horror",
    "Romantic thriller": "Romance",
    "Comedy Thriller": "Thriller/Suspense",
    "Steampunk": "Science Fiction (Sci-Fi)",
    "Historical Documentaries": "Documentary",
    "Art film": "Drama",
    "Music": "Documentary",
}



############

# Define the Indian Ethnicities
South_Indian_Ethnicities =[
    'Tamil', 'Nair', 'Bunt (RAJPUT)', 'Tamil Brahmin', 'Telugu people', 'Malayali', 'Karnataka Brahmins',
    'Kannada people', 'Niyogi','Sri Lankan Tamils', 'Chitrapur Saraswat Brahmin', 'Tulu people',
    'Konkani people', 'Gaud Saraswat Brahmin', 'Mangaloreans' , 'Mudaliar', 'Telugu Brahmins', 'Chettiar']

North_Indian_Ethnicities = [
    'Punjabis', 'Pashtuns', 'Sindhis', 'Kayastha', 'Kashmiri Pandit', 'Bihari people',
    'Jaat', 'Sikh',  'Kashmiri people', 'Jatt Sikh', 'Pathani', 'Rajput', 'Marwari people',
    'Rohilla', 'Khatri', 'Mohyal', 'Dogra', 'Dalit', 'Agrawal']

Eastern_Indian_Ethnicities = ['Bengali', 'Bengali Hindus', 'Bhutia']

Western_and_Central_Indian_Ethnicities = [
    'Parsi', 'Gujarati people', 'Marathi people', 'Ezhava', 'Chaliyan', 'Indian']

Indian_Diaspora = [
    'British Indian','Nepali Indian','Indian Americans', 'Anglo-Indian people', 'Muhajir diaspora',
    'Indian Australian', 'Indian diaspora in France', 'Punjabi diaspora', 'Indo-Canadians', 'Tamil Americans']

Religious_and_Caste_Groups = [
    'Kanyakubja', 'Brahmins', 'Brahmin', 'Muslim', 'Hindkowans', 'history of the Jews in India', 'Hindu',
    'Mizrahi Jews', 'Jewish people']

Non_Indian_Ethnicities = [
    'Pakistanis','Afghans in India', 'Iranian peoples', 'Italians', 'Romani people',
    'British', 'Irish people', 'White people', 'Asian people', 'English people', 'Australians',
    'African Americans', 'Czechs', 'Pakistani Americans', 'Sudanese Australians', 'Sinhalese', 'French',
    'White British',' White Americans', 'Poles', 'British Americans', 'Native Hawaiians', 'White South Africans',
    'Spanish Americans', 'Italian Americans', 'Swedes', 'Welsh Americans', 'Brazilians', 'Puerto Ricans', 
    'Hispanic and Latino Americans', 'Uruguayans', 'British Asians', 'Germans', 'Irish migration to Great Britain',
    'Asian Americans', 'African people', 'Italian Australians', 'Anglo-Irish people', 'Vietnamese people']

######################

# Define the African American ethnicities
african_american_ethnicities = [
    "African Americans", "Black people", "British Nigerian", "Yoruba people",
    "African-American Jews", "Black Canadians", "Afro Trinidadians and Tobagonians",
    "Afro-Cuban", "Black Britons", "Blackfoot Confederacy", "African people",
    "Bahamian Americans", "British Jamaicans", "Haitian Americans", "Ghanaian Americans",
    "Afro-Asians", "Afro-Guyanese", "Black Hispanic and Latino Americans", 
    "Mandinka people", "Barbadian Americans", "Wolof people", "multiracial American",
    "Akan people", "Xhosa people", "South African Americans",
    "Sierra Leoneans in the United Kingdom", "Kabyle people", "Berber",
    "Louisiana Creole people", "Nigerian Americans", "Dinka people",
    "Ghanaian", "Somalis"
]

# Define the American Indians ethnicities
american_indian_ethnicities = [
    "American Indians", "Omaha Tribe of Nebraska", "Cherokee", "Aboriginal Australians",
    "Native Hawaiians", "First Nations", "Indigenous peoples of the Americas",
    "Native Americans in the United States", "Mohawk", "Sioux", "Ojibwe", "Lumbee",
    "Cree", "Choctaw", "Five Nations", "Cheyennes", "Oneida", "Dene", "Nez Perce", "Ho-Chunk",
    "Samoan Americans", "Pacific Islander Americans", "Māori", "Inuit", "Apache",
    "Métis", "Aymara", "Iñupiaq people",
]

# Define the Arab Americans ethnicities
arab_american_ethnicities = [
    "Arab Americans", "Iranian peoples", "Afghans in India", "Muslim", "Pashtuns",
    "Lebanese Americans", "Moroccan Americans", "Syrian Americans", "Pathani",
    "Arabs in Bulgaria", "Sudanese Arabs", "Persians", "Lebanese people",
    "Moroccans", "Palestinians in the United States", "Arab Mexican",
    "Lebanese people in the United Kingdom", "Arabs", "culture of Palestine", "مسح",
    "Iranians in the United Kingdom", "Iraqi Americans", "Egyptians", "Iranian Americans",
    "Iranian Canadians"
    
]

# Define the Asian Americans ethnicities
asian_american_ethnicities = [
    "Asian Americans", "Asian people", "Indian Americans", "Japanese Americans", "Filipino Americans",
    "Tamil", "Punjabis", "Sindhis", "Telugu people", "Koreans", "Bengali", "Chinese Americans",
    "Filipino people", "Indonesian Americans", "Sri Lankan Tamils", "Tamil Americans", "Taiwanese Americans",
    "Kashmiri Pandit", "Telugu Brahmins", "Jatt Sikh", "Kannada people", "Brahmin", "Chinese Filipino",
    "Pakistani Canadians", "Sri Lankan Tamil diaspora", "Filipino Australians", "Chinese Singaporeans",
    "Nepali Indian", "Sikh", "Chaliyan", "Malaysian Chinese", "Hmong Americans", "Koryo-saram", 
    "Burmese Americans", "Vietnamese Americans", "Thai Chinese", "Cambodian Americans", "Chinese Indonesians",
    "Pakistani Americans", "Indian diaspora in France", "Indo-Canadians", "Kashmiri people", "Bengali Brahmins",
    "Rohilla", "Sinhalese", "Hindu", "Ryukyuan people", "Bangladeshi Americans", "Thai Americans", "Thai people",
    "Indian Australian", "Indian diaspora", "Punjabi diaspora", "Filipino mestizo", "Japanese Brazilians",
    "Tibetan people", "Hazaras", "Zhuang people", "Dogra", "Kurds", "Goans", "Gujarati people", "Indians",
    "Bihari people", "Hongkongers", "British Indian", "Bengali Hindus", "Korean Americans", "Kiwi", "British Chinese",
    "British Asians", "Vietnamese people", "Chinese Jamaicans", "Taiwanese people", "Sherpa", "Tamil Brahmin",
    "Lao people", "Manchu", "Jaat", "Bhutia", "Marathi people", "Kanyakubja Brahmins",
    "Gin people", "Pakistanis", "Dalit"
]

# Define the Latinos ethnicities
latino_ethnicities = [
    "Hispanic and Latino Americans", "Latinos", "Puerto Ricans", "Mexican Americans", 
    "Cuban Americans", "Stateside Puerto Ricans", "Colombian Americans", "Chilean Americans", 
    "Cajun", "Criollo people", "Portuguese Americans", "Bolivian Americans", "Cubans", 
    "Brazilian Americans", "Brazilians", "Ecuadorian Americans", "Galicians", 
    "White Latin American", "Colombians", "Chileans", "Chileans in the United Kingdom", 
    "Peruvians in the United Kingdom", "Venezuelans", "Hondurans", "Honduran Americans", 
    "Acadians", "Salvadoran Americans", "Panamanian Americans", "Indo Caribbeans", 
    "Tejano", "Spaniards in Mexico", "Spanish people of Filipino ancestry", "Spanish Americans",
    "Uruguayans", "Mexicans", "Guyanese Americans", "Dominican Americans", "Spaniards",
    "Hispanic", "Colombian Australian", "Chinese Canadians", "Portuguese", "Latino",
    "Latin American British", "Venezuelan Americans", 
    
]

# Define the Jewish Americans ethnicities
jewish_american_ethnicities = [
    "Jewish people", "American Jews", "African-American Jews", "Mizrahi Jews", 
    "Ashkenazi Jews", "Sephardi Jews", "British Jews", "Israeli Americans", 
    "history of the Jews in India", "Moroccan Jews", "Lithuanian Jews", 
    "Israeli Jews", "Assyrian people", "Israelis"
]

# Define the Caucasian Americans ethnicities
caucasian_american_ethnicities = [
    "Whites", "White people", "White Americans", "White British", "Italian Americans",
    "Irish Americans", "Scottish Americans", "German Americans", "Russian Americans",
    "French", "English Americans", "European Americans", "Scandinavian Americans",
    "Swedish Americans", "Finnish Americans", "Canadian Americans", "Dutch Americans",
    "Hungarian Americans", "Lithuanian Americans", "Austrians", "French Canadians",
    "English people", "Irish people", "Norwegian Americans", "Austrian Americans",
    "Albanian Americans", "Romanichal", "Parsi", "Swiss", "Latvians", "Belgians",
    "Italian Australians", "Australian Americans", "English Canadians", "English Australian",
    "French Chilean", "Hungarians", "Greek Americans", "Greeks in South Africa", 
    "Sicilian Americans", "Slovaks", "Slovak Americans", "Serbs of Croatia", 
    "White South Africans", "Dutch", "Dutch Australian", "Russian Canadians", 
    "German Canadians", "Romanian Americans", "Polish Canadians", "Czechs", 
    "Belarusians", "Serbs in the United Kingdom", "Serbian Canadians", "Greek Canadians",
    "Greek Cypriots", "Catalans", "Croatian Canadians", "Croatian Americans", 
    "Argentines", "Sámi people", "Welsh Americans", "Welsh Italians", "Tulu people",
    "Mohyal", "Anglo-Indian people", "Anglo-Irish people", "Canadians in the United Kingdom",
    "Slovene Americans", "Aromanians", "Swedish-speaking population of Finland", 
    "Bulgarian Canadians", "Ukrainian Americans", "Italians in the United Kingdom",
    "Croatian Australians", "Irish Australians", "Swedish Canadians", 
    "French-speaking Quebecer", "Finns", "Albanians", "Polish Australians", 
    "Mudaliar", "Serbian Australians", "Romani people", "Rajput", "Turkish Americans", "Gibraltarian people",
    "Sri Lankan Americans", "Icelanders", "Québécois", "Italian immigration to Mexico", 
    "Corsicans", "Danish Canadians", "Dutch Canadians", "German Brazilians", 
    "Greek Australians", "Slovenes", "Basque people", "Tatars", 
    "Austrians in the United Kingdom", "Transylvanian Saxons", "Afrikaners",
    "Sierra Leone Creole people", "Georgians", "Italians", "Armenians", "Danish Americans",
    "Russians", "Welsh people", "Italian Canadians", "Scottish Australians", "White Africans of European ancestry",
    "Americans", "British", "Serbian Americans", "Polish Americans", "Germans",
    "Irish migration to Great Britain", "Scotch-Irish Americans", "Black Irish", "Scottish people",
    "British Americans", "Australians", "French Americans", "Czech Americans", "Danes",
    "Armenian Americans", "Irish Canadians", "Scottish Canadians", "Italian Brazilians", "Swedes",
    "names of the Greeks", "Slavs", "Anglo-Celtic Australians", "Eurasian", "Poles",
    "Norwegians", "Croats", "Ukrainian Canadians", "Ukrainians", "Yugoslavs",
    "Rusyn American", "Canadian Australian", "Bohemian People", "Luxembourgish Americans",
    "Armenians in Italy", "Baltic Russians", "Latvian Americans", "Ossetians",
    "Castilians", "Bulgarians", "Armenians of Russia", "Estonians", "Bosnians",
    "Manx people", "peoples of the Caucasus", "Romanians"
]


########################################################### Europe

# Caucasian/white
caucasian_ethnicities = [
    'Spaniards', 'Anglo-Celtic Australians', 'White Americans', 'Irish Americans',
    'Italian Americans', 'Slovak Americans', 'European Americans', 'Swedes',
    'Czech Americans', 'Dutch Americans', 'English Americans', 'Italians',
    'Hungarian Americans', 'White people', 'French', 'Australians',
    'Polish Americans', 'Germans', 'English people', 'Scottish Americans',
    'Spanish Americans', 'British', 'Croats', 'German Americans',
    'French Americans', 'Danes', 'Welsh people', 'Scottish people',
    'Australian Americans', 'Swiss', 'White British', 'Swedish Americans',
    'Danish Americans', 'Russian Americans', 'Lithuanian Americans',
    'Austrians', 'Bosnians', 'Norwegians', 'French Canadians',
    'Scottish Canadians', 'Croatian Americans', 'Icelanders',
    'Slovene Americans', 'Sicilian Americans', 'Finns', 'Dutch',
    'Austrian Americans', 'Ukrainian Americans', 'Swedish-speaking population of Finland',
    'Uruguayans', 'Anglo-Irish people', 'Portuguese', 'Scandinavian Americans',
    'Bulgarians', 'Greek Canadians', 'German Canadians', 'Greek Americans',
    'Norwegian Americans', 'Irish Canadians', 'Serbian Canadians', 'Galicians',
    'White Africans of European ancestry', 'Irish Australians', 'Italian Canadians',
    'Belarusians', 'Poles', 'Czechs', 'Welsh Americans', 'Latvians',
    'Serbs of Bosnia and Herzegovina', 'Serbs of Croatia', 'Austrians in the United Kingdom',
    'Corsicans', 'Greek Cypriots', 'Welsh Italians', 'Bulgarian Canadians',
    'Belgians', 'Serbian Australians', 'Albanians', 'Polish Canadians',
    'Basque people', 'Slavs', 'Aromanians', 'Transylvanian Saxons', 'Rusyn American',
    'Catalans', 'Italian Australians', 'Bolivian Americans', 'White Latin American',
    'Portuguese Americans', 'Ukrainians', 'Dalmatian Italians', 'Scotch-Irish Americans',
    'English Australian', 'Scottish Australians', 'Russians',
    'Canadians in the United Kingdom', 'British Americans', 'Kiwi', 'Serbs in the United Kingdom',
    'Croatian Australians', 'names of the Greeks', 'Bosniaks', 'Serbian Americans', 'Americans', 
    'Irish migration to Great Britain', 'Albanian Americans', 'Romanichal', 'Cajun'
]


# Arab/Middle Eastern
arab_ethnicities = [
    'Israelis', 'Lebanese people', 'Lebanese Americans', 'Sudanese Arabs',
    'Syrian Americans', 'Palestinians in the United States', 'Arab Americans',
    'Arabs in Bulgaria', 'Moroccans', 'Kurds', 'Azerbaijanis', 'Israeli Americans',
    'Lebanese people in the United Kingdom', 'Iranians in the United Kingdom',
    'Iranian peoples', 'Armenians of Russia', 'Assyrian people', 'Turkish Americans',
    'Armenians', 'Armenians in Italy', 'Armenian Americans', 'Copts'
]


# African/Black
african_ethnicities = [
    'African Americans', 'Ghanaian Americans', 'Sudanese Arabs', 'Somalis',
    'Afro Trinidadians and Tobagonians', 'Berber', 'Ghanaian', 'Black people',
    'Kabyle people', 'Mandinka people', 'Moroccans', 'Black Canadians',
    'Wolof people', 'African people', 'Xhosa people', 'Buryats', 'Malagasy people',
    'Haitian Americans', 'Yoruba people', 'Black Irish' , 'British Nigerian', 
    'Guyanese Americans', 'British Jamaicans', 'South African Americans', 
    'Louisiana Creole people', 'Chinese Jamaicans'
]


# South Asian
south_asian_ethnicities = [
    'Indian Americans', 'Indians', 'Sindhis', 'Tamil', 'British Indian',
    'Punjabis', 'Punjabi diaspora', 'Tamil Brahmin', 'Gujarati people',
    'Bengali', 'Bengali Brahmins', 'Indian diaspora in France',
    'Telugu people', 'Malayali', 'Pathani', 'Afghans in India',
    'Sri Lankan Tamil', 'Kayastha', 'Jaat', 'Kashmiri Pandit', 'Marathi people',
    'Hindu', 'Rohilla', 'Nair', 'Ezhava', 'Mudaliar', 'Kanyakubja Brahmins',
    'Chitrapur Saraswat Brahmin', 'Niyogi', 'Bunt (RAJPUT)', 'Sikh', 'Parsi',
    'Indo-Canadians', 'Marwari people'
]


# East Asian
east_asian_ethnicities = [
    'Japanese Americans', 'Chinese Americans', 'Manchu', 'British Chinese',
    'Chinese Singaporeans', 'Hongkongers', 'Taiwanese people', 'Koreans',
    'Korean Americans', 'Taiwanese Americans', 'Chinese Canadians',
    'Chinese Filipino', 'Ryukyuan people', 'Tibetan people'
]


# Southeast Asian
southeast_asian_ethnicities = [
    'Malaysian Chinese', 'Singaporeans', 'Thai Americans', 'Thai Chinese',
    'Vietnamese Americans', 'Vietnamese people', 'Filipino people',
    'Filipino Americans', 'Filipino Australians', 'Cambodian Americans',
    'Samoan Americans', 'Pacific Islander Americans'
]


# Latino/Hispanic
latino_ethnicities = [
    'Mexican Americans', 'Puerto Ricans', 'Latin American British', 'Venezuelan Americans',
    'Cuban Americans', 'Uruguayans', 'Mexicans', 'Hispanic and Latino Americans',
    'Argentines', 'Dominican Americans', 'Venezuelans', 'Hispanic',
    'Panamanian Americans', 'Castilians', 'Chileans', 'Chileans in the United Kingdom',
    'Peruvians in the United Kingdom', 'Latino', 'French Chilean', 'Italian Brazilians',
    'Criollo people', 'Colombian Americans', 'Colombian Australian', 'Stateside Puerto Ricans',
    'Cubans', 'Hondurans'
]


# Indigenous Peoples
indigenous_ethnicities = [
    'Apache', 'Mohawk', 'Blackfoot Confederacy', 'Cherokee',
    'Indigenous peoples of the Americas', 'Native Americans in the United States',
    'First Nations', 'Native Hawaiians', 'Aboriginal Australians', 'Māori',
    'Ojibwe', 'Dene', 'Malagasy people', 'Gin people', 'Sámi people'
]


# Jewish
jewish_ethnicities = [
    'Jewish people', 'British Jews', 'American Jews', 'Ashkenazi Jews',
    'Israeli Jews', 'Sephardi Jews', 'Moroccan Jews', 'Lithuanian Jews'
]


# Ethnicities that are not categorized due to being too broad
other_ethnicities = [
    'multiracial American', 'multiracial people', 'Eurasian', 'Q31340083'
]


#################################################### EA


# Define the chinese ethnicities
chinese_ethnicities = [
    "Chinese Americans", "Chinese Singaporeans", "British Chinese", "Malaysian Chinese", 
    "Chinese Canadians", "Thai Chinese", "Chinese Filipino", "Zhuang people", "Vietnamese Americans", 
]

taiwanese_ethnicities = [
    "Taiwanese people"
]
hong_kong_ethnicities = [
    "Hongkongers"
]

koreans_ethnicities = [
    "Koreans"
]

# Define the japanese ethnicities
japanese_ethnicities = [
    "Japanese Americans", "Ryukyuan people", "Asian people"
]

# Define the south asian ethnicities
other_asian_ethnicities = [
   "Indians", "Bihari people", "Parsi", "Malayali", "Eurasian", "Javanese"
]

# Define the european ethnicities 
european_ethnicities = [
    "Anglo-Irish people", "Welsh Italians", "Irish Americans", "English people",
    "Scottish people", "Italian Americans", "German Americans", "Hungarians", 
    "Spanish Americans", "names of the Greeks", "Portuguese", "Italians", "Germans", "White British",
    "British", "Irish migration to Great Britain", "Dutch", "Irish people",
    "Swedes", "French", "Scottish Americans", "Scandinavian Americans", "Dutch Americans",
    "Danish Americans", "Greek Americans", "Luxembourgish Americans",
    "Swedish Americans", "Albanian Americans", "Welsh people", "Cajun", "Honduras",
    "White people"
]

# Define the Americans ethnicities
american_ethnicities = [
    "Rusyn American", "Cherokee", "African Americans", "Ojibwe",
    "White Americans", "Canadian Americans", "Vietnamese Americans",
    "Asian Americans", "Jewish people", "British Americans", 
    "Hispanic and Latino Americans", "Ghanaian Americans", 
    "Mexican Americans", "Iranian Americans",
    "Latin American British", "multiracial American", "Native Hawaiians",
    "Québécois", "American Jews", "Indigenous peoples of the Americas", "Australians"
]

african_ethnicities = [
    "Akan people"
]

#############################################################3




# Standardize 'release' column to extract the correct year
def extract_year(release_date):
    try:
        # Attempt to convert to datetime and extract the year
        year = pd.to_datetime(release_date, errors='coerce').year
        if year is not pd.NaT:  # Check if the year is valid
            return year
        # If conversion fails, try extracting just the first 4 digits as year
        return int(str(release_date)[:4])
    except (ValueError, TypeError):
        return None  # Return None if extraction fails
    
########################################################
    
def compute_age_at_release(row):
    if pd.isna(row['age_at_release']) and pd.notna(row['release_y']) and pd.notna(row['actor_birth_year']):
        return row['release_y'] - row['actor_birth_year']
    return row['age_at_release']

###################################################

def extract_values_if_str_dict(value):
    """Parses string as a dictionary and extracts values if possible, otherwise returns the original value."""
    try:
        # Attempt to parse the string as a dictionary
        parsed_value = ast.literal_eval(value)
        if isinstance(parsed_value, dict):
            return list(parsed_value.values())
    except (ValueError, SyntaxError):
        # Return the original value if parsing fails
        return value
    
#####################################################

# Function to determine the cluster
def assign_cluster(countries):
    for country in countries:
        if country in hollywood_cluster:
            return 'Hollywood'
        elif country in indian_cluster:
            return 'Indian'
        elif country in east_asian_cluster:
            return 'EastAsian'
        elif country in european_cluster:
            return 'Europe'
    return 'Other'

###################################################


def map_main_genre(dataset, genre_column='genres', genre_mapping=GENRE_MAPPING, fallback_mappings=None):
    
    # Create reverse mapping from sub-genres to main genres
    sub_genre_to_main = {sub_genre: main_genre for main_genre, sub_genres in genre_mapping.items() for sub_genre in sub_genres}

    # Function to assign main genre based on sub-genres
    def assign_main_genre(genres):
        if not isinstance(genres, list) or len(genres) == 0:
            return "Other"  # Handle invalid or empty lists

        main_genre_counts = {}
        for sub_genre in genres:
            main_genre = sub_genre_to_main.get(sub_genre, "Other")
            main_genre_counts[main_genre] = main_genre_counts.get(main_genre, 0) + 1

        max_count = max(main_genre_counts.values())
        tied_genres = [genre for genre, count in main_genre_counts.items() if count == max_count]
        return sorted(tied_genres)[0] if tied_genres else "Other"

    # Apply main genre assignment to the specified column
    dataset.loc[:, 'main_genre'] = dataset[genre_column].apply(assign_main_genre)

    # Apply fallback mappings if provided
    if fallback_mappings:
        for mapping in fallback_mappings:
            dataset.loc[dataset['main_genre'] == "Other", 'main_genre'] = (
                dataset.loc[dataset['main_genre'] == "Other", genre_column]
                .apply(lambda x: reassign_genres(x, mapping))
            )

    return dataset


########################################################


def reassign_genres(genres, mapping):
    """Helper function to reassign genres using a specified mapping."""
    if not isinstance(genres, list):
        return "Other"

    for sub_genre in genres:
        if sub_genre in mapping:
            return mapping[sub_genre]
    return "Other"

###########################################################

def plot_top_ethnicities(dataframe, ethnicity_column='actor_ethnicity_label', region_name='Region'):
    # Count the occurrences of each ethnicity, excluding 'Unknown'
    ethnicity_counts = dataframe[dataframe[ethnicity_column] != 'Unknown'][ethnicity_column].value_counts()

    # Select the top 10 most frequent ethnicities
    top_ethnicities = ethnicity_counts.head(10)

    # Create a DataFrame to use 'hue'
    top_ethnicities_df = top_ethnicities.reset_index()
    top_ethnicities_df.columns = ['Ethnicity', 'Count']

    # Plotting the distribution using a bar chart
    plt.figure(figsize=(14, 8))
    sns.barplot(data=top_ethnicities_df, x='Ethnicity', y='Count', palette='viridis', hue='Ethnicity', dodge=False, legend=False)
    plt.title(f'Top 10 Most Frequent Ethnicities in Characters Dataset ({region_name})', fontsize=18)
    plt.xlabel('Ethnicity', fontsize=14)
    plt.ylabel('Number of Actors', fontsize=14)
    plt.xticks(rotation=30, ha='right', fontsize=12)
    plt.yticks(fontsize=12)
    sns.despine()
    plt.tight_layout()
    plt.show()


#################################################################

def classify_actor_ethnicity_europe(df):  
    df = df.copy()  # Create a copy to avoid modifying the original DataFrame
    df.loc[:, "actor_ethnicity_classification"] = df["actor_ethnicity_label"].apply(
        lambda x: "Caucasians" if x in caucasian_ethnicities else (
            "Arabs / Middle Easterns" if x in arab_ethnicities else (
                "Africans" if x in african_ethnicities else (
                    "South Asians" if x in south_asian_ethnicities else (
                        "East Asians" if x in east_asian_ethnicities else (
                            "Southeast Asian" if x in southeast_asian_ethnicities else (
                                "Latinos" if x in latino_ethnicities else (
                                    "Indigenous People" if x in indigenous_ethnicities else (
                                        "Jewish People" if x in jewish_ethnicities else 'Unkown'
                                    )
                                )
                            )
                        )
                    )
                )
            )
        )
    )
    return df



####################################################

# Real-world

####################################################

def process_ethnic_group_data(df):
    
    # Combine 'from' and 'to' columns into a new column 'from to'
    df.loc[:, "from to"] = df["from"].astype(str) + "-" + df["to"].astype(str)
    
    # Group by 'from to', 'group', and 'size', then count occurrences
    grouped_data = df.groupby(['from to', 'group', 'size']).size()
    
    # Reset index to convert groupings to columns
    df = grouped_data.reset_index(name='counts')   
    return df


####################################################

def process_grouped_averages_by_columns(df, group_col, drop_cols=None, decimals=2):
    
    # Drop specified columns if provided
    if drop_cols:
        drop_cols = [drop_cols] if isinstance(drop_cols, str) else drop_cols
        df = df.drop(columns=drop_cols, errors='ignore')

    # Select numeric columns only
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    
    # Group by the specified column and calculate the mean for numeric columns
    grouped_averages = (
        df.groupby(group_col)[numeric_cols]
        .mean()
        .reset_index()
    )

    # Round the averages to the specified number of decimals
    grouped_averages = grouped_averages.round(decimals)

    return grouped_averages

#########################################################

# Function to count regions and assign the biggest one
def assign_region(countries):
    # Ensure input is a list; if a string, convert it to a list
    if isinstance(countries, str):
        countries = [countries]
    
    # Initialize counts for each region
    region_counts = {'east_europe': 0, 'west_europe': 0, 'nordic_europe': 0}
    
    # Count the occurrence of each region
    for country in countries:
        region = country_to_region.get(country)
        if region:
            region_counts[region] += 1
    
    # Find the region with the maximum count
    max_count = max(region_counts.values())
    # Get all regions that have the maximum count
    regions_with_max_count = [region for region, count in region_counts.items() if count == max_count]
    
    # If there's a tie, pick the first in alphabetical order
    return sorted(regions_with_max_count)[0] if max_count > 0 else "Unknown"


#####################################################

def calculate_proportions(realworld_averages, bothsexes_averages):
    """
    Calculate proportions of a specific gender compared to both sexes.

    Parameters:
    - realworld_averages: DataFrame containing averages for a specific gender.
    - bothsexes_averages: DataFrame containing averages for both sexes.

    Returns:
    - DataFrame with calculated proportions.
    """
    proportions = realworld_averages.copy()
    proportions.iloc[:, 1:] = (
        realworld_averages.iloc[:, 1:].values /
        bothsexes_averages.iloc[:, 1:].values
    )
    return proportions

#####################################################

def classify_actor_ethnicity_indian(df):  
    df["actor_ethnicity_classification"] = df["actor_ethnicity_label"].apply(
        lambda x: "South_Indian_Ethnicities" if x in South_Indian_Ethnicities else (
            "North_Indian_Ethnicities" if x in North_Indian_Ethnicities else (
                "Eastern_Indian_Ethnicities" if x in Eastern_Indian_Ethnicities else (
                    "Western_and_Central_Indian_Ethnicities" if x in Western_and_Central_Indian_Ethnicities else (
                        "Religious_and_Caste_Groups" if x in Religious_and_Caste_Groups else None
                    )
                )
            )
        )
    )
    return df


######################################################

def classify_actor_ethnicity_hollywood(df):  
    df["actor_ethnicity_classification"] = df["actor_ethnicity_label"].apply(
        lambda x: "African Americans" if x in african_american_ethnicities else (
            "American Indians" if x in american_indian_ethnicities else (
                "Arab Americans" if x in arab_american_ethnicities else (
                    "Asian Americans" if x in asian_american_ethnicities else (
                        "Latino Americans" if x in latino_ethnicities else (
                            "Jewish Americans" if x in jewish_american_ethnicities else (
                                "Caucasian Americans" if x in caucasian_american_ethnicities else None
                            )
                        )
                    )
                )
            )
        )
    )
    return df


########################################################

def classify_actor_ethnicity_ea(df):  
    df["actor_ethnicity_classification"] = df["actor_ethnicity_label"].apply(
        lambda x: "Chinese" if x in chinese_ethnicities else (
            "Hongkongers" if x in hong_kong_ethnicities else (
                "Koreans" if x in koreans_ethnicities else (
                    "Japanese" if x in japanese_ethnicities else (
                        "Other Asians" if x in other_asian_ethnicities else (
                            "Europeans" if x in european_ethnicities else (
                                "Taiwanese" if x in taiwanese_ethnicities else (
                                "Americans" if x in american_ethnicities else None
                            )
                        )
                    )
                )
            )
        )
    )
    )
    return df


##########################################################3

