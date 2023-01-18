"""Action table for the edubot."""


ACTION_TABLE = {
    "greet":{
        "stage": 0,
        "action": "greet",
        "valid_response":"Hie {name}, Welcome back",
        "invalid_response":{
            "response_type": "text",
            "text":"Welcome to EduBot. Sign up to get started.\n\nWhat is your first name?"
        },
        "next_action_if_valid": "menu",
        "next_action_if_invalid": "register",
        "action_validator": "user_exists",
        "response_type": "text",
        "type": "single",
    },
    "register":{
        "stage": 1,
        "action": "register",
        "valid_response":"Welcome {name}, please enter your last name",
        "invalid_response":"I am sorry, I did not get that. Please enter your first name",
        "next_action_if_valid": "register",
        "next_action_if_invalid": "register",
        "action_validator": "register",
        "response_type": "text",
        "type": "single",
    },
    "menu": {
        "stage": 2,
        "action": "menu",
        "valid_response":"Menu",
        "invalid_response":"Invalid menu option",
        "next_action_if_valid": [
            "enroll",
            "courses",
            "assignments",
            "payments",
            "profile",
            "about",
            "help"
        ],
        "next_action_if_invalid": [
            "enroll",
            "courses",
            "assignments",
            "payments",
            "profile",
            "about",
            "help"
        ],
        "action_validator": "menu",
        "response_type": "interactive",
        "type": "multiple",
    },
    "courses": {
        "stage": 3,
        "action": "courses",
        "valid_response":"Courses",
        "invalid_response":"Invalid course option",
        "next_action_if_valid": "courses",
        "next_action_if_invalid": "courses",
        "action_validator": "courses",
        "response_type": "interactive",
        "type": "multiple",
    },
    "enroll": {
        "stage": 4,
        "action": "enroll",
        "valid_response":"Enroll",
        "invalid_response":"Invalid enroll option",
        "next_action_if_valid": "menu",
        "next_action_if_invalid": "enroll",
        "action_validator": "enroll",
        "response_type": "interactive",
        "type": "multiple",
    },
    "assignments": {
        "stage": 5,
        "action": "assignments",
        "valid_response":"Assignments",
        "invalid_response":"Invalid assignments option",
        "next_action_if_valid": "menu",
        "next_action_if_invalid": "assignments",
        "action_validator": "assignments",
        "response_type": "interactive",
        "type": "single",
    },

    "profile": {
        "stage": 6,
        "action": "profile",
        "valid_response":"Profile",
        "invalid_response":"Invalid profile option",
        "next_action_if_valid": "profile",
        "next_action_if_invalid": ["menu", "profile"],
        "action_validator": "profile",
        "response_type": "interactive",
        "type": "multiple",
    },
    "help": {
        "stage": 7,
        "action": "help",
        "valid_response":"Help",
        "invalid_response":"Invalid help option",
        "next_action_if_valid": "help",
        "next_action_if_invalid": "menu",
        "action_validator": "help",
        "response_type": "text",
        "type": "single",
    },
    "about": {
        "stage": 8,
        "action": "about",
        "valid_response":"About",
        "invalid_response":"Invalid about option",
        "next_action_if_valid": "about",
        "next_action_if_invalid": "menu",
        "action_validator": "about",
        "response_type": "text",
        "type": "single",
    },
    "payments": {
        "stage": 9,
        "action": "payments",
        "valid_response":"Payments",
        "invalid_response":"Invalid payments option",
        "next_action_if_valid": "payments",
        "next_action_if_invalid": ["menu", "payments"],
        "action_validator": "payments",
        "response_type": "text",
        "type": "multiple",
    },
}   