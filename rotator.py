#!/usr/bin/env python3

# Intent was that this would run via cron and change my profile picture
# to a random picture in my selected folder every ~n minutes

import os
import discord
import json
import argparse
import random

import logging
import logging.config
from logging import debug, info
from logging import warning
from logging import error

def main(args):
    with open("pylogging.json") as f:
        config = json.load(f)
        logging.config.dictConfig(config)

    if args.quiet:
        logging.getLogger().setLevel(logging.WARNING)
    else:
        logging.getLogger().setLevel(logging.INFO)

    info(f"Parsed args: {args.__dict__}")

    TARGET = ""
    if args.dir:
        # Can omit f.is_file here because directory names won't match the allowed media types
        files = [
            f.path
            for f in os.scandir(args.dir)
            if f.name.endswith((".gif", ".jpeg", ".png", ".jpg"))
        ]
        debug(f"Files in directory {args.dir} are: {files}")
        TARGET = random.choice(files)
    elif args.file:
        if not os.path.isfile(args.file):
            error(f"{args.file} is not a file")
            return
        TARGET = args.file

    info(f"File to upload: {TARGET}")

    TOKEN = "DISCORD_USER_TOKEN"
    PASSWORD = "DISCORD_USER_PASSWORD"
    if args.creds:
        info("Creds flag was specified, using creds from creds.py")
        from creds import PASSWORD, TOKEN
    else:
        info("Creds flag was not specified, using environment variables")
        
        if os.environ.get(TOKEN) == None:
            error(f"Set Discord token as env var: {TOKEN} or use --creds")
            return
        TOKEN: str = os.environ.get(TOKEN)

        if os.environ.get(PASSWORD) == None:
            error(f"Set Discord account password as env var: {PASSWORD} or use --creds")
            return
        PASSWORD: str = os.environ.get(PASSWORD)

    client = discord.Client()

    @client.event
    async def on_ready():
        info(f"We have logged in as {client.user}")
        with open(TARGET, "rb") as image:
            try:
                await client.user.edit(password=PASSWORD, avatar=image.read())
                info("Successfully updated Discord avatar for user")
            except Exception as e:
                warning(f"Failed to update avatar with exception: {e}")
        await client.close()


    client.run(
        TOKEN,
        bot=False,
        reconnect=True,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Update Discord profile picture via command line"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-f",
        "--file",
        dest="file",
        action="store",
        help="File to use as profile picture",
    )
    group.add_argument(
        "-d",
        "--dir",
        dest="dir",
        action="store",
        help="Folder to choose profile picture from, chosen at random from media files in the directory.",
    )
    parser.add_argument(
        "-c",
        "--creds",
        dest="creds",
        action="store_true",
        help="Indicates the creds from creds.py should be used. If not supplied then environment variables will be used. See creds.py for more information.",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        dest="quiet",
        action="store_true",
        help="Enable quiet mode only logging errors.",
    )
    args = parser.parse_args()
    main(args)
