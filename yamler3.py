import pathlib
import yaml
import pprint


in_file = "bitrise3.yml"
out_file = "bitrise4.yml"
old_stack = 'osx-xcode-12.1.x'
new_stack = 'osx-xcode-12.3.x'

with open(in_file, 'r') as infile:
    #data = yaml.load(f, Loader=yaml.FullLoader)
    y = yaml.safe_load(infile)
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(y)
    y['workflows']['primary']['meta']['bitrise.io']['stack'] = new_stack 
    print(y['workflows']['primary']['meta']['bitrise.io']['stack'])


with open(out_file, 'w') as outfile:
    yaml.dump(y, outfile, default_flow_style=False) 
