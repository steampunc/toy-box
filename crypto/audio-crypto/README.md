This is a message-sharing program that takes advantage of pseudo-random numbers and audio files to store encrypted data.

It uses xor, so the encryption itself isn't that secure, but I'm relying on the idea that people won't know where the message is stored in the audio file, or be able to extract the message from white noise in the audio which is generated by a seeded random number generator. You will have to know that seed to be able to decrypt the data. If you're familiar with one-time pads, this also has an important flaw like one-time pads, which is that you can't use them more than once with the same seed, because then an experienced cryptographer could subtract the noise from the two messages then get a simple difference of two plaintext messages. Most people probably won't realize that though. 

Usage:
Run encrypter.py. `python encrypter.py`
Follow the instructions in the prompt for if you're encrypting a file or encrypting a simple message, then feed it the seed that you have decided on. It will save the message to a .wav file, then you can send that .wav file to the person you're communicating with.

To Decrypt:
Run decrypter.py. `python decrypter.py`
Follow the instructions in the prompt, giving it the name of the .wav file you're going to decrypt, then feed it the seed and it will decrypt it and print it out and save the decrypt to a file.