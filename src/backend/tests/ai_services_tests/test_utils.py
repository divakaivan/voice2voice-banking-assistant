from pydantic_ai.messages import ModelRequest, ModelResponse, TextPart, UserPromptPart
from ai_services.utils import format_messages_for_agent

def test_format_messages_for_agent():
    """ Test the format_messages_for_agent function. """
    conversation_history = [
        {"sender": "user", "content": "Hello!"},
        {"sender": "agent", "content": "Hi, how can I help?"},
        {"sender": "user", "content": "Tell me a joke."},
        {"sender": "agent", "content": "Why did the chicken cross the road?"},
        {"sender": "system", "content": "This should be ignored."},
    ]

    expected_output = [
        ModelRequest(parts=[UserPromptPart(content="Hello!")]),
        ModelResponse(parts=[TextPart(content="Hi, how can I help?")]),
        ModelRequest(parts=[UserPromptPart(content="Tell me a joke.")]),
        ModelResponse(parts=[TextPart(content="Why did the chicken cross the road?")]),
    ]

    result = format_messages_for_agent(conversation_history)
    for i in range(len(result)):
        assert result[i].parts[0].content == expected_output[i].parts[0].content, f"Expected: {expected_output[i].parts.content}, got: {result[i].parts.content}"
        assert result[i].parts[0].part_kind == expected_output[i].parts[0].part_kind, f"Expected: {expected_output[i].part_kind}, got: {result[i].part_kind}"
    

def test_empty_conversation():
    assert format_messages_for_agent([]) == [], "Function should return an empty list for an empty conversation history."

def test_unknown_sender():
    conversation_history = [
        {"sender": "unknown", "content": "Should be ignored."},
    ]
    assert format_messages_for_agent(conversation_history) == [], "Function should ignore unknown sender messages."
