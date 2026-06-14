from yt_transcript import get_transcript
import yt_transcript as youtube_reader

print("MODULE FILE:", youtube_reader.__file__)
print("FUNCTION:", get_transcript)

url = "https://youtu.be/IkACdHCLn8Q"

result = get_transcript(url)

print(result[:500] if isinstance(result, str) else result)