import librosa
import numpy as np
import pretty_midi
from fastapi import FastAPI, UploadFile
import uvicorn
import soundfile as sf

app = FastAPI()

def humming_to_midi(audio_path, midi_path):
    y, sr = librosa.load(audio_path)
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    
    notes = []
    for i in range(pitches.shape[1]):
        pitch = pitches[:, i].max()
        if pitch > 0:
            midi_note = librosa.hz_to_midi(pitch)
            notes.append(midi_note)

    pm = pretty_midi.PrettyMIDI()
    instrument = pretty_midi.Instrument(program=0)

    time = 0
    for n in notes:
        note = pretty_midi.Note(velocity=90, pitch=int(n), start=time, end=time+0.2)
        instrument.notes.append(note)
        time += 0.2

    pm.instruments.append(instrument)
    pm.write(midi_path)

@app.post("/convert")
async def convert(file: UploadFile):
    audio_path = "input.wav"
    midi_path = "output.mid"

    with open(audio_path, "wb") as f:
        f.write(await file.read())

    humming_to_midi(audio_path, midi_path)

    return {"midi": "/output.mid"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)