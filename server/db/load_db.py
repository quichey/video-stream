import db.Schema as Schema
import db.Seed.Seed as Seed

# This is the unifying script that will use DB_SCHEMA.py in conjunction with Seed.py
# To initiate the state of this specific video-stream web-app

# Think about how I intend to use this script
# -- the different programs/options to run this script
# -- and then plan out the functions/fields/etc

seed = Seed.Seed(Schema.admin_specs, Schema.database_specs, Schema)

testing_state = {
    "tables_random_populate": [
        {
            "name": "users",
            "num_records": 2, #10
        },
        {
            "name": "videos",
            "num_records": 2
        },
        {
            "name": "comments",
            "num_records": 10000,
            #"num_records": 10000
        },
        
        #{
        #    "name": "comment_likes",
        #    "num_records": 10
        #},
    ]
}
testing_state_comments_only = {
    "tables_random_populate": [
        {
            "name": "comments",
            "num_records": 10000,
            #"num_records": 10000
        },
        
        #{
        #    "name": "comment_likes",
        #    "num_records": 10
        #},
    ]
}

def run():
    seed.initiate_test_environment(testing_state)