#!/usr/bin/env python3
"""translate_to_english.py

Usage:
    python translate_to_english.py <input_file> <output_file>

This script reads a French AsciiDoctor document, sends its content to the
LiteLLM API for translation to English, and writes the translated text to
<output_file>. If <output_file> already exists, its previous contents are
saved to <output_file>.old before being overwritten.

Configuration:
    The API key and model configuration is loaded automatically from a **.env** file at the
    project root **or** from environment variables. Optionally, you may still override it
    with the `--api-key` and `--model` CLI flags.

Dependencies::

        pip install "litellm>=1.0.0" python-dotenv

Note:
    This script uses LiteLLM which provides a unified interface for multiple LLM providers
    including OpenAI, Anthropic, Hugging Face, and others.
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path

from dotenv import load_dotenv
import litellm  # Requires litellm>=1.0.0

DEFAULT_MODEL = "openrouter/openai/gpt-4o-mini"  # Default model, can be overridden via CLI or env
TEMPERATURE = 0.2


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def backup_old_file(path: Path) -> None:
    """If *path* exists, copy it to *path*.old."""
    if path.exists():
        backup_path = path.with_suffix(path.suffix + ".old")
        shutil.copy2(path, backup_path)
        print(f"Backed up existing {path} to {backup_path}")


def translate(api_key: str, model: str, text: str) -> str:
    """Translate *text* from French to English using the LiteLLM API."""
    response = litellm.completion(
        api_key=api_key,
        model=model,
        temperature=TEMPERATURE,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a professional translator. Translate the following French "
                    "technical document about cybersecurity from French into clear, "
                    "concise English. Preserve ALL AsciiDoctor markup, code blocks, "
                    "and diagrams exactly as they appear—only translate natural language "
                    "sentences."
                ),
            },
            {"role": "user", "content": text},
        ],
    )
    return response.choices[0].message.content.strip()  # type: ignore[attr-defined]


def parse_args() -> argparse.Namespace:
    """Parse command‑line arguments."""
    parser = argparse.ArgumentParser(
        description="Translate a French AsciiDoctor document to English using the LiteLLM API."
    )
    parser.add_argument("input_file", help="Path to the source .adoc file in French")
    parser.add_argument("output_file", help="Path where the translated file will be written")
    parser.add_argument("--api-key", dest="api_key", help="Override the API key (else .env / env var)")
    parser.add_argument("--model", dest="model", default=DEFAULT_MODEL, help=f"Model to use for translation (default: {DEFAULT_MODEL})")
    parser.add_argument("--env-file", dest="env_file", default=None, help="Custom path to a .env file")
    return parser.parse_args()


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def main() -> None:
    args = parse_args()

    # ---------------------------------------------------------------------
    # Load .env configuration (before reading env vars)
    # ---------------------------------------------------------------------
    load_dotenv(dotenv_path=args.env_file, override=False)

    # Retrieve API key (CLI arg wins over ENV)
    api_key = args.api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        sys.exit(
            "Error: API key missing. Provide it in a .env file, "
            "set OPENAI_API_KEY, or pass --api-key."
        )

    # Get model (CLI arg wins over ENV, then default)
    model = args.model or os.getenv("MODEL") or DEFAULT_MODEL

    input_path = Path(args.input_file)
    output_path = Path(args.output_file)

    if not input_path.is_file():
        sys.exit(f"Error: {input_path} does not exist or is not a file.")

    # Backup existing output file if present
    backup_old_file(output_path)

    # Read input file
    with input_path.open("r", encoding="utf-8") as f:
        french_text = f.read()

    # Call LiteLLM to translate
    print(f"Translating {input_path.name} using model {model}... (this may take a moment)")
    try:
        english_text = translate(api_key, model, french_text)
    except Exception as e:
        sys.exit(f"Error while calling the LiteLLM API: {e}")

    # Write translated output
    with output_path.open("w", encoding="utf-8") as f:
        f.write(english_text)
    print(f"Translation saved to {output_path}")


if __name__ == "__main__":
    main()
