FILE="./PYTHON/sheetness.py"
LOG="../LOG/"

submit() {
	BASE="$1"
	LOG_FILE="${LOG}/SHEETNESS_${BASE}.LOG"

	cmd="python \"${FILE}\" \"${BASE}\" | tee -a \"${LOG_FILE}\""
	echo $cmd
	eval $cmd
}

#submit RETRO_00005
