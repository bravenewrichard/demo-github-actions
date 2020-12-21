import pathlib


fname = "bitrise.yml"
root = pathlib.Path(__file__).parent.resolve()

new_stack = 'osx-xcode-12.1.x'

"""
with open(fname, 'r') as f:
    s = f.read() 

with open(fname, 'w') as f:
    s = s.replace('<stack>', new_stack)
    f.write(s)
"""

bitriseyml = root / "bitrise.yml"
bitriseyml_contents = bitriseyml.open().read()
bitriseyml_contents = bitriseyml_contents.replace('<stack>', new_stack)
bitriseyml.open("w").write(bitriseyml_contents)
