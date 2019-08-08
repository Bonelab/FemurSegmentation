FILE="./PYTHON/periosteal_segmentation.py"
LOG="../LOG/"

submit() {
	BASE="$1"
	LOG_FILE="${LOG}/PERIOSTEAL_${BASE}.LOG"

	cmd="python \"${FILE}\" \"${BASE}\" | tee -a \"${LOG_FILE}\""
  cmd="python \"${FILE}\" \"${BASE}\""
	echo $cmd
	eval $cmd
}

#submit RETRO_00005

