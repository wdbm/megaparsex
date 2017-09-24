#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
################################################################################
#                                                                              #
# megaparsex                                                                   #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program is a parser and associated utilities.                           #
#                                                                              #
# copyright (C) 2017 William Breaden Madden, name by Liam Moore                #
#                                                                              #
# This software is released under the terms of the GNU General Public License  #
# version 3 (GPLv3).                                                           #
#                                                                              #
# This program is free software: you can redistribute it and/or modify it      #
# under the terms of the GNU General Public License as published by the Free   #
# Software Foundation, either version 3 of the License, or (at your option)    #
# any later version.                                                           #
#                                                                              #
# This program is distributed in the hope that it will be useful, but WITHOUT  #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or        #
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for     #
# more details.                                                                #
#                                                                              #
# For a copy of the GNU General Public License, see                            #
# <http://www.gnu.org/licenses/>.                                              #
#                                                                              #
################################################################################
"""

import datetime
import json
import os
import requests
import subprocess
import sys
import time

name    = "megaparsex"
version = "2017-09-22T1419Z"

def trigger_keyphrases(
    text                          = None,  # input text to parse
    keyphrases                    = None,  # keyphrases for parsing input text
    response                      = True,  # optional text response on trigger
    function                      = None,  # optional function on trigger
    kwargs                        = None,  # optional function keyword arguments
    confirm                       = False, # optional return of confirmation
    confirmation_prompt           = "Do you want to continue? (y/n)",
    confirmation_feedback_confirm = "confirm",
    confirmation_feedback_deny    = "deny"
    ):

    """
    Parse input text for keyphrases. If any keyphrases are found, respond with
    text or by seeking confirmation or by engaging a function with optional
    keyword arguments. Return text or True if triggered and return False if not
    triggered. If confirmation is required, a confirmation object is returned,
    encapsulating a function and its optional arguments.
    """

    if any(pattern in text for pattern in keyphrases):

        if confirm:

            return confirmation(
                prompt           = confirmation_prompt,
                feedback_confirm = confirmation_feedback_confirm,
                feedback_deny    = confirmation_feedback_deny,
                function         = function,
                kwargs           = kwargs
            )

        if function and not kwargs:

            function()

        if function and kwargs:

            function(**kwargs)

        return response

    else:

        return False

def parse(
    text   = None,
    humour = 75
    ):

    """
    Parse input text using various triggers, some returning text and some for
    engaging functions. If triggered, a trigger returns text or True if and if
    not triggered, returns False. If no triggers are triggered, return False, if
    one trigger is triggered, return the value returned by that trigger, and if
    multiple triggers are triggered, return a list of the values returned by
    those triggers.

    Options such as humour engage or disengage various triggers.
    """

    triggers = []

    # humour

    if humour >= 75:

        triggers.extend([
            trigger_keyphrases(
                text       = text,
                keyphrases = [
                             "image"
                             ],
                response   = "http://i.imgur.com/MiqrlTh.jpg"
            ),
            trigger_keyphrases(
                text       = text,
                keyphrases = [
                             "sup",
                             "hi"
                             ],
                response   = "sup home bean"
            ),
            trigger_keyphrases(
                text       = text,
                keyphrases = [
                             "how are you",
                             "are you well",
                             "status"
                             ],
                response   = "nae bad fam"
            )
        ])

    # information

    triggers.extend([
        trigger_keyphrases(
            text       = text,
            keyphrases = [
                         "IP",
                         "I.P.",
                         "IP address",
                         "I.P. address",
                         "ip address"
                         ],
            response   = report_IP()
        )
    ])

    # actions

    triggers.extend([
        trigger_keyphrases(
            text                          = text,
            keyphrases                    = [
                                            "restart"
                                            ],
            function                      = restart,
            confirm                       = True,
            confirmation_prompt           = "Do you want to restart this "
                                            "program? (y/n)",
            confirmation_feedback_confirm = "confirm restart",
            confirmation_feedback_deny    = "deny restart"
        )
    ])

    if any([trigger for trigger in triggers if trigger is not False]):

        responses = [response for response in triggers if response]

        if len(responses) > 1:

            return responses

        else:

            return responses[0]

    else:

        return False

def multiparse(
    text         = None,
    parsers      = [parse],
    help_message = None
    ):

    """
    Parse input text by looping over a list of multiple parsers. If one trigger
    is triggered, return the value returned by that trigger, if multiple
    triggers are triggered, return a list of the values returned by those
    triggers. If no triggers are triggered, return False or an optional help
    message.
    """

    responses = []

    for _parser in parsers:

        response = _parser(text = text)

        if response is not False:

            responses.extend(response if response is list else [response])

    if not any(responses):

        if help_message:

            return help_message

        else:

            return False

    else:

        if len(responses) > 1:

            return responses

        else:

            return responses[0]

class confirmation(
    object
    ):

    """
    A confirmation object contains the ability to detect a confirmation or a
    denial in input text, and contains a prompt, a function to run, with
    optional keyword arguments, and feedback on confirmation or denial.
    """

    def __init__(
        self,
        prompt           = "Do you want to continue? (y/n)",
        feedback_confirm = "confirm",
        feedback_deny    = "deny",
        function         = None,
        kwargs           = None
        ):

        self._prompt           = prompt
        self._feedback_confirm = feedback_confirm
        self._feedback_deny    = feedback_deny
        self._function         = function
        self._kwargs           = kwargs

        self._feedback         = None
        self._confirmed        = None

    def prompt(
        self
        ):

        return self._prompt

    def feedback(
        self
        ):

        if self._confirmed is True:

            self._feedback = self._feedback_confirm

        if self._confirmed is False:

            self._feedback = self._feedback_deny

        return self._feedback

    def test(
        self,
        text = None
        ):

        """
        Parse input text as a confirmation or denial. If a confirmation is
        detected, return True and set internal confirmed state to True and if a
        denial is detected, return False and set internal confirmed state to
        False if a denial is detected, and if neither a confirmation nor a
        denial is detected, return None and set internal confirmed state to
        None.
        """

        if text is None:

            self._confirmed = None

            return None

        else:

            if text.lower() in ["y"]:

                self._confirmed = True

                return True

            elif text.lower() in ["n"]:

                self._confirmed = False

                return False

            else:

                self._confirmed = None

                return None

    def confirmed(
        self
        ):

        """
        Return internal confirmation state.
        """

        return self._confirmed

    def run(
        self
        ):

        """
        Engage contained function with optional keyword arguments.
        """

        if self._function and not self._kwargs:

            return self._function()

        if self._function and self._kwargs:

            return self._function(**self._kwargs)

    def __str__(
        self
        ):

        if self._kwargs is not None:

            kwargs = self._kwargs
            kwargs = ", ".join(
                [str(key) + "=" + str(kwargs[key]) for key in kwargs]
            )

        else:

            kwargs = ""

        return "confirmation: function: {function}({kwargs})".format(
            function = self._function.__name__,
            kwargs   = kwargs
        )

def get_input(
    prompt = None
    ):

    if sys.version_info >= (3, 0):

        return input(prompt)

    else:

        return raw_input(prompt)

def engage_command(
    command    = None,
    background = True
    ):

    if not background:

        process = subprocess.Popen(
            [command],
            shell      = True,
            executable = "/bin/bash"
        )
        process.wait()
        output, errors = process.communicate()

        return output

    else:

        subprocess.Popen(
            [command],
            shell      = True,
            executable = "/bin/bash"
        )

        return None

def report_IP(
    country = True,
    IP_only = False
    ):

    IP = "unknown"

    try:

        data_IP_website = requests.get("http://ipinfo.io/json")
        data_IP         = data_IP_website.json()
        IP              = data_IP["ip"]
        country         = data_IP["country"]

        if IP_only:

            text = IP

        else:

            text = "IP address: " + IP

            if country:

                text = text + " (" + country + ")"

        return text

    except:

        pass

    return "IP address: unknown"

def restart():

    import __main__
    os.execv(__main__.__file__, sys.argv)
