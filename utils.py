import os

known_signatures = {"89504e47": "png",
                    "44445320": "dds",
                    "7b0d0a20": "json",
                    "706c6778": "plgx",
                    "7f524c43": "rlc",
                    "52494646": "riff",
                    "d2560102": "ov",
                    "00000001": "toc"
                    }


def _create_working_dir(filename: str) -> str:

    directory = "./" + filename + "_extracted/"

    try:
        os.mkdir(directory)
    except OSError:
        return ""
    else:
        return directory


def _get_extension_by_signature(signature: str) -> str:
    ext = known_signatures.get(signature)
    if ext:
        return ext
    else:
        return "unknown"
