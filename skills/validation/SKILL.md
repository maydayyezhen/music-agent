# Instrument validation

Run `scripts/critic_instruments.py`. Treat physical impossibilities and invalid ranges as errors;
treat repetition, register collision, flat velocity and bass-kick balance as contextual warnings.
Read the evidence before changing music or thresholds.

For `phrase_generation_mode: long_form_experimental`, also run
`.\.venv\Scripts\python.exe scripts\critic_long_form.py <song> --write`. Resolve early peaks,
phrase resets, missing cross-bar notes, automatic vibrato endings and broken relationship graphs.
