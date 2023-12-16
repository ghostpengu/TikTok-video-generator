import requests, base64, random, argparse, os, playsound, time, re, textwrap,random
import whisper
# https://twitter.com/scanlime/status/1512598559769702406
from moviepy.editor import VideoFileClip, AudioFileClip
from moviepy.audio.fx.all import audio_fadein, audio_fadeout
from pydub import AudioSegment
from pydub.playback import play

model = whisper.load_model("base")


voices = [
    # DISNEY VOICES
    'en_us_ghostface',            # Ghost Face
    'en_us_chewbacca',            # Chewbacca
    'en_us_c3po',                 # C3PO
    'en_us_stitch',               # Stitch
    'en_us_stormtrooper',         # Stormtrooper
    'en_us_rocket',               # Rocket

    # ENGLISH VOICES
    'en_au_001',                  # English AU - Female
    'en_au_002',                  # English AU - Male
    'en_uk_001',                  # English UK - Male 1
    'en_uk_003',                  # English UK - Male 2
    'en_us_001',                  # English US - Female (Int. 1)
    'en_us_002',                  # English US - Female (Int. 2)
    'en_us_006',                  # English US - Male 1
    'en_us_007',                  # English US - Male 2
    'en_us_009',                  # English US - Male 3
    'en_us_010',                  # English US - Male 4

    # EUROPE VOICES
    'fr_001',                     # French - Male 1
    'fr_002',                     # French - Male 2
    'de_001',                     # German - Female
    'de_002',                     # German - Male
    'es_002',                     # Spanish - Male

    # AMERICA VOICES
    'es_mx_002',                  # Spanish MX - Male
    'br_001',                     # Portuguese BR - Female 1
    'br_003',                     # Portuguese BR - Female 2
    'br_004',                     # Portuguese BR - Female 3
    'br_005',                     # Portuguese BR - Male

    # ASIA VOICES
    'id_001',                     # Indonesian - Female
    'jp_001',                     # Japanese - Female 1
    'jp_003',                     # Japanese - Female 2
    'jp_005',                     # Japanese - Female 3
    'jp_006',                     # Japanese - Male
    'kr_002',                     # Korean - Male 1
    'kr_003',                     # Korean - Female
    'kr_004',                     # Korean - Male 2

    # SINGING VOICES
    'en_female_f08_salut_damour'  # Alto
    'en_male_m03_lobby'           # Tenor
    'en_female_f08_warmy_breeze'  # Warmy Breeze
    'en_male_m03_sunshine_soon'   # Sunshine Soon

    # OTHER
    'en_male_narration'           # narrator
    'en_male_funny'               # wacky
    'en_female_emotional'         # peaceful
]


def tts(session_id: str, text_speaker: str = "en_au_001", req_text: str = "TikTok Text To Speech", filename: str = 'voice.mp3', play: bool = False):

    req_text = req_text.replace("+", "plus")
    req_text = req_text.replace(" ", "+")
    req_text = req_text.replace("&", "and")

    headers = {
        'User-Agent': 'com.zhiliaoapp.musically/2022600030 (Linux; U; Android 7.1.2; es_ES; SM-G988N; Build/NRD90M;tt-ok/3.12.13.1)',
        'Cookie': f'sessionid={session_id}'
    }
    url = f"https://api16-normal-c-useast2a.tiktokv.com/media/api/text/speech/invoke/?text_speaker={text_speaker}&req_text={req_text}&speaker_map_type=0&aid=1233"
    r = requests.post(url, headers = headers)

    if r.json()["message"] == "Couldn't load speech. Try again.":
        output_data = {"status": "Session ID is invalid", "status_code": 5}
        print(output_data)
        return output_data

    vstr = [r.json()["data"]["v_str"]][0]
    msg = [r.json()["message"]][0]
    scode = [r.json()["status_code"]][0]
    log = [r.json()["extra"]["log_id"]][0]
    
    dur = [r.json()["data"]["duration"]][0]
    spkr = [r.json()["data"]["speaker"]][0]

    b64d = base64.b64decode(vstr)

    with open(filename, "wb") as out:
        out.write(b64d)

    output_data = {
        "status": msg.capitalize(),
        "status_code": scode,
        "duration": dur,
        "speaker": spkr,
        "log": log
    }

    print(output_data)

    if play is True:
        playsound.playsound(filename)
        os.remove(filename)

    return output_data

def tts_batch(session_id: str, text_speaker: str = 'en_us_002', req_text: str = 'TikTok Text to Speech', filename: str = 'voice.mp3'):
    req_text = req_text.replace("+", "plus")
    req_text = req_text.replace(" ", "+")
    req_text = req_text.replace("&", "and")

    headers = {
        'User-Agent': 'com.zhiliaoapp.musically/2022600030 (Linux; U; Android 7.1.2; es_ES; SM-G988N; Build/NRD90M;tt-ok/3.12.13.1)',
        'Cookie': f'sessionid={session_id}'
    }
    url = f"https://api16-normal-useast5.us.tiktokv.com/media/api/text/speech/invoke/?text_speaker={text_speaker}&req_text={req_text}&speaker_map_type=0&aid=1233"

    r = requests.post(url, headers=headers)

    if r.json()["message"] == "Couldn't load speech. Try again.":
        output_data = {"status": "Session ID is invalid", "status_code": 5}
        print(output_data)
        return output_data

    vstr = [r.json()["data"]["v_str"]][0]
    msg = [r.json()["message"]][0]
    scode = [r.json()["status_code"]][0]
    log = [r.json()["extra"]["log_id"]][0]
    
    dur = [r.json()["data"]["duration"]][0]
    spkr = [r.json()["data"]["speaker"]][0]

    b64d = base64.b64decode(vstr)
    
    with open(filename, "wb") as out:
        out.write(b64d)

    output_data = {
        "status": msg.capitalize(),
        "status_code": scode,
        "duration": dur,
        "speaker": spkr,
        "log": log
    }

    print(output_data)

    return output_data

def batch_create(filename: str = 'voice.mp3'):
    out = open(filename, 'wb')

    def sorted_alphanumeric(data):
        convert = lambda text: int(text) if text.isdigit() else text.lower()
        alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
        return sorted(data, key=alphanum_key)
    
    for item in sorted_alphanumeric(os.listdir('./batch/')):
        filestuff = open('./batch/' + item, 'rb').read()
        out.write(filestuff)

    out.close()

def main():
    parser = argparse.ArgumentParser(description = "Simple Python script to interact with the TikTok TTS API")
    parser.add_argument("-v", "--voice", help = "the code of the desired voice")
    parser.add_argument("-t", "--text", help = "the text to be read")
    parser.add_argument("-s", "--session", help = "account session id")
    parser.add_argument("-f", "--file", help = "use this if you wanna use 'text.txt'")
    parser.add_argument("-n", "--name", help = "The name for the output file (.mp3)")
    parser.add_argument("-p", "--play", action='store_true', help = "use this if you want to play your output")
    args = parser.parse_args()

    text_speaker = args.voice

    if args.file is not None:
        req_text = open(args.file, 'r', errors='ignore', encoding='utf-8').read()
    else:
        if args.text == None:
            req_text = 'TikTok Text To Speech'
            print('You need to have one form of text! (See README.md)')
        else:
            req_text = args.text

    if args.play is not None:
        play = args.play

    if args.voice == None:
        text_speaker = 'en_us_002'
        print('You need to have a voice! (See README.md)')

    if text_speaker == "random":
        text_speaker = randomvoice()

    if args.name is not None:
        filename = args.name
    else:
        filename = 'voice.mp3'

    if args.session is None:
        print('FATAL: You need to have a TikTok session ID!')
        exit(1)

    if args.file is not None:
        chunk_size = 200
        textlist = textwrap.wrap(req_text, width=chunk_size, break_long_words=True, break_on_hyphens=False)

        os.makedirs('./batch/')

        for i, item in enumerate(textlist):
            tts_batch(args.session, text_speaker, item, f'./batch/{i}.mp3')
        
        batch_create(filename)

        for item in os.listdir('./batch/'):
            os.remove('./batch/' + item)
        
        os.removedirs('./batch/')

        return

    tts(args.session, text_speaker, req_text, filename, play)


def randomvoice():
    count = random.randint(0, len(voices))
    text_speaker = voices[count]

    return text_speaker

def sampler():
    for item in voices:
        text_speaker = item
        filename = item
        print(item)
        req_text = 'TikTok Text To Speech Sample'
        tts(text_speaker, req_text, filename)
def get_audio_duration(audio_path):
    # Load the audio clip
    audio_clip = AudioFileClip(audio_path)

    # Get the duration of the audio clip
    audio_duration = audio_clip.duration

    return audio_duration
def add_audio_to_video(video_path, audio_path, output_path):
    # Load video clip
    video_clip = VideoFileClip(video_path)

    # Load audio clip
    audio_clip = AudioFileClip(audio_path)

    # Add audio to video
    video_clip = video_clip.set_audio(audio_clip)

    # Set the audio fade in and fade out
    audio_clip = audio_fadein(audio_clip, 2).fx(audio_fadeout, 2)

    # Make sure the audio duration matches the video duration
    if audio_clip.duration < video_clip.duration:
        audio_clip = audio_clip.subclip(0, video_clip.duration)
    elif audio_clip.duration > video_clip.duration:
        audio_clip = audio_clip.subclip(0, video_clip.duration)

    # Set the audio with fades
    video_clip = video_clip.set_audio(audio_clip)

    # Adjust the time range to fit within the valid duration of the audio clip
    start_time = 0
    end_time = min(video_clip.duration + 2, start_time + get_audio_duration("voice.mp3"))  # Extend video duration by 1 second

    # Trim the video to match the adjusted time range
    video_clip = video_clip.subclip(start_time, end_time)

    # Save the result
    video_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

def combine_mp3s(mp3_files, output_file):
    # Load each MP3 file
    audio_segments = [AudioSegment.from_file(mp3_file, format="mp3") for mp3_file in mp3_files]

    # Concatenate the audio segments
    combined_audio = sum(audio_segments)

    # Export the combined audio to a new MP3 file
    combined_audio.export(output_file, format="mp3", bitrate="320k")

    print(f"Combined MP3 files saved to {output_file}")
def split_string(input_string, max_length=300):
    """Split a string into parts with a maximum length."""
    parts = []
    for i in range(0, len(input_string), max_length):
        part = input_string[i:i+max_length]
        parts.append(part)
    return parts

# Example usage:
input_string = input(":")
result = split_string(input_string)
mp3_files = []
# Print the result
for idx, part in enumerate(result, start=1):
    tts("4f72d2385f81a1d3ed121d3c1c75994a",req_text=part,filename=f"sounds\\{idx}.mp3")
    mp3_files.append(f"sounds\\{idx}.mp3")
    print(f"Part {idx}: {part}")
output_file = "voice.mp3"

time.sleep(1)
combine_mp3s(mp3_files, output_file)
video =  "1.mp4"

add_audio_to_video(video,"voice.mp3","out/vid.mp4")


