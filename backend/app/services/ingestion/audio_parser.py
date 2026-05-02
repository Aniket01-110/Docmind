import whisper
import os 
from typing import Optional

#load whisper model once at module level
# "base" model of openai whisper is best for local device , it is good balance of speed and accuracy and cost,downloads for first time, and then cached 
print("Loading Whisper model...")
whisper_model = whisper.load_model("base")

SUPPORTED_FORMATS = [
    ".mp3",
    ".wav", #uncompressed audio
    ".m4a", #apple audio format
    ".mp4", #audio with video
    "webm", #web audio/video
    ".ogg", #open source format
    ".flac", #lossless audio
]


#main function of extracting audio content

def extract_audio_content(file_path: str) -> dict:
    
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(
        f"AUDIO file not found: {file_path}")
        
    
    file_extensions = os.path.splitext(file_path)[1].lower()
    if file_extensions not in SUPPORTED_FORMATS:
        raise ValueError(
            f"Unsupported format: {file_extensions}"
            f"Supported: {SUPPORTED_FORMATS}")
        
        
        
    #Get file size for metadata
    File_size_kb = round(os.path.getsize(file_path)/1024,2)
    
    transcript = transcribe_audio(file_path)
    
    duration = get_audio_duration(file_path)
    
    return {
        "text": transcript["text"],
        "segments": transcript["segments"],
        "language": transcript["language"],
        "metadata" : {
            "file_path" : file_path,
            "file_size_kb" : File_size_kb,
            "duration_seconds": duration,
            "language" : transcript["language"],
            "file_type": "audio"
        },
        "total_pages" : 1,
        "tables" : []
    }
        

def transcribe_audio(file_path: str) -> dict:
    print(f"  Transcirbing audio: {file_path}")
    
    #transcribe is whispers main method
    
    result = whisper_model.transcribe(file_path, fp16=False,verbose=False)
    
    print(f" Audio transcription complete")
    print(f" Language detected:{result['language']}")
    print(f" Text length:{len(result['text'])}chars")
    
    return {
        "text": result["text"],
        "segments" : format_segments(result["segments"]),
        "language" : result["language"]
    }
    
def format_segments(segments: list) -> list:
    formatted  = []
    
    for segment in segments:
        
        start = seconds_to_timestamp(segment["start"])
        end = seconds_to_timestamp(segment["end"])
        
        formatted.append({
            "start": start,
            "end" : end, 
            "text" : segment["text"].strip()
        })
        
    return formatted

def seconds_to_timestamp(seconds : float) -> str:
    """ Converting Minutes to seconds"""
    minutes = int(seconds//60)
    remaining_seconds = int(seconds % 60)
    return f"{minutes:02d}:{remaining_seconds:02d}"

def get_audio_duration(file_path:str) -> Optional[float]:
    try:
        audio = whisper.load_audio(file_path)
        
        duration = len(audio) / whisper.audio.SAMPLE_RATE
        return round(duration, 2)
    
    except Exception:
        return None
    
def format_transcript_with_timestamp(segments: list) -> str:
    lines =[]
    
    for segment in segments:
        lines.append(f"[{segment['start']}] {segment['text']}")
        
    return "\n".join(lines)
    


        
        