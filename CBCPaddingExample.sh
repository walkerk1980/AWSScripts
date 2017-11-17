#!/bin/bash

echo -e "\n\rGenerating 16 bit hex IV...\n\r"
openssl rand -out iv.hex -hex 16

echo -e "\n\rGenerating 32 bit hex KEY...\n\r"
openssl rand -out key.hex -hex 32

echo -e "\n\rEchoing padded string 1111111111111111jonathanjonathanjonathanjonathan to plaintext.txt...\n\r"
echo '1111111111111111jonathanjonathanjonathanjonathan' >plaintext.txt

echo -e "\n\rEncrypting plaintext.txt with AES-128-CBC using our Key and IV...\n\r"
openssl enc -e -aes-128-cbc -in plaintext.txt -out ciphertext.bin -K `cat key.hex` -iv `cat iv.hex`

echo -e "\n\rDecrypting ciphertext.bin with AES-128-CBC using our Key and IV...\n\r"
openssl enc -d -aes-128-cbc -in ciphertext.bin -K `cat key.hex` -iv `cat iv.hex`

echo -e "\n\rDecrypting ciphertext.bin with AES-128-CBC using our Key and the wrong IV...\n\r"
openssl enc -d -aes-128-cbc -in ciphertext.bin -K `cat key.hex` -iv `openssl rand -hex 16`

echo -e "\n\rAs you can see, when the wrong IV is supplied to CBC decrytion you will lose the first block of data,\n\r\
after the first block of data you are fine because you have the previous block's ciphertext. This is not the case with\n\r\
the GCM algorithm because you XOR after decryption with the previous block's plaintext instead of it's ciphertext, which\n\r\
is not known to you because you cannot decrypt the previous block's plaintext for any block if you do not start with the\n\r\
correct IV.\n\r"
