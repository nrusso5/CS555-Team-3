# -*- coding: utf-8 -*-
"""Simple fact sample app."""

import random
import logging
import json
import prompts

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response

sb = SkillBuilder()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# Built-in Intent Handlers
class GetNewFactHandler(AbstractRequestHandler):
    """Handler for Skill Launch and GetNewFact Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_request_type("LaunchRequest")(handler_input) or
                is_intent_name("GetNewFactIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In GetNewFactHandler")

        # Provide the help message for the Vital Link skill on launch
        help_message = (
            "Hi! Welcome to Vital Link. I am your personal smart voice assistant. How can I assist you?"#I can assist you with managing your medication schedule. "
            #"You can ask me to set reminders for your medicines, check existing reminders, "
            #"or delete a reminder. For example, say 'Remind me to take my medicine at 8 AM,' "
            #"or 'What are my reminders?' How can I assist you?"
        )

        # Respond with the help message
        handler_input.response_builder.speak(help_message).ask(help_message)
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In HelpIntentHandler")

        # get localization data
        data = handler_input.attributes_manager.request_attributes["_"]

        speech = data[prompts.HELP_MESSAGE]
        reprompt = data[prompts.HELP_REPROMPT]
        handler_input.response_builder.speak(speech).ask(
            reprompt).set_card(SimpleCard(
                data[prompts.SKILL_NAME], speech))
        return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In CancelOrStopIntentHandler")

        # get localization data
        data = handler_input.attributes_manager.request_attributes["_"]

        speech = data[prompts.STOP_MESSAGE]
        handler_input.response_builder.speak(speech)
        return handler_input.response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    """Handler for Fallback Intent.

    AMAZON.FallbackIntent is only available in en-US locale.
    This handler will not be triggered except in that locale,
    so it is safe to deploy on any locale.
    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")

        # get localization data
        data = handler_input.attributes_manager.request_attributes["_"]

        speech = data[prompts.FALLBACK_MESSAGE]
        reprompt = data[prompts.FALLBACK_REPROMPT]
        handler_input.response_builder.speak(speech).ask(
            reprompt)
        return handler_input.response_builder.response


class LocalizationInterceptor(AbstractRequestInterceptor):
    """
    Add function to request attributes, that can load locale specific data.
    """

    def process(self, handler_input):
        locale = handler_input.request_envelope.request.locale
        logger.info("Locale is {}".format(locale))

        # localized strings stored in language_strings.json
        with open("language_strings.json") as language_prompts:
            language_data = json.load(language_prompts)
        # set default translation data to broader translation
        if locale[:2] in language_data:
            data = language_data[locale[:2]]
            # if a more specialized translation exists, then select it instead
            # example: "fr-CA" will pick "fr" translations first, but if "fr-CA" translation exists,
            # then pick that instead
            if locale in language_data:
                data.update(language_data[locale])
        else:
            data = language_data[locale]
        handler_input.attributes_manager.request_attributes["_"] = data


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In SessionEndedRequestHandler")

        logger.info("Session ended reason: {}".format(
            handler_input.request_envelope.request.reason))
        return handler_input.response_builder.response


# Exception Handler
class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch all exception handler, log exception and
    respond with custom message.
    """

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.info("In CatchAllExceptionHandler")
        logger.error(exception, exc_info=True)

        handler_input.response_builder.speak(EXCEPTION_MESSAGE).ask(
            HELP_REPROMPT)

        return handler_input.response_builder.response


# Request and Response loggers
class RequestLogger(AbstractRequestInterceptor):
    """Log the alexa requests."""

    def process(self, handler_input):
        # type: (HandlerInput) -> None
        logger.debug("Alexa Request: {}".format(
            handler_input.request_envelope.request))


class ResponseLogger(AbstractResponseInterceptor):
    """Log the alexa responses."""

    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        logger.debug("Alexa Response: {}".format(response))
    


class VitalLinkHelpIntentHandler(AbstractRequestHandler):
    """Handler for VitalLinkHelpIntent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("VitalLinkHelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In VitalLinkHelpIntentHandler")

        # Define the help message for the Vital Link skill
        help_message = (
            "Say, help with, then the name of the feature. Features include medicine reminders, healthy habit reminders, health challenges, exercise tracking, or other."
            #"Vital Link can assist you with managing your medication schedule. "
            #"You can ask me to set reminders for your medicines, check existing reminders, "
            #"or delete a reminder. For example, say 'Remind me to take my medicine at 8 AM,' "
            #"or 'What are my reminders?' How can I assist you?"
        )

        # Respond with the help message
        handler_input.response_builder.speak(help_message).ask(help_message)
        return handler_input.response_builder.response


class VitalLinkHelpIntent_MedicineRemindersHandler(AbstractRequestHandler):
    """Handler for VitalLinkHelpIntent_MedicineReminders."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("VitalLinkHelpIntent_MedicineReminders")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In VitalLinkHelpIntent_MedicineRemindersHandler")

        # Define the help message for the Vital Link skill
        help_message = (
            "To check current medicine reminders, say, check medicine reminders. To delete a medicine reminder, say, delete medicine reminder, then say the name of the medicine reminder to delete. To add a new medicine reminder, say, add medicine reminder, then say the name of the medicine to be reminded about, then say the hour to be reminded at, then say whether the hour is A.M. or P.M. "
        )

        # Respond with the help message
        handler_input.response_builder.speak(help_message).ask(help_message)
        return handler_input.response_builder.response



class VitalLinkHelpIntent_ExerciseTracking(AbstractRequestHandler):
    """Handler for VitalLinkHelpIntent_ExerciseTracking."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("VitalLinkHelpIntent_ExerciseTracking")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In VitalLinkHelpIntent_ExerciseTracking")

        # Define the help message for the Vital Link skill
        help_message = (
            "To track your exercise, say, log exercise, then specify the type of exercise, duration, and intensity level. To check your logged exercises, say, check my exercise log. To delete an exercise entry, say, delete exercise, then specify which entry to remove."
        )

        # Respond with the help message
        handler_input.response_builder.speak(help_message).ask(help_message)
        return handler_input.response_builder.response
        
        
        
        


class VitalLinkHelpIntent_HealthyHabitReminders(AbstractRequestHandler):
    """Handler for VitalLinkHelpIntent_HealthyHabitReminders."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("VitalLinkHelpIntent_HealthyHabitReminders")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In VitalLinkHelpIntent_HealthyHabitReminders")

        # Define the help message for the Vital Link skill
        help_message = (
            "To check current healthy habit reminders, say, check healthy habit reminders. To delete a healthy habit reminder, say, delete healthy habit reminder, then specify the habit reminder to delete. To add a new healthy habit reminder, say, add healthy habit reminder, then name the habit and specify the time and whether it's A.M. or P.M."
        )

        # Respond with the help message
        handler_input.response_builder.speak(help_message).ask(help_message)
        return handler_input.response_builder.response



class VitalLinkHelpIntent_HealthChallenges(AbstractRequestHandler):
    """Handler for VitalLinkHelpIntent_HealthChallenges."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("VitalLinkHelpIntent_HealthChallenges")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In VitalLinkHelpIntent_HealthChallenges")

        # Define the help message for the Vital Link skill
        help_message = (
            "To view available health challenges, say, list health challenges. To join a challenge, say, join health challenge, then mention the challenge name. To check your progress in a challenge, say, check my challenge progress."
        )

        # Respond with the help message
        handler_input.response_builder.speak(help_message).ask(help_message)
        return handler_input.response_builder.response



class VitalLinkHelpIntent_Other(AbstractRequestHandler):
    """Handler for VitalLinkHelpIntent_Other."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("VitalLinkHelpIntent_Other")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In VitalLinkHelpIntent_Other")

        # Define the help message for the Vital Link skill
        help_message = (
            "For general assistance, say, help me with something else. If you need help with a specific feature, please specify the name of the feature, such as exercise tracking or healthy habit reminders."
        )

        # Respond with the help message
        handler_input.response_builder.speak(help_message).ask(help_message)
        return handler_input.response_builder.response




# Register intent handlers
sb.add_request_handler(GetNewFactHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(VitalLinkHelpIntentHandler()) 
sb.add_request_handler(VitalLinkHelpIntent_MedicineRemindersHandler()) 
sb.add_request_handler(VitalLinkHelpIntent_ExerciseTracking()) 
sb.add_request_handler(VitalLinkHelpIntent_HealthyHabitReminders()) 
sb.add_request_handler(VitalLinkHelpIntent_HealthChallenges()) 
sb.add_request_handler(VitalLinkHelpIntent_Other()) 

# Register exception handlers
sb.add_exception_handler(CatchAllExceptionHandler())

# Register request and response interceptors
sb.add_global_request_interceptor(LocalizationInterceptor())
sb.add_global_request_interceptor(RequestLogger())
sb.add_global_response_interceptor(ResponseLogger())

# Handler name that is used on AWS lambda
lambda_handler = sb.lambda_handler()
