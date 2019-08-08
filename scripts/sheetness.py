
# Imports
import os
import SimpleITK as sitk
import subprocess
import argparse

# Argument Parsing
parser = argparse.ArgumentParser(description='Compute sheetness enhanced filtering')
parser.add_argument('base_name', help='Scan base name (e.g. RETRO_00001)')
parser.add_argument('--hu_ending', default='.nii', help='Ending for the HU image')
parser.add_argument('--sheet_ending', default='_SHEET.nii', help='Ending for the shetness image')
parser.add_argument('--skin_ending', default='_SKIN.nii', help='Ending for the skin image')
parser.add_argument('--enhance_bright', default=1, help='Enhance bright objects? (1=Yes, 0=No)')
parser.add_argument('--number_of_sigma', default=2, help='How many sigmas to use for enhancing')
parser.add_argument('--min_sigma', default=0.5, help='How many sigmas to use for enhancing')
parser.add_argument('--max_sigma', default=1.0, help='How many sigmas to use for enhancing')
parser.add_argument('--air_threshold', default=-400.0, help='Threshold for determining air')
parser.add_argument('--metal_threshold', default=1200.0, help='Threshold for determining metal')
parser.add_argument('--trace_weight', default=0.05, help='Weight for reducing noise')
parser.add_argument('--project_directory', default=
  os.path.join(os.sep, *os.path.dirname(os.path.abspath(__file__)).split(os.sep)[:-2]),
  help='Base directory for project')
parser.add_argument('--model_dir', default=os.path.join('MODELS'),
  help='Directory for MODEL files')
parser.add_argument('--cpp_compiled', default=os.path.join('COM', 'CPP', 'Sheetness2'),
  help='The C++ code compiled to be ran')
args = parser.parse_args()

# Check inputs
print('Arguments:')
for arg in vars(args):
  print('  {}: {}'.format(arg, getattr(args, arg)))
print('')

MODEL_DIR = os.path.join(args.project_directory, args.model_dir)
CPP = os.path.join(args.project_directory, args.cpp_compiled)
HU_FILE_NAME = os.path.join(MODEL_DIR, args.base_name + args.hu_ending)
SHEET_FILE_NAME = os.path.join(MODEL_DIR, args.base_name + args.sheet_ending)
SKIN_FILE_NAME = os.path.join(MODEL_DIR, args.base_name + args.skin_ending)

print('')

# {cmd} {input} {skin} {sheetness} {enhance} {N} {min} {max} {lowThreshold} {highThreshold} {weight}
cmd = [
  CPP, HU_FILE_NAME, SKIN_FILE_NAME, SHEET_FILE_NAME, args.enhance_bright,
  args.number_of_sigma, args.min_sigma, args.max_sigma,
  args.air_threshold, args.metal_threshold, args.trace_weight
]
cmd = [str(x) for x in cmd]
print('CMD: {}'.format(cmd))
res = subprocess.check_output(cmd)
print('Result: ' + res)

print('Finished!')