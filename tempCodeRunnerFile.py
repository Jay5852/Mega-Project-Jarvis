else:
        # Check if it is a general OpenAI query
        handled = handleOpenAIQuery(command)
        if not handled:
            speak(f"I did not understand: {command}")