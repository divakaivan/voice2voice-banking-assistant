import pytest
from unittest.mock import ANY
from unittest.mock import AsyncMock
from nlp_processor.speech_to_text import transcribe_audio_data


@pytest.mark.asyncio
async def test_transcribe_audio_data():
    audio_data = b"fake_audio_data"
    model_name = "groq_model"
    temperature = 0.5
    language = "en"

    mock_api_client = AsyncMock()
    mock_response = AsyncMock()
    mock_response.text = "Hello, this is a test transcription."
    mock_api_client.audio.transcriptions.create.return_value = mock_response

    transcribed_text = await transcribe_audio_data(
        audio_data,
        mock_api_client,
        model_name,
        temperature,
        language
    )

    assert transcribed_text == "Hello, this is a test transcription.", "The transcribed text should match the response text"

    # ensure that the audio.transcriptions.create method was called with the expected arguments
    mock_api_client.audio.transcriptions.create.assert_called_once_with(
        model=model_name,
        file=ANY,
        temperature=temperature,
        language=language,
    )
