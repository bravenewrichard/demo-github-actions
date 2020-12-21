fname = "bitrise.yml"

new_stack = 'osx-xcode-12.1.x'

with open(fname, 'r') as f:
    s = f.read() 

with open(fname, 'w') as f:
    s = s.replace('<stack>', new_stack)
    f.write(s)


