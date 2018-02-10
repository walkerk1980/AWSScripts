#!/bin/bash

keyid=e191b72b-b2c4-44c0-a5a5-93e94c45a085
context='Context1=context1'
plaintext="abcdefg"

aws kms decrypt --ciphertext-blob fileb://<(aws kms encrypt --plaintext $plaintext --encryption-context $context --key-id $keyid --query CiphertextBlob --output text|base64 -D) --encryption-context $context --output text --query Plaintext|base64 -D;echo
