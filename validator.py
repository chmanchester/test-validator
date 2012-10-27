from appvalidator.testcases.scripting import test_js_snippet, test_js_file
from appvalidator.errorbundle import ErrorBundle

from bs4 import BeautifulSoup

import optparse
import os

parser = optparse.OptionParser()
parser.add_option("-t", "--test", dest="test",
                  default=None,
                  help="Path to test, or directory containing tests. "
                       "Directories will be recursively searched."
parser.add_option("-v", "--verbose", dest="verbose",
                  default=False,
                  action="store_true",
                  help="Use verbose mode for output.")

opt, args = parser.parse_args()

if os.path.isfile(opt.test):
    files = [opt.test]
else:
    files = []
    for root, folders, fileList in os.walk(opt.test):
        for f in fileList:
            files.append(os.path.join(root,f))

bundle = ErrorBundle()
for name in files:
    print name
    f = open(name, 'r')
    if name.endswith('.js'):
        test_js_file(bundle, name, f.read())
    else:
        soup = BeautifulSoup(f.read())
        for script in soup.find_all('script'):
            test_js_snippet(bundle, script.renderContents(), name)
    f.close()

print bundle.print_summary(verbose=opt.verbose)
