import os
#from google.cloud import texttospeech
#from google.cloud import texttospeech_v1
from google.cloud import texttospeech_v1beta1 as tos

import winsound

LOCALE_LIST = {"Afrikaans (South Africa)":"af-ZA",
               "Arabic":"ar-XA",
               "Bengali (India)":"bn-IN",
               "Bulgarian (Bulgaria)":"bg-BG",
               "Catalan (Spain)":"ca-ES",
               "Chinese (Hong Kong)":"yue-HK",
               "Czech (Czech Republic)":"cs-CZ",
               "Danish (Denmark)":"da-DK",
               "Dutch (Belgium)":"nl-BE",
               "Dutch (Netherlands)":"nl-NL",
               "English (Australia)":"en-AU",
               "English (India)":"en-IN",
               "English (UK)":"en-GB",
               "English (US)":"en-US",
               "Filipino (Philippines)":"fil-PH",
               "Finnish (Finland)":"fi-FI",
               "French (Canada)":"fr-CA",
               "French (France)":"fr-FR",
               "German (Germany)":"de-DE",
               "Greek (Greece)":"el-GR",
               "Gujarati (India)":"gu-IN",
               "Hindi (India)":"hi-IN",
               "Hungarian (Hungary)":"hu-HU",
               "Icelandic (Iceland)":"is-IS",
               "Indonesian (Indonesia)":"id-ID",
               "Italian (Italy)":"it-IT",
               "Japanese (Japan)":"ja-JP",
               "Kannada (India)":"kn-IN",
               "Korean (South Korea)":"ko-KR",
               "Latvian (Latvia)":"lv-LV",
               "Malay (Malaysia)":"ms-MY",
               "Malayalam (India)":"ml-IN",
               "Mandarin Chinese":"cmn-CN",
               "Mandarin Chinese":"cmn-TW",
               "Norwegian (Norway)":"nb-NO",
               "Polish (Poland)":"pl-PL",
               "Portuguese (Brazil)":"pt-BR",
               "Portuguese (Portugal)":"pt-PT",
               "Romanian (Romania)":"ro-RO",
               "Russian (Russia)":"ru-RU",
               "Serbian (Cyrillic)":"sr-RS",
               "Slovak (Slovakia)":"sk-SK",
               "Spanish (Spain)":"es-ES",
               "Spanish (US)":"es-US",
               "Swedish (Sweden)":"sv-SE",
               "Tamil (India)":"ta-IN",
               "Telugu (India)":"te-IN",
               "Thai (Thailand)":"th-TH",
               "Turkish (Turkey)":"tr-TR",
               "Ukrainian (Ukraine)":"uk-UA",
               "Vietnamese (Vietnam)":"vi-VN"}

client = tos.TextToSpeechClient()

class voice_param():
    text = ""
    name = ""
    language_code =""
    pitch=0
    speakingRate=1

def playAudio(voice_param):
    ssml_text = text_to_ssml(voice_param.text)
    ssml_to_audio(ssml_text, voice_param)

def text_to_ssml(plainText):
    """Synthesizes speech from the input string of ssml.

    Note: ssml must be well-formed according to:
        https://www.w3.org/TR/speech-synthesis/

    Example: <speak>Hello there.</speak>
    """

    # Convert plaintext to SSML
    # Wait two seconds between each address
    ssml = "<speak>{}</speak>".format(
        plainText.replace("\n", '\n<break time="0.5s"/>')
    )

    # Return the concatenated string of ssml script
    return ssml

def ssml_to_audio(ssml_text, voice_param):
    # Generates SSML text from plaintext.
    #
    # Given a string of SSML text and an output file name, this function
    # calls the Text-to-Speech API. The API returns a synthetic audio
    # version of the text, formatted according to the SSML commands. This
    # function saves the synthetic audio to the designated output file.
    #
    # Args:
    # ssml_text: string of SSML text
    #
    # Returns:
    # nothing

    # Instantiates a client
    #client = texttospeech.TextToSpeechClient()

    # Sets the text input to be synthesized
    synthesis_input = tos.SynthesisInput(ssml=ssml_text)

    # Builds the voice request, selects the language code ("en-US") and
    # the SSML voice gender ("MALE")
    voice = tos.VoiceSelectionParams(
        language_code=voice_param.language_code, 
        name=voice_param.name,
        ssml_gender=tos.SsmlVoiceGender.FEMALE
    )

    # Selects the type of audio file to return
    audio_config = tos.AudioConfig(
        audio_encoding=tos.AudioEncoding.LINEAR16,
        pitch=voice_param.pitch,
        speaking_rate=voice_param.speakingRate,
    )

    # Performs the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, 
        voice=voice, 
        audio_config=audio_config
    )

    winsound.PlaySound(response.audio_content, winsound.SND_MEMORY)

def get_voice_list(locale):
    voices = client.list_voices()
    voice_name_list = set([])
    for voice in voices.voices:
        name = voice.name
        if (name[:len(locale)] == locale):
            voice_name_list.add(voice.name)   
    return sorted(voice_name_list)

if __name__ == '__main__':
    print("Test")