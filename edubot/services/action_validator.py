"""Action validator for the edubot."""
#pylint: disable=line-too-long
# pylint: disable=import-error
# pylint: disable=no-name-in-module
import re
import sys
import math
from io import BytesIO
import requests
from django.core.cache import cache
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from decouple import config
from courses.models import Course
from assignments.models import Assignment, PendingWork
from payments.models import Payment
from packages.models import Package
from users.serializers import UserSerializer
from users.models import User
from utils.helper_functions import (
    is_phone_number,
    payment_method
)


class ActionValidator(object):
    """Action validator for the edubot."""

    def __init__(self):
        """Initialize the action validator."""
        self.registry = {
            "greet": self.greet,
            "user_exists": self.user_exists,
            "register": self.registration,
            "menu": self.menu,
            "enroll": self.enroll,
            "assignments": self.assignments,
            "profile": self.profile,
            "courses": self.my_courses,
            "payments": self.payments,
            "help": self.help,
            "about": self.about,
        }
        self.pagination = config("PAGINATION_COUNT", cast=int, default=5)
        self.pending_work = None

    #pylint: disable=unused-argument
    def greet(self, phone_number, message=None, session=dict):
        """Greet the user."""
        user = User.objects.filter(phone_number=phone_number)
        if user.exists():
            cache.set(phone_number, {
                "state": "menu",
                "data": None
            }, 60*60*24)
            return {
                "is_valid": True,
                "data": None,
                "message": {
                    "response_type": "interactive",
                    "username": "Welcome back to EduBot. What would you like to do?",
                    "menu_name": "Main Menu",
                    "menu_items" :[
                        {"id": "enroll", "name": "Enroll", "description": "Enroll in a course"},
                        {"id": "courses", "name": "Courses", "description": "View your courses"},
                        {"id": "assignments", "name": "Assignments", "description": "Go to assignments"},
                        {"id": "payments", "name": "Payments", "description": "View your payments"},
                        {"id": "profile", "name": "Profile", "description": "View your profile"},
                        {"id": "help", "name": "Get Started", "description": "User guide"},
                        {"id": "about", "name": "About Us", "description": "Contact Us"},           
                    ]
                }
            }
        cache.set(phone_number, {
                "state": "greet",
                "data": None
            }, 60*60*24)
        return {
            "is_valid": False,
            "data": None,
            "message": {
                "response_type": "text",
                "text": "Welcome to EduBot. Sign up to get started.\n\nWhat is your first name?"
            }
        }       

    def user_exists(self, phone_number, message=None, session=dict, payload=dict):
        """Check if the user exists."""
        user = User.objects.filter(phone_number=phone_number)
        print("Session : ", session, "\n", phone_number, "->", message)
        if user.exists():
            cache.set(phone_number, {
                "state": "menu",
                "data": None
            }, 60*60*24)
            return {
                "is_valid": True,
                "data": None,
                "message": {
                    "response_type": "interactive",
                    "text": "What would you like to do?",
                    "username": f"{user.first().first_name} {user.first().last_name}",
                    "menu_name": "🏠 Main Menu",
                    "menu_items" :[
                        {"id": "enroll", "name": "Enroll", "description": "Enroll in a course"},
                        {"id": "courses", "name": "Courses", "description": "View your courses"},
                        {"id": "assignments", "name": "Assignments", "description": "Go to assignments"},
                        {"id": "payments", "name": "Payments", "description": "View your payments"},
                        {"id": "profile", "name": "Profile", "description": "View your profile"},
                        {"id": "help", "name": "Get Started", "description": "User guide"},
                        {"id": "about", "name": "About Us", "description": "Contact Us"},
                        
                    ]
                }
            }
        message = "Welcome to EduBot. Sign up to get started.\n\nWhat is your first name?"  if not user.exists() else ""
        return {
            "is_valid": user.exists(),
            "data": user.first() if user.exists() else None, 
            "message": {
                "response_type": "text",
                "text": message
            }
        }

    def registration(self, phone_number, message=None, session=dict, payload=dict):
        """Validate the registration action."""
        user = User.objects.filter(phone_number=phone_number)
        print("Session : ", session, "\n", phone_number, "->", message)
        if not user.exists():
            if session:
                if not session.get("data").get("password"):
                    session["data"]["password"] = phone_number
                if not session.get("data").get("phone_number"):
                    session["data"]["phone_number"] = phone_number
                if not session.get("data").get("username"):
                    session["data"]["username"] = phone_number

                if not session.get("data").get("role"):
                    session["data"]["role"] = "STUDENT"

                if not session["data"].get("first_name") and message:
                    regex_legal_name = r"^[a-zA-Z]+(([',. -][a-zA-Z ])?[a-zA-Z]*)*$"
                    if not re.match(regex_legal_name, message):
                        return {
                            "is_valid": False, 
                            "data": "Invalid first name",
                            "message": {
                                "response_type": "text",
                                "text": f"{message} is not a valid first name.\n\nPlease enter a valid first name",
                            }
                        }
                    session["data"]["first_name"] = message
                    message = None

                if not session["data"].get("last_name") and message:
                    regex_legal_name = r"^[a-zA-Z]+(([',. -][a-zA-Z ])?[a-zA-Z]*)*$"
                    if not re.match(regex_legal_name, message):
                        return {
                            "is_valid": False, 
                            "data": "Invalid last name",
                            "message":{
                                "response_type": "text",
                                "text": f"{message} is not a valid last name.\n\nPlease enter a valid last name"
                            }
                        }
                    session["data"]["last_name"] = message
                    message = None

                if not session["data"].get("email") and message:
                    email_address_regex = r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
                    print("Validating email address", re.match(email_address_regex, message))
                    if not re.match(email_address_regex, message):
                        return {
                            "is_valid": False,
                            "data": "Invalid email",
                            "message": {
                                "response_type": "text",
                                "text": f"{message} is not a valid email.\n\nPlease enter a valid email address"
                            }
                        }
                    else:
                        session["data"]["email"] = message
                    message = None
                cache.set(phone_number, session, 60*60*24)

                if not session["data"].get("sex") and message:
                    if message.title() not in ["Male", "Female", "Other"]:
                        return {
                            "is_valid": False,
                            "data": "Invalid sex",
                            "message": {
                                "response_type": "text",
                                "text": f"{message} should be Male or Female or Other.\n\nPlease enter your sex"
                            }
                        }
                    else:
                        session["data"]["sex"] = message.upper()
                    message = None
                cache.set(phone_number, session, 60*60*24)
        serializer = UserSerializer(data=session["data"])
        is_valid = serializer.is_valid()
        if not is_valid:
            message = serializer.errors[
                "non_field_errors"
                ][0].replace("ErrorDetail(string='", "").replace("', code='invalid')", "")
            print(message)
        else:
            serializer.save()
            message = f"Registration successful, thank you {serializer.data.get('first_name')} {serializer.data.get('last_name')} for registering with EduBot.\n\nPress *menu* to proceed to your account."
        return {
            "is_valid": is_valid,
            "data": serializer.data if is_valid else serializer.errors,
            "message": {
                "exclude_back": True,
                "response_type": "button" if is_valid else "text",
                "text": message,
            }
        }

    def menu(self, phone_number, message=None, session=dict, payload=dict):
        """Validate the menu action."""
        user = User.objects.filter(phone_number=phone_number)
        print("MENU SESSION : ", session, "\n", user, "->", message)
        if not user.exists():
            cache.set(phone_number, {
                "state": "register",
                "data": None
            }, 60*60*24)
            return {
                "is_valid": False,
                "data": "User does not exist",
                "message": {
                    "response_type": "text",
                    "text":"You are not registered with EduBot.  Sign up to get started.\n\nWhat is your first name?"
                }
            }
        cache.set(phone_number, {
            "state": "menu",
            "data": None
        }, 60*60*24)
        return {
            "is_valid": True,
            "data": user.first(),
            "message": {
                "response_type": "interactive",
                "text": "What would you like to do?",
                "username": f"{user.first().first_name} {user.first().last_name}",
                "menu_name": "🏠 Main Menu",
                "menu_items" :[
                    {"id": "enroll", "name": "Enroll", "description": "Enroll in a course"},
                    {"id": "courses", "name": "Courses", "description": "View your courses"},
                    {"id": "assignments", "name": "Assignments", "description": "Go to assignments"},
                    {"id": "payments", "name": "Payments", "description": "View your payments"},
                    {"id": "profile", "name": "Profile", "description": "View your profile"},
                    {"id": "help", "name": "Get Started", "description": "User guide"},
                    {"id": "about", "name": "About Us", "description": "Contact Us"},
                ]
            }
        }

    def enroll(self, phone_number, message=None, session=dict, payload=dict):
        """Validate the enroll action."""
        user = User.objects.filter(phone_number=phone_number)

        # pylint: disable=no-member
        courses = Course.objects.all()
        if cache.get(phone_number):
            session = cache.get(phone_number)

            if session.get("state") == "enroll":
                if session["data"].get("selected_course"):
                    if message in [i.name for i in Package.objects.all()]:
                        session["data"]["selected_package"] = message
                        cache.set(phone_number, session, 60*60*24)
                        return {
                            "is_valid": False,
                            "data": user.first(),
                            "message": {
                                "response_type": "interactive",
                                "text": f"Purchase {session['data']['selected_package'].title()} Package.",
                                "username": f"{user.first().first_name} {user.first().last_name}",
                                "menu_name": "💳 Purchase",
                                "menu_items" :[
                                    {
                                        "id": "paypal",
                                        "name": "PayPal",
                                        "description": "Complete purchase with PayPal",
                                    },
                                    {
                                        "id": "paynow",
                                        "name": "PayNow",
                                        "description": "Complete purchase with PayNow",
                                    },
                                ]
                            }
                        }
                    elif message == "paynow":
                        print("PAYNOW")
                        session["data"]["payment_method"] = "paynow"
                        cache.set(phone_number, session, 60*60*24)
                        return {
                            "is_valid": False,
                            "data": user.first(),
                            "message": {
                                "response_type": "text",
                                "text": "*PayNow*\n\nPlease enter the phone number you want to pay with\n\n*NB:* _The number should be registered with Ecocash or OneMoney._",
                            }
                        }
                    elif session["data"].get("payment_method") == "paynow" and  session["data"].get("paying_phone_number") is None:
                        if not is_phone_number(message):
                            return {
                                "is_valid": False,
                                "data": user.first(),
                                "message": {
                                    "response_type": "text",
                                    "text": f"*PayNow*\n\n{message} is not a valid number, please enter a valid phone number ",
                                }
                            }

                        if payment_method(message) in ["ecocash", "onemoney"] and message != "retry":
                            if message == "retry":
                                message = session["data"]["payee"]
                            session["data"]["payee"] = message
                            cache.set(phone_number, session, 60*60*24)
                            course=Course.objects.get(code=session["data"]["selected_course"])
                            package=Package.objects.get(name=session["data"]["selected_package"])
                            method=payment_method(message)
                            print(course, package, method)
                            #pylint: disable=no-value-for-parameter
                            payment = Payment.create_payment(
                                course=course,
                                package=package,
                                method=method,
                                user=user.first(),
                                payment_type=session["data"]["payment_method"],
                            )
                            print(payment)
                            response = Payment.send_payment_request(payment, message)
                            if response.get("status") == "Error":
                                print("ERROR==============>>>>", phone_number)
                                Payment.objects.filter(id=payment.id).update(payment_status="Declined")
                                
                                return {
                                    "is_valid": False,
                                    "data": user.first(),
                                    "message": {
                                        "response_type": "text",
                                        "text": f"*PayNow*\n\nFailed to process payment with error *{response.get('error')}*\n\nPlease try entering your phone number again.",
                                    }
                                }
                            # Initiate payment here
                            return {
                                "is_valid": False,
                                "data": user.first(),
                                "message": {
                                    "response_type": "text",
                                    "text": f"*PayNow*\n\nYour ${payment.amount} {payment_method(message).lower()} payment has been initiated. Please complete the payment on your handset on prompt.",
                                }
                            }
                        else:
                            return {
                                "is_valid": False,
                                "data": user.first(),
                                "message": {
                                    "response_type": "text",
                                    "text": f"*PayNow*\n\n{payment_method(message).title()} is not supported. Please enter a valid Ecocash or OneMoney phone number.",
                                }
                            }
                            

                        # pylint: disable=no-member
                        # course = Course.objects.get(code=session["data"]["selected_course"])
                        # student = User.objects.get(phone_number=phone_number)
                        # package = Package.objects.get(name=session["data"]["selected_package"])

                        # if student.enrolled_courses.filter(id=course.id).exists():
                        #     session["state"] = "menu"
                        #     session["data"] = {
                        #         "selected_course": None,
                        #         "selected_package": None,
                        #     }
                        #     cache.set(phone_number, session, 60*60*24)
                        #     return{
                        #         "is_valid": True,
                        #         "data": user.first(),
                        #         "message": {
                        #             "response_type": "interactive",
                        #             "text": "You are already enrolled in this course.\n\n What would you like to do?",
                        #             "username": f"{user.first().first_name} {user.first().last_name}",
                        #             "menu_name": "🏠 Main Menu",
                        #             "menu_items" :[
                        #                 {"id": "enroll", "name": "Enroll", "description": "Enroll in a course"},
                        #                 {"id": "courses", "name": "Courses", "description": "View your courses"},
                        #                 {"id": "assignment", "name": "Assignments", "description": "Go to assignments"},
                        #                 {"id": "payments", "name": "Payments", "description": "View your payments"},
                        #                 {"id": "profile", "name": "Profile", "description": "View your profile"},
                        #                 {"id": "help", "name": "Get Started", "description": "User guide"},
                        #                 {"id": "about", "name": "About Us", "description": "Contact Us"},
                        #             ]
                        #         }
                        #     }

                       


                        # Payment.objects.create(
                        #     user=student,
                        #     course=course,
                        #     amount=package.price,
                        #     package=package,
                        #     payment_status="Paid",
                        #     payment_type="PayPal"
                        # )
                        ############################################

                        # session["state"] = "menu"
                        # session["data"] = {
                        #     "selected_course": None,
                        #     "selected_package": None,
                        # }
                        return{
                            "is_valid": True,
                            "data": user.first(),
                            "message": {
                                "response_type": "text",
                                "text": "Please follow the link to complete your purchase.\n\nhttps://www.spotify.com/us/purchase/offer/premium-family/?country=US"
                            }
                        }

                    elif message == "paypal":
                        session["state"] = "menu"
                        session["data"] = {
                            "selected_course": None,
                            "selected_package": None,
                        }
                        cache.set(phone_number, session, 60*60*24)
                        return {
                            "is_valid": False,
                            "data": user.first(),
                            "message": {
                                "response_type": "interactive",
                                "text": "Purchase cancelled.",
                                "username": f"{user.first().first_name} {user.first().last_name}",
                                "menu_name": "🏠 Main Menu",
                                "menu_items" :[
                                    {"id": "enroll", "name": "Enroll", "description": "Enroll in a course"},
                                    {"id": "courses", "name": "Courses", "description": "View your courses"},
                                    {"id": "assignments", "name": "Assignments", "description": "Go to assignments"},
                                    {"id": "payments", "name": "Payments", "description": "View your payments"},
                                    {"id": "profile", "name": "Profile", "description": "View your profile"},
                                    {"id": "help", "name": "Get Started", "description": "User guide"},
                                    {"id": "about", "name": "About Us", "description": "Contact Us"},
                                ]
                            }
                        }
                    else:
                        return {
                            "is_valid": False,
                            "data": "Invalid selection",
                            "message": {
                                "response_type": "text",
                                "text": "Invalid selection.  Please try again."
                            }
                        }
                elif message in [course.code for course in courses]:
                    course = Course.objects.get(code=message)
                    session["data"]["selected_course"] = message
                    cache.set(phone_number, session, 60*60*24)
                    return {
                        "is_valid": False,
                        "data": user.first(),
                        "message": {
                            "response_type": "interactive",
                            "text": f"*Course:* {course.name}\n*Duration:* {course.duration} week(s)\n*Description:* {course.description}\n\n",
                            "username": f"{user.first().first_name} {user.first().last_name}",
                            "menu_name": "📦 Available Packages",
                            "menu_items" :[
                                {
                                    "id": package.name,
                                    "name": f"{package.name.title()} (${package.price})",
                                    "description": f"{package.description}",
                                } for package in Package.objects.all()
                            ]
                        }
                    }
                cache.set(phone_number, session, 60*60*24)
                return {
                    "is_valid": False,
                    "data": user.first(),
                    "message": {
                        "response_type": "interactive",
                        "text": "Select a course to enroll in.",
                        "username": f"{user.first().first_name} {user.first().last_name}",
                        "menu_name": "📚 Available Courses",
                        "menu_items" :[
                            {
                                "id": course.code,
                                "name": course.name,
                                "description": f"Course Code: {course.code}\nCourse Duration: {course.duration} week(s)",
                            } for course in Course.objects.all()
                        ]
                    }
                }
           
        session = {
            "state": "enroll",
            "data": {
                "page": 1,
                "total_pages": math.ceil(len(courses)/5),
                "selected_course": None
            }
        }
        cache.set(phone_number, session, 60*60*24)
        return {
            "is_valid": False,
            "data": user.first(),
            "message": {
                "response_type": "interactive",
                "text": "Select a course to enroll in.",
                "username": f"{user.first().first_name} {user.first().last_name}",
                "menu_name": "📚 Available Courses",
                "menu_items" :[
                    {
                        "id": course.code,
                        "name": course.name,
                        "description": f"Course Code: {course.code}\nCourse Duration: {course.duration} week(s)",
                    } for course in courses
                ]
            }
        } if courses else {
            "is_valid": False,
            "data": user.first(),
            "message": {
                "response_type": "text",
                "text": "Oops! No courses available at the moment.  Please try again later."
            }
        }

    def my_courses(self, phone_number, message, session, payload=dict):
        """My courses menu"""
        user = User.objects.filter(phone_number=phone_number)
        # pylint: disable=no-member
        courses = Course.objects.filter(students__in=user)
        base = []
        if session.get("data"):
            if session["data"].get("total_pages"):
                pass
        else:
            session["data"] = {
                "page": 1,
                "total_pages": math.ceil(len(courses)/self.pagination)
            }
        base =[]
        if message == "next":
            base = []
            session["data"]["page"] += 1
            cache.set(phone_number, session, 60*60*24)
            if session["data"]["page"] > 1:
                base.append({
                    "id": "previous",
                    "name": "Previous",
                    "description": "Previous page"
                })
            if session["data"]["page"] < session["data"]["total_pages"]:
                base.append({
                    "id": "next",
                    "name": "Next",
                    "description": "Next page"
                })
            return {
                "is_valid": True,
                "data": user.first(),
                "message": {
                    "response_type": "interactive",
                    "text": f"Your Enrolled Courses({session['data']['page']} of {session['data']['total_pages']}).",
                    "username": f"{user.first().first_name} {user.first().last_name}",
                    "menu_name": "📚 My Courses",
                    "menu_items" :[
                        {
                            "id": course.code,
                            "name": course.name,
                            "description": f"Course Code: {course.code}\nCourse Duration: {course.duration} week(s)",
                        } for course in courses[session["data"]["page"]*self.pagination-self.pagination:session["data"]["page"]*self.pagination]
                    ] + base
                }
            }       
        elif message == "previous":
            base = []
            if session["data"]["page"] > 1:
                session["data"]["page"] -= 1
                cache.set(phone_number, session, 60*60*24)
            
            if session["data"]["page"] > 1:
                base.append({
                    "id": "previous",
                    "name": "Previous",
                    "description": "Previous page"
                })
            
            print("\n\nSESSION : ", session["data"], session["data"]["page"] , session["data"]["total_pages"], session["data"]["page"] < session["data"]["total_pages"])
            if session["data"]["page"] < session["data"]["total_pages"]:
                base.append({
                    "id": "next",
                    "name": "Next",
                    "description": "Next page"
                })
                return {
                    "is_valid": True,
                    "data": user.first(),
                    "message": {
                        "response_type": "interactive",
                        "text": f"Your Enrolled Courses({session['data']['page']} of {session['data']['total_pages']})",
                        "username": f"{user.first().first_name} {user.first().last_name}",
                        "menu_name": "📚 My Courses",
                        "menu_items" :[
                            {
                                "id": course.code,
                                "name": course.name,
                                "description": f"Course Code: {course.code}\nCourse Duration: {course.duration} week(s)",
                            } for course in courses[session["data"]["page"]*self.pagination-self.pagination:session["data"]["page"]*self.pagination]
                        ]+ base
                    }
                }
            return {
                "is_valid": False,
                "data": user.first(),
                "message": {
                    "response_type": "button",
                    "text": "You are already on the first page."
                }
            }
        else:
            if not session["data"].get("selected_course") and message not in [i.code for i in courses]:
                session = {
                    "state": "my_courses",
                    "data": {
                        "page": 1,
                        "total_pages": math.ceil(len(courses)/self.pagination),
                        "selected_course": None
                    }
                }
                cache.set(phone_number, session, 60*60*24)
                if session["data"]["page"] > 1:
                    base.append({
                        "id": "previous",
                        "name": "Previous",
                        "description": "Previous page"
                    })
                if session["data"]["page"] < session["data"]["total_pages"]:
                    base.append({
                        "id": "next",
                        "name": "Next",
                        "description": "Next page"
                    })
                menu_items =[
                    {
                        "id": course.code,
                        "name": course.name,
                        "description": f"Course Code: {course.code}\nCourse Duration: {course.duration} week(s)",
                    } for course in courses[session["data"]["page"]*self.pagination-self.pagination:session["data"]["page"]*self.pagination]
                ]
                if base and menu_items and courses.count() > self.pagination:
                    menu_items.extend(base)
                return {
                    "is_valid": True,
                    "data": user.first(),
                    "message": {
                        "response_type": "interactive",
                        "text": f"Your Enrolled Courses({session['data']['page']} of {session['data']['total_pages']}).",
                        "username": f"{user.first().first_name} {user.first().last_name}",
                        "menu_name": "📚 My Courses",
                        "menu_items" :menu_items
                    }
                } if courses else {
                    "is_valid": False,
                    "data": user.first(),
                    "message": {
                        "response_type": "text",
                        "text": "Oops! You are not enrolled in any course at the moment.  Please try again later.",
                    }
                }
            else:
                if message in [i.code for i in courses]:
                    session["data"]["selected_course"] = message
                    cache.set(phone_number, session, 60*60*24)
                    course = Course.objects.get(code=message)
                    return {
                        "is_valid": True,
                        "data": user.first(),
                        "message": {
                            "response_type": "interactive",
                            "text": "Course Menu",
                            "username": f"{user.first().first_name} {user.first().last_name}",
                            "menu_name": f"📚 {course.name}",
                            "menu_items" :[
                                {
                                    "id": "course_outline",
                                    "name": "Course Outline",
                                    "description": "Course Outline"
                                },
                                {
                                    "id": "tutorial",
                                    "name": "Tutorial",
                                    "description": "Course Tutorial"
                                },
                                {
                                    "id": "course_material",
                                    "name": "Course Material",
                                    "description": "Course Material"
                                },
                                {
                                    "id": "course_assessment",
                                    "name": "Course Assessment",
                                    "description": "Course Assessment"
                                },
                                {
                                    "id": "back",
                                    "name": "Back",
                                    "description": "Back to courses"
                                },
                            ]
                        }
                    }
                else:
                    # TODO: Handle back button
                    # TODO: Handle course operations
                    pass

    def profile(self, phone_number, message, session, payload=dict):
        """Profile menu"""
        user = User.objects.filter(phone_number=phone_number)

        if message == "update":
            session = {
                "state": "update_profile",
                "data": {
                    "first_name": user.first().first_name,
                    "last_name": user.first().last_name,
                    "email": user.first().email,
                    "phone_number": user.first().phone_number,
                    "done": False
                }
            }
            cache.set(phone_number, session, 60*60*24)
        
        if user.first().sex == "MALE":
            imo = '🤵🏽‍♂'
        elif user.first().sex == "FEMALE":
            imo = '🤵🏽‍♀'
        else:
            imo = '🤵🏽'

        return {
            "is_valid": True,
            "data": user.first(),
            "message": {
                "response_type": "interactive",
                "text": f"*Your Profile*\n\n*Email:* {user.first().email}\n*Phone Number:* {user.first().phone_number}\n*Name: _{user.first().first_name} {user.first().last_name}_*\n*Sex: _{user.first().sex.title()}_*",
                "username": f"{user.first().first_name} {user.first().last_name}",
                "menu_name": f"{imo} Profile",
                "menu_items" :[
                    {"id": "deactivate", "name": "Deactivate Profile", "description": "Suspend your profile"},
                    {"id": "menu", "name": "Main Menu", "description": "Back To Menu"},
                ]
            }
        }

    def help(self, phone_number, message, session, payload=dict):
        """Help menu"""
        user = User.objects.filter(phone_number=phone_number)
        print(message, session)
        if message == "guide":
            return {
                "is_valid": True,
                "data": user.first(),
                "message": {
                    "response_type": "button",
                    "text": "EduBot is a chatbot that helps you to manage your courses and profile.\n\n1. Follow the instructions to register.\n2. Type *menu* to get started.\n3. Enroll in a course.\n4. Manage your profile.\n5. Enjoy Learning!\n\nAt any point, you can type *menu* to get back to your main menu.\n\n",
                }
            }
        elif message == "contact":
            return {
                "is_valid": True,
                "data": user.first(),
                "message": {
                    "response_type": "button",
                    "text": "You can contact the developer via email: *[developer@edubot.com]*",
                }
            }
        return {
            "is_valid": True,
            "data": user.first(),
            "message": {
                "response_type": "interactive",
                "text": "Help Menu",
                "username": f"{user.first().first_name} {user.first().last_name}",
                "menu_name": "🆘 Help",
                "menu_items" :[
                    {"id": "guide", "name": "User guide", "description": "User guide"},
                    {"id": "contact", "name": "Contact", "description": "Contact the developer"},
                ]
            }
        }

    def about(self, phone_number, message, session, payload=dict):
        """About menu"""
        user = User.objects.filter(phone_number=phone_number)
        print(message, session)
        return {
            "is_valid": True,
            "data": user.first(),
            "message": {
                "exclude_back": True,
                "response_type": "button",
                "text": "EduBot is a chatbot that helps you to manage your courses and profile brought to you by Empart.\n\nFor more information, visit *[https://edubot.com]* \nor contact \n*[https://wa.me/2627767646]*",
            }
        }

    def payments(self, phone_number, message, session, payload=dict):
        """Payment menu"""
        user = User.objects.filter(phone_number=phone_number)
        #pylint: disable=maybe-no-member
        payments = Payment.objects.filter(user=user.first()).order_by("-created_at")[:7]
        if not session["data"]:
            session["data"] = {}

        if message in [str(payment.id) for payment in payments]:
            payment = Payment.objects.get(id=message)
            return {
                "is_valid": True,
                "data": user.first(),
                "message": {
                    "response_type": "button",
                    "text": f"*Payment Details*\n\n*Course: _{payment.course.name}_*\n*Amount:* ${payment.amount}\n*Date:* _{payment.created_at.strftime('%d %b %Y')}_\n*Status:* _{payment.payment_status}_\n*Package:* _{payment.package.name.title()}_\n\n",
                }
            }
        if payments:
            return {
                "is_valid": True,
                "data": user.first(),
                "message": {
                    "response_type": "interactive",
                    "text": "*Your Recent Payments*\n\n",
                    "username": f"{user.first().first_name} {user.first().last_name}",
                    "menu_name": "💰 Payments",
                    "menu_items" :[
                        {"id": f"{payment.id}", "name": f"{payment.course.name}", "description": f"{payment.created_at.strftime('%d %b %Y %H:%M')}"} for payment in payments
                    ]

                }
            }

            
        else:
            return {
                "is_valid": True,
                "data": user.first(),
                "message": {
                    "response_type": "button",
                    "text": "You have not made any payments yet.",
                }
            }
      
    def assignments(self, phone_number, message, session, payload=dict):
        """Assignment menu"""
        user = User.objects.get(phone_number=phone_number)
        #pylint: disable=maybe-no-member
        pending_work = PendingWork.objects.filter(course__students__in=[user]).exclude(submitted_assignments__submitted_by=user).order_by("-created_at")
        session = cache.get(f"{phone_number}_session", {"data": {}})
        if message in [str(work.id) for work in pending_work]:
            session["data"]["assignment_id"] = message
            cache.set(f"{phone_number}_session", session)
            work = PendingWork.objects.get(id=message)
            return {
                "is_valid": False,
                "data": user,
                "message": {
                    "response_type": "download",
                    "text": f"*{work.title} Details*\n\n*Course: _{work.course.name}_*\n*Deadline:* _{work.deadline.strftime('%d %b %Y %H:%M') if  work.deadline else 'No deadline'}_\n*Description:* _{work.description}_\n\n",
                }
            }
        elif message == "download":
            work = PendingWork.objects.get(id=session["data"]["assignment_id"])
            return {
                "is_valid": False,
                "data": user,
                "message": {
                    "response_type": "document",
                    "caption": f"*{work.title} Details*\n\n*Course: _{work.course.name}_*\n*Deadline:* _{work.deadline.strftime('%d %b %Y %H:%M') if  work.deadline else 'No deadline'}_\n*Description:* _{work.description}_\n\n",
                    "url": settings.NGROK + work.file.url,
                    "filename": work.file.name
                }
            }
        elif message == "upload":
            session["data"]["action"] = message
            cache.set(f"{phone_number}_session", session)
            return {
                "is_valid": False,
                "data": user,
                "message": {
                    "response_type": "text",
                    "text": "Please upload and send your assignment as a document."
                }
            }
        elif session["data"].get("action") == "upload":
            
            try:
                url_regex = re.compile(
                    r'^(?:http|ftp)s?://' # http:// or https://
                    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
                    r'localhost|' #localhost...
                    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
                    r'(?::\d+)?' # optional port
                    r'(?:/?|[/?]\S+)$', re.IGNORECASE)
                if url_regex.match(message):
                    file = requests.get(url=message, headers={
                                    'Authorization': f"Bearer {config('CLOUD_API_TOKEN')}"})
                    bytesio_o = BytesIO(file.content)

                    obj = InMemoryUploadedFile(
                        file=bytesio_o,
                        field_name='file',
                        name=payload.get("filename"),
                        content_type=file.headers.get("content-type"),
                        size=sys.getsizeof(bytesio_o),
                        charset="Unicode - UTF8"
                    )
                    #pylint: disable=no-member
                    work = PendingWork.objects.get(id=session["data"]["assignment_id"])
                    asignment = Assignment.objects.create(
                        title=f"{work.title} - {user.first_name} {user.last_name}",
                        file=obj,
                        status="Completed",
                        referenced_work=work,
                        submitted_by=user
                    )
                    work.submitted_assignments.add(asignment)
                    work.save()
                    session["data"]["action"] = None
                    cache.set(f"{phone_number}_session", session)
                    return {
                        "is_valid": True,
                        "data": user,
                        "message": {
                            "exclude_back": True,
                            "response_type": "button",
                            "text": "Your assignment has been submitted successfully.",
                        }
                    }
                else:
                    return {
                        "is_valid": False,
                        "data": user,
                        "message": {
                            "response_type": "text",
                            "text": "Please upload and send your assignment as a document."
                        }
                    }
            #pylint: disable=broad-except
            except Exception:
                return {
                    "is_valid": False,
                    "data": user,
                    "message": {
                        "exclude_back": True,
                        "response_type": "button",
                        "text": "There was an error while processing your request. Please try again.",
                    }
                }
        elif message == "my_assignments":
            # filter pending work if user is enrolled in the course and user not in the list of submitted assignments
            if pending_work:
                return {
                    "is_valid": False,
                    "data": user,
                    "message": {
                        "response_type": "interactive",
                        "text": "*Pending Assignments*\n\n",
                        "username": f"{user.first_name} {user.last_name}",
                        "menu_name": "📝 Pending",
                        "menu_items" :[
                            {"id": f"{work.id}", "name": f"{work.course.name}", "description": f"Due {work.deadline.strftime('%d %b %Y %H:%M') if  work.deadline else 'No deadline'}"} for work in pending_work
                        ]

                    }
                }
            return {
                "is_valid": False,
                "data": user,
                "message": {
                    "response_type": "button",
                    "text": "You have not been assigned any assignments yet. Please check back later.",
                }
            }  
        elif message == "get_help":
            session["data"]["action"] = message
            cache.set(f"{phone_number}_session", session)
            return {
                "is_valid": False,
                "data": user,
                "message": {
                    "response_type": "interactive",
                    "text": "Assignments Help Menu",
                    "username": f"{user.first_name} {user.last_name}",
                    "menu_name": "📝 Get Help",
                    "menu_items" :[
                        {"id": "outsource", "name": "Upload Assignment", "description": "Upload your assignment"},
                        {"id": "pending", "name": "View Pending", "description": "View pending assignments"},
                        {"id": "back", "name": "Back", "description": "Back to assignments menu"},
                    ]
                }
            }
        elif session["data"].get("action") == "get_help" and message == "outsource":
            session["data"]["action"] = "receive_assignment"
            cache.set(f"{phone_number}_session", session)
            return {
                "is_valid": False,
                "data": user,
                "message": {
                    "response_type": "text",
                    "text": "Please upload and send your assignment document and we will get back to you."
                }
            }     
        elif session["data"].get("action") == "receive_assignment":
            # try:
            url_regex = re.compile(
                r'^(?:http|ftp)s?://' # http:// or https://
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
                r'localhost|' #localhost...
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
                r'(?::\d+)?' # optional port
                r'(?:/?|[/?]\S+)$', re.IGNORECASE)
            if url_regex.match(message):
                file = requests.get(url=message, headers={
                                'Authorization': f"Bearer {config('CLOUD_API_TOKEN')}"})
                bytesio_o = BytesIO(file.content)

                obj = InMemoryUploadedFile(
                    file=bytesio_o,
                    field_name='file',
                    name=payload.get("filename"),
                    content_type=file.headers.get("content-type"),
                    size=sys.getsizeof(bytesio_o),
                    charset="Unicode - UTF8"
                )
                assignment = Assignment.objects.create(

                    assignment_type="Outsourced",
                    status="Pending",
                    submitted_by=user,
                    file=obj

                )
                payment = Payment.objects.create(
                    user=user,
                    amount=0,
                    assignment=assignment,
                    payment_type="Outsource",
                    status="Awaiting Payment"
                )
                assignment.payment = payment
                assignment.save()

                session["data"]["action"] = "pending_payment"
                cache.set(f"{phone_number}_session", session)
                return {
                    "is_valid": True,
                    "data": user,
                    "message": {
                        "exclude_download": True,
                        "response_type": "pay_download",
                        "id": payment.id,
                        "text": f"We have received your assignment referenced as Assignment {assignment.id}.\nPlease note that you will be charged a fee for this service. Complete the payment process so we can start working on it.\n\nThank you for using our service.",
                    }
                }
            else:
                return {
                    "is_valid": False,
                    "data": user,
                    "message": {
                        "response_type": "text",
                        "text": "Please upload and send your assignment as a document."
                    }
                }
        elif session["data"].get("action") == "get_help" and message == "pending":
            session["data"]["action"] = "pending_payment"
            cache.set(f"{phone_number}_session", session)
            pending_work = Assignment.objects.filter(assignment_type="Outsourced").order_by("-created_at")[:7]
            if pending_work:
                return {
                    "is_valid": False,
                    "data": user,
                    "message": {
                        "response_type": "interactive",
                        "text": "*Pending Assignments*\n\n",
                        "username": f"{user.first_name} {user.last_name}",
                        "menu_name": "📝 Pending",
                        "menu_items" :[
                            {"id": f"payment_{work.id}", "name": f"Assignment {work.id}", "description": f"Status :{work.status}"} for work in pending_work
                        ]

                    }
                }
            return {
                "is_valid": False,
                "data": user,
                "message": {
                    "response_type": "button",
                    "text": "You have not been assigned any assignments yet. Please check back later.",
                }
            }
        elif session["data"].get("action") == "pending_payment" and message.startswith("payment_"):
            if message.split("_")[1] in [str(work.id) for work in Assignment.objects.filter(assignment_type="Outsourced")]:
                assignment_id = message.split("_")[1]
                assignment = Assignment.objects.get(id=assignment_id)
                if assignment:
                    return {
                        "is_valid": False,
                        "data": user,
                        "message": {
                            "response_type": "pay_download",
                            "text": f"Assignment: Assignment {assignment.id}\nAssignment Status: {assignment.status}\nPayment Status : {assignment.payment.status}\n\n*NB:* _You will be charged a fee for this service & we will only start working on it once you have completed the payment process._",
                        }
                    }               
        return {
            "is_valid": False,
            "data": user,
            "message": {
                "response_type": "interactive",
                "text": "Assignments Menu",
                "username": f"{user.first_name} {user.last_name}",
                "menu_name": "📝 Assignments",
                "menu_items" :[
                    {"id": "my_assignments", "name": "My Assignments", "description": "View your assignments"},
                    {"id": "get_help", "name": "Outsource Assignment", "description": "Get help with your assignments"},
                    {"id": "menu", "name": "Main Menu", "description": "Back to main menu"},
                ]
            }
        }

            