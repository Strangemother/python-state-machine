# Making testing easy

Testing should be fun. Doing python testing is actually funner. Making it easier is one step closer to victory and 100%

### Generating Test stubs

You can generate stubs for implementing tests by using pythoscope; the unittest generator

    $ pythoscope scatter

### Autodocs

The documentation is written to be parsed through Sphinx. Auto-generated documentation writes the source doc strings into a readme format.

#### Generating

Generating the documenation from the source can also be done with the built in Sphinx commands:

    $ sphinx-apidoc -o autodocs\build scatter

This will generate additional files the build command can read.

#### Build

Documentation is generated from the inline python and `.md` or `.rst` files in `autodocs/source`. This implements `Sphinx` and documentation can be generated on the command line:

    $ sphinx-build autodocs\source autodocs\build

Documentation is compiled to:

    ./autodocs/build/index.html

Documentation format can be altered from the root docs source:

    ./autodocs/source/index.md #etc


