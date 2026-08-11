"""
Demo.

Run the entire platform.

Usage

python -m runner.demo
"""

from pathlib import Path

from runner.config import RunnerConfig
from runner.pipeline_runner import PipelineRunner


def main():

    config = RunnerConfig(

        input_file=Path(
            "sample_data/customers.csv"
        ),

        output_directory=Path(
            "output"
        ),

        enable_profiling=True,

        enable_validation=True,

    )

    runner = PipelineRunner(config)

    runner.run()


if __name__ == "__main__":

    main()