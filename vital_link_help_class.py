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
            "Vital Link can assist you with managing your medication schedule. "
            "You can ask me to set reminders for your medicines, check existing reminders, "
            "or delete a reminder. For example, say 'Remind me to take my medicine at 8 AM,' "
            "or 'What are my reminders?' How can I assist you?"
        )

        # Respond with the help message
        handler_input.response_builder.speak(help_message).ask(help_message)
        return handler_input.response_builder.response
