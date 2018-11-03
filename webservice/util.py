
import librosa
import numpy as np
import random


def random_string(l):
    def to_char(x):
        if x < 10:
            return chr(48 + x)
        if x < 36:
            return chr(55 + x)
        return chr(61 + x)
    return "".join([to_char(random.randint(0, 61)) for _ in range(l)])


def extract_feature(file_name):
    audio, sample_rate = librosa.load(file_name)
    stft = np.abs(librosa.stft(audio))

    mfccs = np.mean(librosa.feature.mfcc(
        y=audio, sr=sample_rate, n_mfcc=40).T, axis=0)
    chroma = np.mean(librosa.feature.chroma_stft(
        S=stft, sr=sample_rate).T, axis=0)
    mel = np.mean(librosa.feature.melspectrogram(
        audio, sr=sample_rate).T, axis=0)
    contrast = np.mean(librosa.feature.spectral_contrast(
        S=stft, sr=sample_rate).T, axis=0)
    tonnetz = np.mean(librosa.feature.tonnetz(
        y=librosa.effects.harmonic(audio), sr=sample_rate).T, axis=0)
    return mfccs, chroma, mel, contrast, tonnetz


def get_features(audio_file):
    features = extract_feature(audio_file)
    ans = []
    for feat in features:
        ans.extend(feat)
    return ans
