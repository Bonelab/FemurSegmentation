
# Imports
import os
import SimpleITK as sitk
import subprocess
import argparse

# Argument Parsing
parser = argparse.ArgumentParser(description='Perform graph cut segmentation on the image')
parser.add_argument('base_name', help='Scan base name (e.g. RETRO_00001)')
parser.add_argument('--sheet_ending', default='_SHEET.nii', help='Ending for the shetness image')
parser.add_argument('--mark_ending', default='_MARK.nii', help='Ending for the marked image')
parser.add_argument('--peri_ending', default='_PERI.nii', help='Ending for the periosteal segmentation')
parser.add_argument('--enhance_bright', default=1, help='Enhance bright objects? (1=Yes, 0=No)')
parser.add_argument('--sigma', default=0.25, help='Boundry term noise')
parser.add_argument('--gc_lambda', default=50.0, help='Smoothness term')
parser.add_argument('--project_directory', default=
  os.path.join(os.sep, *os.path.dirname(os.path.abspath(__file__)).split(os.sep)[:-2]),
  help='Base directory for project')
parser.add_argument('--model_dir', default=os.path.join('MODELS'),
  help='Directory for MODEL files')
parser.add_argument('--cpp_compiled', default=os.path.join('COM', 'CPP', 'PeriostealSegmentation'),
  help='The C++ code compiled to be ran')
args = parser.parse_args()

# Check inputs
print('Arguments:')
for arg in vars(args):
  print('  {}: {}'.format(arg, getattr(args, arg)))
print('')

MODEL_DIR = os.path.join(args.project_directory, args.model_dir)
CPP = os.path.join(args.project_directory, args.cpp_compiled)
SHEET_FILE_NAME = os.path.join(MODEL_DIR, args.base_name + args.sheet_ending)
MARK_FILE_NAME = os.path.join(MODEL_DIR, args.base_name + args.mark_ending)
PERI_FILE_NAME = os.path.join(MODEL_DIR, args.base_name + args.peri_ending)

labels = {
  "Femur_Right":  1,
  "Femur_Left":   2,
  "Pelvis_Right": 3,
  "Pelvis_Left":  4,
  "Sacrum":       5,
  "L5":           6,
  "L4":           7,
  "L3":           8,
  "L2":           9,
  "L1":           10
}

for name, label in labels.items():
  print('Processing label {} ({})'.format(label, name))
  temp_name = os.path.join(MODEL_DIR, args.base_name + "_TEMP_" + name + ".nii")

  # ${prog} ${input} ${mask} ${output} ${lambda} ${sigma} ${label}"
  cmd = [CPP, SHEET_FILE_NAME, MARK_FILE_NAME, temp_name, args.gc_lambda, args.sigma, label]
  cmd = [str(x) for x in cmd]
  print('  CMD: {}'.format(cmd))
  res = subprocess.check_output(cmd)
  print('  Result: {}'.format(res))
  print('')

print('Combining each segmentation')
first = labels.keys()[0]
temp_name = os.path.join(MODEL_DIR, args.base_name + "_TEMP_" + first + ".nii")
seg = sitk.ReadImage(str(temp_name), sitk.sitkUInt8)
seg = labels[first]*(seg>0)
os.remove(temp_name)

for name, label in labels.items():
  if name == first:
    continue

  temp_name = os.path.join(MODEL_DIR, args.base_name + "_TEMP_" + name + ".nii")
  this_label = sitk.ReadImage(str(temp_name), sitk.sitkUInt8)

  bin_seg = seg>0
  bin_this = this_label>0
  overlap = (bin_seg + bin_this)==2
  mask = 1 - overlap
  this_label = sitk.Mask(this_label, mask)

  seg = seg + label*(this_label>0)
  os.remove(temp_name)

print('Writing result to ' + PERI_FILE_NAME)
sitk.WriteImage(seg, PERI_FILE_NAME)
