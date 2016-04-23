# README

## Installation instructions

This program is meant to be installed as a local `pip` module.  In the root of this directory, fun the following command:

```bash
pip install -e .
```

that will handle installing the module locally, so that the rest of the files can find it.  It will even handle installing the third-party dependencies that it needs.

## Running Part 2

If you want to run the evaluation for part 2, you can do so with the following:

```bash
python ngram __model__ __path_to_training_file__ __path_to_dev_file__ __path_to_test_file__
```

## Running Part 3

Part 3 is meant to be run from the `./sentence-judgement` directory.  You can run it like the following:

```bash
python ./part3.py __path_to_training_file_directory__ __path_to_Holmes_question_file__ > output.txt
```

Note: the program will attempt to run all of the files that it can find in the training file directory.  **DO NOT USE ALL OF THE TRAINING FILES**.  It will take an exceedingly long time to run them all.  While the processing will run on as many cores as possible (yay multithreading!) the sentence processing will take very long.

Redirect the output to some file, `output.txt`.  Debugging information will be printed to `stderr` to update the user on progress.  The resulting file can be piped into the `bestof5` program, per the example usage `.sh` file given.
