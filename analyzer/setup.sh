#!/bin/zsh
# One-time setup for the analyzer: the main environment plus ADTOF's isolated TensorFlow environment
# and the model checkpoints that packages fail to fetch on their own.
set -e
cd "$(dirname "$0")"
uv sync
uv venv .venv-adtof --python 3.11
uv pip install --python .venv-adtof/bin/python adtof "git+https://github.com/MZehren/ADTOF" tf_keras
mkdir -p ~/piano_transcription_inference_data
[ -f ~/piano_transcription_inference_data/note_F1=0.9677_pedal_F1=0.9186.pth ] || \
  curl -L -o ~/piano_transcription_inference_data/note_F1=0.9677_pedal_F1=0.9186.pth \
  "https://zenodo.org/record/4034264/files/CRNN_note_F1%3D0.9677_pedal_F1%3D0.9186.pth?download=1"
echo "analyzer ready"
