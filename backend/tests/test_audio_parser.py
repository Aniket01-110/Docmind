from app.services.ingestion.audio_parser import(
    extract_audio_content,
    format_transcript_with_timestamp
)

def test_audio_parser():
    file_path = "tests/sample_audio.mp3"
    
    print("Testing audio parser")
    result = extract_audio_content(file_path)
    
    print(f"\n=== TRANSCRIPT ===")
    print(result["text"][:500])
    
    print(f"\n=== Language Detected ===")
    print(result["language"])
    
    print(f"\n=== Duration ===")
    print(f"{result['metadata']['duration_seconds']} seconds")
    
    print(f"\n=== SEGMENTS (first 8) ===")
    for segment in result["segments"][:8]:
        print(f"[{segment['start']}] {segment['text']}")

    print(f"\n=== TIMESTAMPED TRANSCRIPT ===")
    timestamped = format_transcript_with_timestamp(
        result["segments"]
    )
    print(timestamped[:500])
test_audio_parser()