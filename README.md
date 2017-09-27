![](https://raw.githubusercontent.com/wdbm/megaparsex/master/media/megaparsex.png)

# credits

- name by Liam Moore

# introduction

`megaparsex` is a Python module that features parsing and associated utilities. It features parsing functions that detect keyphrases in input text and that then return text, seek confirmations and run functions in response. It features functions that accept a list of parsing functions so that collections of parsing functions can be combined and new parsing functions can be added easily.

It features a confirmation class that contains the ability to check responses for confirmation or denial while containing a function with optional keyword arguments to run on detection of confirmation together with optional specialized prompts and responses to confirmation and denial. It features a command class that contains the ability to request an input that is to be run as a command and to run that command, and contains a prompt.

Some associated utilities are functions for manual input, to run system commands, to report IP information, to report weather information and to restart a script.

See example code for basic usage information.

# coding ideas

The multiparse function can combine a number of predefined or custom parser functions. Simple interactions involve responding to a single text input with text or by running a function. More complex interactions involve responding to a single text input but with a confirmation object which is used to ask for a confirmation before proceeding with defined actions. Still more complex interactions could involve nested parsers, whereby a parser or set of parsers is used to extract a response and that response can be used to propagate to nested parsers.
