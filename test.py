from elevenlabs import ElevenLabs
client = ElevenLabs(api_key="sk_013fc9719d3453342f2b8ca3896a0b98fa2aff7f4db81a88")
print(client.voices.get_all())
