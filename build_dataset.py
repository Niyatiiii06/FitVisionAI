import sys

from src.dataset_builder import DatasetBuilder

builder = DatasetBuilder()

exercise = sys.argv[1]

builder.build(exercise)