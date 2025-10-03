TESTING_STATE_SMALL = {
    "tables_random_populate": [
        {
            "name": "users",
            "num_records": 2,  # 10
        },
        {"name": "videos", "num_records": 2},
        {
            "name": "comments",
            "num_records": 10000,
        },
        {
            "name": "user_cookies",
            "num_records": 0,
        },
        {
            "name": "third_party_auth_users",
            "num_records": 0,
        },
        {
            "name": "third_party_auth_tokens",
            "num_records": 0,
        },
    ]
}

TESTING_STATE_SERVER_RESTART = {
    "tables_random_populate": [
        {
            "name": "users",
            "num_records": 2,  # 10
        },
        {"name": "videos", "num_records": 2},
        {
            "name": "comments",
            "num_records": 10000,
        },
        {
            "name": "user_cookies",
            "num_records": 1,
        },
        {
            "name": "third_party_auth_users",
            "num_records": 0,
        },
        {
            "name": "third_party_auth_tokens",
            "num_records": 0,
        },
    ]
}

TESTING_STATE_FULL = {
    "tables_random_populate": [
        {
            "name": "users",
            "num_records": 10,
        },
        {
            "name": "videos",
            "num_records": 5,
        },
        {
            "name": "comments",
            "num_records": 10000,
        },
        # Add more tables as needed
    ]
}


TESTING_STATE_USERS_ONLY = {
    "tables_random_populate": [
        {
            "name": "users",
            "num_records": 5,
        },
    ]
}
