## This collects emotion from the cyanite api so that we get the emotion vectors


from python_graphql_client import GraphqlClient
import pandas as pd
from requests.auth import AuthBase
import json
## clean this up.
class BearerAuth(AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["Authorization"] = f"Bearer {self.token}"
        return r


# Instantiate the client with an endpoint.
client = GraphqlClient(endpoint="https://api.cyanite.ai/graphql")



token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiSW50ZWdyYXRpb25BY2Nlc3NUb2tlbiIsInZlcnNpb24iOiIxLjAiLCJpbnRlZ3JhdGlvbklkIjo0MzYsInVzZXJJZCI6MTkxMjUsImFjY2Vzc1Rva2VuU2VjcmV0IjoiODNlNGY1M2QxZmNkNmNjMzk0YzZjYzYxN2UwZjMzNmE4NTAxNzQ1ZDk2ODZlMjczYzIxMTZmNzlmZDhhMDBlZCIsImlhdCI6MTY3NDA5ODE1N30.gUE-BzTVJ3g73otcsU5NFO40OoMQ-0dDlPYbcIoMfTg"
auth = BearerAuth(token)

feature_matrix = pd.read_csv('feature_matrix.csv').drop('Unnamed: 0',axis=1) ## holds the song id and emotion


## gets the dictionary format of all features from the cyanide API 
def get_tags(input_song, the_feature,second_feature=False):
# Create the query string and variables required for the request.
    query = """
    query LibraryTrackQuery($libraryTrackId: ID!) {

    spotifyTrack(id: $libraryTrackId) {
        __typename
        ... on SpotifyTrackError{
        message
        }
        ... on SpotifyTrack {
        id
        title

            
        
    
    audioAnalysisV6 {
            __typename
            ... on AudioAnalysisV6Finished {
            result {
                valence
                arousal
                energyLevel
                energyDynamics
                emotionalProfile
                emotionalDynamics
                voicePresenceProfile
                predominantVoiceGender
                voice {
                female
                male
                instrumental
                }
                voiceTags
                musicalEraTag
                classicalEpochTags
                classicalEpoch {
                middleAge
                renaissance
                baroque
                classical
                romantic
                contemporary
                }

                genre {
              ambient
              blues
              classical
              electronicDance
              folkCountry
              funkSoul
              jazz
              latin
              metal
              pop
              rapHipHop
              reggae
              rnb
              rock
              singerSongwriter
            }
            genreTags
            advancedGenre {
              afro
              ambient
              arab
              asian
              blues
              childrenJingle
              classical
              electronicDance
              folkCountry
              funkSoul
              indian
              jazz
              latin
              metal
              pop
              rapHipHop
              reggae
              rnb
              rock
              singerSongwriters
              sound
              soundtrack
              spokenWord
            }
        
                instrumentTags
                advancedInstrumentTags
                mood {
                aggressive
                calm
                chilled
                dark
                energetic
                epic
                happy
                romantic
                sad
                scary
                sexy
                ethereal
                uplifting
                }
                moodTags
                moodMaxTimes {
                mood
                start
                end
                }
                moodAdvanced {
                anxious
                barren
                cold
                creepy
                dark
                disturbing
                eerie
                evil
                fearful
                mysterious
                nervous
                restless
                spooky
                strange
                supernatural
                suspenseful
                tense
                weird
                aggressive
                agitated
                angry
                dangerous
                fiery
                intense
                passionate
                ponderous
                violent
                comedic
                eccentric
                funny
                mischievous
                quirky
                whimsical
                boisterous
                boingy
                bright
                celebratory
                cheerful
                excited
                feelGood
                fun
                happy
                joyous
                lighthearted
                perky
                playful
                rollicking
                upbeat
                calm
                contented
                dreamy
                introspective
                laidBack
                leisurely
                lyrical
                peaceful
                quiet
                relaxed
                serene
                soothing
                spiritual
                tranquil
                bittersweet
                blue
                depressing
                gloomy
                heavy
                lonely
                melancholic
                mournful
                poignant
                sad
                frightening
                horror
                menacing
                nightmarish
                ominous
                panicStricken
                scary
                concerned
                determined
                dignified
                emotional
                noble
                serious
                solemn
                thoughtful
                cool
                seductive
                sexy
                adventurous
                confident
                courageous
                resolute
                energetic
                epic
                exciting
                exhilarating
                heroic
                majestic
                powerful
                prestigious
                relentless
                strong
                triumphant
                victorious
                delicate
                graceful
                hopeful
                innocent
                intimate
                kind
                light
                loving
                nostalgic
                reflective
                romantic
                sentimental
                soft
                sweet
                tender
                warm
                anthemic
                aweInspiring
                euphoric
                inspirational
                motivational
                optimistic
                positive
                proud
                soaring
                uplifting
                }
                moodAdvancedTags
                movement {
                bouncy
                driving
                flowing
                groovy
                nonrhythmic
                pulsing
                robotic
                running
                steady
                stomping
                }
                movementTags
                character {
                bold
                cool
                epic
                ethereal
                heroic
                luxurious
                magical
                mysterious
                playful
                powerful
                retro
                sophisticated
                sparkling
                sparse
                unpolished
                warm
                }
                characterTags
            }
            }
        }
        
        
        }
    }







    
    }

    """

    if 'spotify' in input_song:
        input_song = input_song.split(':')[2]
    variables = { "libraryTrackId": input_song } 

    data = client.execute(query=query, variables=variables,auth=auth)
    ## just doing advanced moods for now 
    if second_feature:
        cleaned = data["data"]["spotifyTrack"]["audioAnalysisV6"]["result"][the_feature]
        second_cleaned = data["data"]["spotifyTrack"]["audioAnalysisV6"]["result"][second_feature]
        return {'id':input_song,**cleaned, **second_cleaned} ## combine two features into one matrix.

    cleaned = data["data"]["spotifyTrack"]["audioAnalysisV6"]["result"][the_feature]
    return cleaned 





## below is running this on our 'tracks' dataframe. 

def collect_cyanide(df,feature_one,feature_two):
    counter = 0 
    global feature_matrix
    print(df)
    for row_index in range(len(df)):
        try: 
            if len(feature_matrix)==0: ## if its an empty data_frame then this is the first row. 
                counter+=1
                print(counter)
                feature_matrix = pd.DataFrame(get_tags(df['uri'][row_index],feature_one,feature_two),index=[0])
            else:
                print(feature_matrix)
                feature_matrix = pd.concat([feature_matrix,pd.DataFrame(get_tags(df.iloc[row_index]['uri'],feature_one,feature_two),index=[0])])
            
            print(feature_matrix['id'])
    
        except Exception as e :
            print(type(e))    # the exception type
            print(e) 
            continue 

        if row_index%100 ==0:
                print(feature_matrix)
                feature_matrix.to_csv('feature_matrix.csv')
            
        
    return feature_matrix




# we run this to collect the cyanite features for all tracks in our dataset. 
 
# tracks = pd.read_csv('spotify_dataset.csv')
# tracks = tracks[(tracks['decade']!='60s')&(tracks['decade']!='70s')&(tracks['decade']!='80s') ]

# collect_cyanide(tracks,'mood','moodAdvanced')
