import pylrc
    
subs = pylrc.parse('./tests/nested.lrc')

print(subs.toSRT())

print('\n--------------------\n')

print(subs.toLRC())
