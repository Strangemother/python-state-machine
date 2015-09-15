from setuptools import setup, find_packages

def get_deps():
    r = open('requirements.txt')
    res = []
    for line in r.readlines():
        res.append( line.strip('\r\n') )
    return res

setup(
    name = "scatter",
    version = "0.1",
    packages = ['scatter'], # find_packages(),
    # scripts = ['say_hello.py'],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires = get_deps(),

    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst'],
        # And include any *.msg files found in the 'hello' package, too:
        'hello': ['*.msg'],
    },
    test_suite='nose.collector',
    tests_require=['nose'],
    # metadata for upload to PyPI
    author = "Jay Jagpal",
    author_email = "localhost@email.com",
    description = "Python distributed state machine",
    license = "MIT",
    keywords = "distributed state machine",
    # url = "http://example.com/HelloWorld/",   # project home page, if any

    # could also include long_description, download_url, classifiers, etc.
)
