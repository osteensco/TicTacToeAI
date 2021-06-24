#! python3
# A multi-clipboard program.

Text = {'agree': """Yes, I agree. That soungs fine to me.""",
        'busy': """Sorry, can we do this later this week or next week?""",
        'upsell': """Would you consider making this a monthly donation?"""}
import sys, pyperclip
if len(sys.argv)_ < 2:
    print('Usage: python MultiClipboard.py[keyphrase] - copy phrase text')
    sys.exit()

keyphrase = sys.argv[1] # first command line arg is the keyphrase

if keyphrase in Text:
    pyperclip.copy(TEXT[keyphrase])
    print('Text for ' + keyphrase + ' copied to clipboard.')
else:
    print('There is no text for ' + keyphrase)