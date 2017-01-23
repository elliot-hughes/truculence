# ROOT styling
## Philosophy
1. Make your labels big
1. If possible, you should be able to interpret your plots unambiguously in grayscale.
1. [...]

## Setup
1. Inside of `~/.rootrc` make sure there's a line pointing to `rootlogon.C`: `Rint.Logon: [path to rootlogon.C]`.

## Styling functions
There're a few simple functions in `styling_tools.cc` to automatically style labels and text. These functions rely on the dimensions of the canvas and fonts in `rootlogon.C`.

### Example
`example_styling.cc` is an example that shows how I use the styling functions. Run it with `root -l example_styling.cc`. As you can see, a lot of the styling still needs to be hardcoded into the macro. Of course, you can make more customizeable styling functions, but at some point you just have to give up making macros pretty and just allow ROOT to be as annoying as it was designed to be.
